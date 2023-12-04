from contextlib import asynccontextmanager
import datetime
from fastapi import FastAPI, Query, Header, Request, HTTPException
from fastapi.responses import JSONResponse
import json
import os.path
import pandas as pd
from pydantic import BaseModel
import requests
from typing import Annotated, List, Optional

qdf = pd.DataFrame()

users = {"alice": "wonderland",
        "bob": "builder",
        "clementine": "mandarine"
        }

admins = {'admin':'4dm1N'}

@asynccontextmanager
async def lifespan(app: FastAPI):
    '''
        If database file is not in current work directory download it.
        Read in database file, prepare data, and provide pandas dataframe.
    '''
    global qdf
    database_name = 'questions_en.csv'
    path_to_database = './' + database_name
    
    if not os.path.exists(path_to_database):
        print('Database not found. Download.')
        database_url = 'https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_en/questions_en.xlsx'
        database_response = requests.get(database_url)

        with open('questions_en.xlsx', 'wb') as output:
            output.write(database_response.content)
            df = pd.read_excel(output)

            # save to csv
            df.to_csv(database_name)

    qdf = pd.read_csv(database_name, index_col=0)
    
    yield

app = FastAPI(lifespan=lifespan)

class MyException(Exception):
    def __init__(self,                 
                 name : str,
                 date: str,
                 message: str):
        self.name = name
        self.message = message
        self.date = date
        
@app.exception_handler(MyException)
def MyExceptionHandler(
    request: Request,
    exception: MyException
    ):
    return JSONResponse(
        status_code=23,
        content={
            'url': str(request.url),
            'name': exception.name,
            'message': exception.message,
            'date': exception.date
        }
    )

def split_authorization(authorization: str):
    white_space_split = authorization.split()
    
    plan = white_space_split[0]
    
    colon_split = white_space_split[1].split(sep=':')
    username = colon_split[0]
    password = colon_split[1]
    
    return plan, username, password


def credentials_valid(username: str, password: str, accessors: dict):
    return username in accessors and password == accessors[username]

@app.get("/getMCQ")
async def getMCQ(use: str, quantity: int, subjects: List[str] = Query(None), 
                 credentials = Header(str)):
    try:
        _, username, password =  split_authorization(credentials)
        if not credentials_valid(username, password, users):
            raise MyException(name='Access error',
                              message='Access denied.',
                              date=str(datetime.datetime.now())
                              )
    except MyException:
            raise HTTPException(
            status_code=543,
            detail='Access denied.')
    
    df = qdf[(qdf['use']==use) & (qdf['subject'].isin(subjects))]
    if quantity < len(df):
        df.sample(quantity)

    MCQ_dict = {
        'use': use,
        'subjects':subjects,
        'quantity': quantity if (quantity < len(df)) else len(df),
        'questions':[],
        'responses': [],
        'correct_answers':[]
    }

    MCQ_dict['questions'] = df['question'].to_list()
    MCQ_dict['responses'] = df[['responseA', 'responseB','responseC','responseD']].values.tolist()
    MCQ_dict['correct_answers'] = df['correct'].to_list()

    return json.dumps(MCQ_dict)


@app.get('/status')
async def getStatus():
    return {'Status': 'SNAFU',
            'Functionality': True}

class Question(BaseModel):
    '''
    Question Model.
    '''
    use: str
    subject:str
    question: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None
    correct_answers: str
    remarks: Optional[str] = None


@app.put('/addQuestion')
async def AddQuestion(question: Question, credentials = Header(str)):
    '''
    Add Questions to database. Requires admin rights.
    '''

    MCQ_dict = {
        'question': question.question,
        'subjects': question.subject,
        'use': question.use,
        'correct': question.correct_answers,
        'responseA': question.responseA,
        'responseB': question.responseB,
        'responseC': question.responseC,
        'responseD': question.responseD,
        'remark': question.remarks
    }

    qdf.append(MCQ_dict)
    _, username, password =  split_authorization(credentials)
    if credentials_valid(username, password, admins):
        raise(MyException(name='Access error',
                    message='Access denied.',
                    date=str(datetime.datetime.now()),
                    ))

    return True
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, Header
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


def split_authorization(authorization: str):
    plan = "Basic"
    username = "username"
    password = "password"
    
    return plan, username, password


def check_credentials(username: str, password: str):



@app.get("/getMCQ")
async def getMCQ(use: str, quantity: int, subjects: List[str] = Query(None), 
                 authorization: Annotated[str | None, Header()] = None):

    _, username, password =  split_authorization(authorization)
    check_credentials(username, password)

    MCQ_dict = {
        'use': use,
        'subjects':subjects,
        'quantity': quantity,
        'questions':[],
        'responses': [],
        'correct_answers':[]
    }
    
    df = qdf[(qdf['use']==use) & (qdf['subject'].isin(subjects))]
    df.sample(quantity)

    MCQ_dict['questions'] = df['question'].to_list()
    MCQ_dict['responses'] = df[['responseA', 'responseB','responseC','responseD']].values.tolist()
    MCQ_dict['correct_answers'] = df['correct'].to_list()

    return json.dumps(MCQ_dict)


@app.get('/status')
async def getStatus():
    return {'Status': 'SNAFU',
            'Functionality': True}

class Question(BaseModel):
    use: str
    subject:str
    questions: str
    responseA: str
    responseB: str
    responseC: str
    responseD: Optional[str] = None
    correct_answers: str
    remarks: Optional[str] = None


@app.put('/addQuestion')
async def AddQuestionusers(question: Question, authorization: Annotated[str | None, Header()] = None):
    # new_id = max(users_db, key=lambda u: u.get('user_id'))['user_id']
    # new_user = {
    #     'user_id': new_id + 1,
    #     'name': user.name,
    #     'subscription': user.subscription
    # }
    # users_db.append(new_user)
    return True
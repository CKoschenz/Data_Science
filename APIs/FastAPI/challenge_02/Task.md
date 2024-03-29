# Task

#### Background
For this evaluation, we will put ourselves in the shoes of a company that creates questionnaires via a smartphone or web browser application. To simplify the architecture of these different products, the company wants to set up an API. The purpose of this API is to query a database to return a series of questions.

![](https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_en/api_eval.png)

Therefore, the objective of this evaluation is to create this API.

#### The data

Our database is represented by a csv file available at this [address](https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_fr/questions.csv).

You can download the dataset on your machine with this command:
```shell
wget https://dst-de.s3.eu-west-3.amazonaws.com/fastapi_en/questions_en.xlsx
```

You may need to install the following package to read excel files: `openpyxl`.

It contains the following fields:
- `question`: the title of the question
- `subject` : the category of the question
- `correct` : the list of correct answers
- `use`: the type of MCQ for which this question is used
- `answerA` : answer A
- `answerB` : answer B
- `answerC` : answer C
- `answerD` : the answer D (if it exists)

Explore this dataset to understand this data.

#### THE API

On the application or web browser, the user must be able to choose a test type (`use`) as well as one or more categories (`subject`). Moreover, the application can produce MCQs of 5, 10 or 20 questions. The API must therefore be able to return this number of questions. As the application must be able to generate many MCQs, the questions must be returned in a random order: thus, a request with the same parameters can return different questions.

As users must have created an account, we need to be able to verify their credentials. For now the API uses basic authentication, based on username and password: the string containing `Basic username:password` will have to be passed in the `Authorization` header (in theory, this string should be encoded but to simplify the exercise, we can choose not to encode it)

For the identifiers, we can use the following dictionary:
```json
{
    "alice": "wonderland",
    "bob": "builder",
    "clementine": "mandarine"
}
```

The API will also need to implement an endpoint to verify that the API is functional. Another feature should allow an `admin` user whose password is `4dm1N` to create a new question.

Finally, it should be widely documented and should return errors when it is called incorrectly.

#### Outputs

Expected output is one or more Python files containing the API code and a file containing the command to test the API. You can also provide a `requirements.txt` file listing the libraries to install. Finally, you can provide a document explaining the architecture choices made.
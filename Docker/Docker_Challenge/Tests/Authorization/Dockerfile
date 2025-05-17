FROM python:3

WORKDIR /Tests/Authorization

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Test_Authorization.py .

CMD [ "python", "Test_Authorization.py" ]

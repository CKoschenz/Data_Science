FROM python:3

WORKDIR /Tests/Authentication

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Test_Authentication.py .

CMD [ "python", "Test_Authentication.py" ]

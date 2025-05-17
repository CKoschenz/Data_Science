FROM python:3

WORKDIR /Tests/Content

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY Test_Content.py .

CMD [ "python", "Test_Content.py" ]

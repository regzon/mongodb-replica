FROM python:3.7-buster

WORKDIR /application

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]

EXPOSE 8000

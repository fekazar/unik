FROM python:3.11
WORKDIR /app
COPY requirements.txt requirements.txt

RUN ["pip3", "install", "-r", "requirements.txt"]
RUN ["mkdir", "/app/logs"]
RUN ["touch", "/app/logs/messages.log"]

COPY . .

ENTRYPOINT ["python3", "logging-consumer.py"]

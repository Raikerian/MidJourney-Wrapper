FROM python:3.8-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt && pip3 install requests

CMD [ "python3", "-u", "main.py" ]


FROM python:3.11-alpine

ENV PORT=5000

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

CMD gunicorn -w 4 -b 0.0.0.0:$PORT app:app

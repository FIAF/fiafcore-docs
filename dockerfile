
FROM python:3.11-alpine

WORKDIR /flask

COPY . /flask

RUN ls -al

RUN pip install -r requirements.txt

CMD [ "gunicorn", "-w", "4", "-b", "0.0.0.0:5086", "app:app"]

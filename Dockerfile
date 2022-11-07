FROM python:3

WORKDIR /resellingapi

COPY /requirements.txt /resellingapi/requirements.txt
COPY app /resellingapi/app

RUN pip3 install -r requirements.txt

WORKDIR /resellingapi/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]


FROM python:3.8-buster

RUN apt-get update
RUN apt-get install apt-utils -y --no-install-recommends
RUN apt-get install build-essential gcc python-dev -y
RUN apt-get install default-libmysqlclient-dev -y
RUN apt-get install cron -y

WORKDIR /usr/src/app

COPY Pipfile .
COPY Pipfile.lock .

RUN pip install pipenv
RUN pipenv install

COPY . .
RUN chmod +x runserver.sh

CMD ./runserver.sh
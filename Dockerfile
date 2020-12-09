FROM python:latest

WORKDIR /srv/recommender-service
COPY ./requirements.txt .
RUN apt-get update
RUN apt-get install -y default-libmysqlclient-dev libssl-dev default-mysql-client mysql-server
RUN python -m pip install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install flake8 pytest pytest-cov
COPY api ./api
COPY tests ./tests
COPY src ./src

FROM python:3.7.2

ENV FLASK_APP server.py

ENV FLASK_ENV development

WORKDIR /usr/src/app

# copy requirements.txt
COPY ./requirements.txt /usr/src/app/requirements.txt

COPY . .

RUN pip install pipenv

RUN pip install pip --upgrade

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]
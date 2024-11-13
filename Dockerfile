FROM python:3.10-bullseye

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pip install pipenv

COPY . .

EXPOSE 8080

CMD ["bash", "run.sh"]

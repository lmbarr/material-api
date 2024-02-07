FROM python:3.9

RUN pip install pipenv

WORKDIR /app
COPY Pipfile .
RUN pipenv install --python 3.9

COPY . .
CMD ["pipenv", "run", "python", "main.py", "0.0.0.0"]
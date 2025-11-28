FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install --upgrade pip &&\
pip install pipenv==2025.0.4

COPY ["Pipfile", "Pipfile.lock"]

RUN pipenv install

COPY . .

CMD ["python3", "./main.py"]
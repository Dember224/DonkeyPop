FROM python:3.12-slim-bookworm

WORKDIR /Users/antoinewashington/DonkeyPop

COPY rerquirements.txt ./

RUN pip install -r rerquirements.txt

COPY . .

CMD ["python3", "./main.py"]
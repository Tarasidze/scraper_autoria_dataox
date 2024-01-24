FROM python:3.11.3
LABEL maintainer="taras.diakiv.dev@gmial.com"

ENV PYTHONBUFFERED 1

WORKDIR app/

RUN apt-get update && apt-get install -y wget

RUN apt -f install -y
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install ./google-chrome-stable_current_amd64.deb -y

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get -y install libpq-dev gcc
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "python data_base_create.py && python main.py"]

FROM python:slim-bullseye

RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN apt-get update && apt-get install -y \
    python3-dev \
    default-libmysqlclient-dev \
    build-essential \
    libffi-dev \
    libjpeg-dev
RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/office

COPY requirements.txt .
COPY entrypoint.sh .

# Установка необходимых пакетов и компиляторов
RUN apk --update add \
    gcc \
    libc-dev \
    libffi-dev \
    jpeg-dev \
    zlib-dev \
    libjpeg \
    libwebp-dev \
    postgresql-dev \
    g++ \  # Компилятор C++
    make \  # Утилита make для сборки
    musl-dev \  # Библиотека musl для Alpine Linux

RUN pip install --upgrade pip
RUN pip --default-timeout=1200 install -r requirements.txt
RUN pip install --upgrade celery

RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "/usr/src/office/entrypoint.sh"]
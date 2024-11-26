FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/office

COPY requirements.txt .
COPY entrypoint.sh .

RUN apk --update add
RUN apk add gcc libc-dev libffi-dev jpeg-dev zlib-dev libjpeg libwebp-dev g++ make
RUN apk add postgresql-dev

RUN pip install --upgrade pip
RUN pip --default-timeout=1200 install -r requirements.txt
RUN pip install --upgrade celery

RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT ["sh", "/usr/src/office/entrypoint.sh"]

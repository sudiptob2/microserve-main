FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY ./scripts/entrypoint.sh /app/scripts/entrypoint.sh
COPY . /app
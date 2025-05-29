FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y build-essential libpq-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]


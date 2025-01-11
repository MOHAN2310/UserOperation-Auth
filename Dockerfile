FROM python:3.10-slim

WORKDIR /app

COPY . /app

COPY dev.env /app/dev.env

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
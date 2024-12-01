FROM python:3.9

VOLUME ["/app"]
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "-u", "app/main.py"]
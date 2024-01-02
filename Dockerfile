FROM python:3.11

WORKDIR /code

COPY requirements.txt .

RUN pip install --no-chache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8000"]

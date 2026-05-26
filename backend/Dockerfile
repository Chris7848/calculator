FROM python:3.11

RUN apt-get update && apt-get install -y ghdl

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]
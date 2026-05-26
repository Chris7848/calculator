FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ghdl python3 python3-pip

WORKDIR /app

COPY backend/ /app/

RUN pip3 install fastapi uvicorn

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "10000"]

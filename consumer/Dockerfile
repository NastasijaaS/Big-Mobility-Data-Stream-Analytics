FROM python:3.9-slim

COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

COPY . /app

WORKDIR /app

ENV CASSANDRA_HOST cassandra
ENV CASSANDRA_PORT 9042
ENV CASSANDRA_KEYSPACE bigdata
ENV POLLUTION_TABLE pollution
ENV TRAFFIC_TABLE traffic

ENV POLLUTION_TOPIC "minnhen-pollution"
ENV TRAFFIC_TOPIC "minnhen-traffic"
ENV KAFKA_URL "kafka:9092"

CMD ["python", "consumer.py"]


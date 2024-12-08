FROM bitnami/spark:latest

COPY requirements.txt /app/
RUN cd /app \
      && pip3 install -r requirements.txt

# Copy the source code
COPY . /app

ENV WINDOW_TYPE "tumbling"
ENV WINDOW_DURATION "20 seconds"
#ENV SLIDE_DURATION "10 seconds"

ENV EMISSION_TOPIC "minnhen-emission"
ENV FCD_TOPIC "minnhen-fcd"
ENV POLLUTION_TOPIC "minnhen-pollution"
ENV TRAFFIC_TOPIC "minnhen-traffic"

ENV KAFKA_URL "kafka:9092"

ENV SPARK_MASTER_NAME spark-master-x
ENV SPARK_MASTER_PORT 7077
ENV SPARK_APPLICATION_PYTHON_LOCATION /app/streaming.py
ENV SPARK_SUBMIT_ARGS "--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"

COPY submit.sh /
CMD ["/bin/bash", "/submit.sh"]

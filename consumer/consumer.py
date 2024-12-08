from confluent_kafka import Consumer
from cassandra.cluster import Cluster
import json
import uuid
import os

emission_topic = os.getenv('POLLUTION_TOPIC')
fcd_topic = os.getenv('TRAFFIC_TOPIC')
kafka_url =  os.getenv('KAFKA_URL')

cassandra_port = os.getenv('CASSANDRA_PORT')
cassandra_host = os.getenv('CASSANDRA_HOST')

keyspace = os.getenv('CASSANDRA_KEYSPACE')
pollution_table = os.getenv('POLLUTION_TABLE')
traffic_table = os.getenv('TRAFFIC_TABLE')


def write_pollution(session, record):
    print(f"Writing pollution data to Cassandra: {record}")
    query = f"""
        INSERT INTO {pollution_table} (id, date, laneid, laneco, laneco2, lanehc, lanenox, lanepmx, lanenoise)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    session.execute(query, (
        uuid.uuid4(),
        record.get("Date"),
        record.get("LaneId"),
        record.get("LaneCO"),
        record.get("LaneCO2"),
        record.get("LaneHC"),
        record.get("LaneNOx"),
        record.get("LanePMx"),
        record.get("LaneNoise")
    ))


def write_traffic(session, record):
    print(f"Writing traffic data to Cassandra: {record}")
    query = f"""
        INSERT INTO {traffic_table} (id, date, laneid, vehiclecount)
        VALUES (%s, %s, %s, %s)
    """
    session.execute(query, (
        uuid.uuid4(),
        record.get("Date"),
        record.get("LaneId"),
        record.get("VehicleCount")
    ))


def handle_message(msg, session):
    try:
        record = json.loads(msg.value().decode('utf-8'))
        topic = msg.topic()

        if topic == emission_topic:
            write_pollution(session, record)
        elif topic == fcd_topic:
            write_traffic(session, record)
        else:
            print(f"Unknown topic: {topic}")
    except Exception as e:
        print(f"Error processing message from topic {msg.topic()}: {e}")


def main():

    conf = {
        'bootstrap.servers': kafka_url,
        'group.id': 'consumer_group',
        'auto.offset.reset': 'earliest'
    }
    consumer = Consumer(conf)

    topics = [emission_topic, fcd_topic]
    consumer.subscribe(topics)

    cassandra_cluster = Cluster([cassandra_host], port=cassandra_port)
    session = cassandra_cluster.connect()
    session.set_keyspace(keyspace)

    print("Connected to Kafka and Cassandra.")
    print(f"Subscribed to topics: {topics}")

    try:
        while True:
            msg = consumer.poll(timeout=1.0)

            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            handle_message(msg, session)
    except KeyboardInterrupt:
        print("Stopping consumers...")
    finally:
        consumer.close()
        cassandra_cluster.shutdown()
        print("Closed Kafka consumer and Cassandra connection.")

if __name__ == "__main__":
    main()

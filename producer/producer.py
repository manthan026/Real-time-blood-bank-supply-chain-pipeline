"""
producer.py

Reads fake events from faker_data.py and publishes
them to the Kafka topic.
"""

import json
import time

from kafka import KafkaProducer

from config import (
    KAFKA_BROKER,
    TOPIC_NAME,
    PRODUCER_CLIENT_ID,
    MESSAGE_INTERVAL
)

from faker_data import generate_event


# Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    client_id=PRODUCER_CLIENT_ID,
    value_serializer=lambda value: json.dumps(value).encode("utf-8")
)


def send_events():
    """
    Continuously generates and sends events to Kafka.
    """

    
    print(" Blood Bank Producer Started...")
    

    try:
        while True:

            event = generate_event()

            producer.send(TOPIC_NAME, value=event)

            producer.flush()

            print(
                f"[{event['event_type'].upper()}] "
                f"Event Sent | ID: {event['event_id']}"
            )

            print(event)
           

            time.sleep(MESSAGE_INTERVAL)

    except KeyboardInterrupt:
        print("\nStopping Producer...")

    finally:
        producer.close()
        print("Producer Closed Successfully.")


if __name__ == "__main__":
    send_events()
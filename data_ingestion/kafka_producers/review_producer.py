import json, random, time
from kafka import KafkaProducer
from faker import Faker
from wheel.wheelfile import WheelFile

from config import TOPICS, KAFKA_BROKER

fake= Faker()
producer = KafkaProducer(bootstrap_servers= KAFKA_BROKER, value_serializer=lambda v:json.dumps(v).encode('utf-8'))

def generate_review():
    return {
        "review_id": fake.uuid4(),
        "product_id": random.randint(100, 500),
        "customer_id": fake.uuid4(),
        "rating": random.randint(1, 5),
        "review_text": fake.sentence(nb_words=15),
        "review_date": fake.date_this_year().isoformat()
    }

if __name__ == "__main__":
    while True:
        msg = generate_review()
        producer.send(TOPICS['reviews'], msg)
        print(f"Sent: {msg}")
        time.sleep(4)
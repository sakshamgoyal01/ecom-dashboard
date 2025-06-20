from kafka import KafkaProducer
from faker import Faker
import json
import time
from config import KAFKA_BROKER, TOPICS

fake = Faker()
producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER,value_serializer=lambda v:json.dumps(v).encode('UTF-8'))

def generate_customer():
    return {
        "customer_id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "signup_date": fake.date_this_decade().isoformat(),
        "location": fake.city()
    }

if __name__ == "__main__":
    while True:
        msg= generate_customer()
        producer.send(TOPICS['customers'],msg)
        print(f"Sent: {msg}")
        time.sleep(2)
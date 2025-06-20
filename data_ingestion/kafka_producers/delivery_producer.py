import json, random, time
from kafka import KafkaProducer
from faker import Faker
from config import TOPICS, KAFKA_BROKER

fake= Faker()
producer = KafkaProducer(bootstrap_servers= KAFKA_BROKER, value_serializer=lambda v:json.dumps(v).encode('utf-8'))

def generate_delivery():
    return {
         "delivery_id": fake.uuid4(),
        "transaction_id": fake.uuid4(),
        "dispatch_time": fake.iso8601(),
        "expected_delivery": random.randint(2, 7),
        "actual_delivery": random.randint(2, 7),
        "region": fake.state(),
        "carrier": random.choice(["Delhivery", "BlueDart", "Ekart", "XpressBees"]),
        "status": random.choice(["Dispatched", "In Transit", "Delivered"])
    }

if __name__ == "__main__":
    while True:
        msg = generate_delivery()
        producer.send(TOPICS['deliveries'], msg)
        print(f"Sent: {msg}")
        time.sleep(3)
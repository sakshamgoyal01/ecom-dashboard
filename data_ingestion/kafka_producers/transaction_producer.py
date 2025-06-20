import json, random, time
from kafka import KafkaProducer
from faker import Faker
from config import TOPICS, KAFKA_BROKER

fake = Faker()
producer = KafkaProducer(bootstrap_servers= KAFKA_BROKER, value_serializer=lambda v:json.dumps(v).encode('utf-8'))

def generate_transaction():
    return{
        "transaction_id": fake.uuid4(),
        "customer_id": fake.uuid4(),
        "product_id": random.randint(100, 500),
        "amount": round(random.uniform(200, 2000), 2),
        "payment_method": random.choice(["UPI", "Card", "NetBanking", "COD"]),
        "timestamp": fake.iso8601()
    }

if __name__ == "__main__":
    while True:
        msg= generate_transaction()
        producer.send(TOPICS['transactions'],msg)
        print(f"sent: {msg}")
        time.sleep(2)
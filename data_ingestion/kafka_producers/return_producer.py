# returns_producer.py
from kafka import KafkaProducer
import json
import random
from datetime import datetime, timedelta
import time
from faker import Faker
from config import TOPICS, KAFKA_BROKER
fake = Faker()


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)



def generate_returns():
    order_date = datetime.now() - timedelta(days=random.randint(5, 30))
    delivery_date = order_date + timedelta(days=random.randint(1, 7))
    return {
        "transaction_id": fake.uuid4(),
        "order_date": order_date.strftime("%Y-%m-%d"),
        "delivery_date": delivery_date.strftime("%Y-%m-%d"),
        "product_category": random.choice(["Electronics", "Laptops", "Groceries", "Home_Essentials", "Toys"]),
        "past_returns": random.randint(0, 5),
        "price": round(random.uniform(200, 2000), 2),
        "return_flag": random.choices([0, 1], weights=[0.8, 0.2])[0]
    }


if __name__ == "__main__":
    while True:
        msg= generate_returns()
        producer.send(TOPICS['returns'],msg)
        print(f"sent: {msg}")
        time.sleep(2)

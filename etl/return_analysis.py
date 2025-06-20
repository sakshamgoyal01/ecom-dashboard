# return_analysis_kafka.py
from kafka import KafkaConsumer
import pandas as pd
import json
import os

def generate_return_features(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure missing return_flag is treated as 0
    df['return_flag'] = df['return_flag'].fillna(0).astype(int)

    # Calculate delivery time
    df['delivery_days'] = (
        pd.to_datetime(df['delivery_date']) - pd.to_datetime(df['order_date'])
    ).dt.days

    return df

# Kafka config
TOPIC = "ecom_returns"
BOOTSTRAP_SERVERS = ["localhost:9092"]
SAVE_PATH = "processed/returns_train.csv"
BATCH_SIZE = 50

# Ensure output directory exists
os.makedirs("processed", exist_ok=True)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP_SERVERS,
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True
)

print(f"✅ Listening to Kafka topic: {TOPIC}")

batch = []

try:
    for msg in consumer:
        batch.append(msg.value)

        if len(batch) >= BATCH_SIZE:
            df_raw = pd.DataFrame(batch)

            # Clean/transform the data
            df_cleaned = generate_return_features(df_raw)

            # Save to CSV
            if not os.path.exists(SAVE_PATH):
                df_cleaned.to_csv(SAVE_PATH, index=False)
            else:
                df_cleaned.to_csv(SAVE_PATH, index=False, mode='a', header=False)

            print(f"✅ Processed and saved batch of {BATCH_SIZE} transactions.")
            batch = []

except KeyboardInterrupt:
    print("🛑 Consumer stopped.")
finally:
    consumer.close()

from kafka import KafkaConsumer
import pandas as pd
import json
import os

def clean_customer_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop_duplicates(subset='customer_id')
    df.columns = df.columns.str.strip().str.lower()
    df['signup_date'] = pd.to_datetime(df['signup_date'])
    df['location'] = df['location'].str.title().str.strip()
    return df

TOPIC = "ecom_customers"
BOOTSTRAP_SERVERS = ["localhost:9092"]
SAVE_PATH = "processed/cleaned_customers.csv"
BATCH_SIZE = 50

os.makedirs("processed", exist_ok=True)

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

            # 👇 Apply your ETL cleaning logic
            df_cleaned = clean_customer_data(df_raw)

            # Append to CSV
            if not os.path.exists(SAVE_PATH):
                df_cleaned.to_csv(SAVE_PATH, index=False)
            else:
                df_cleaned.to_csv(SAVE_PATH, index=False, mode='a', header=False)

            print(f"✅ Processed and saved batch of {BATCH_SIZE} customer records.")

            batch = []

except KeyboardInterrupt:
    print("🛑 Consumer stopped.")
finally:
    consumer.close()
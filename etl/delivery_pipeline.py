from kafka import KafkaConsumer
import pandas as pd
import json
import os

def process_delivery_data(df: pd.DataFrame) -> pd.DataFrame:
    df["actual_delivery"] = pd.to_datetime(df["actual_delivery"], errors="coerce")
    df["expected_delivery"] = pd.to_datetime(df["expected_delivery"], errors="coerce")
    df['dispatch_time'] = pd.to_datetime(df['dispatch_time'])
    df['expected_delivery'] = df['dispatch_time'] + pd.to_timedelta(df['expected_delivery'], unit='d')
    df['actual_delivery'] = pd.to_datetime(df['actual_delivery'])
    df['delay_days'] = (df['actual_delivery'] - df['expected_delivery']).dt.days
    df['delayed'] = df['delay_days'] > 0
    return df

TOPIC = "ecom_deliveries"
BOOTSTRAP_SERVERS = ["localhost:9092"]
SAVE_PATH = "processed/deliveries.csv"
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
            df_cleaned = process_delivery_data(df_raw)

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
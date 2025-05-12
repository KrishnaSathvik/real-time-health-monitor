import json
import time
import random
from kafka import KafkaProducer

# Create Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Simulate vitals
def generate_vitals():
    return {
        "patient_id": random.randint(1000, 1010),
        "heart_rate": random.randint(60, 120),
        "blood_pressure": f"{random.randint(100, 140)}/{random.randint(70, 90)}",
        "spo2": random.randint(90, 100),
        "timestamp": time.time()
    }

# Send vitals to Kafka every 2 seconds
while True:
    vitals = generate_vitals()
    producer.send('health-vitals', vitals)
    print(f"Sent: {vitals}")
    time.sleep(2)

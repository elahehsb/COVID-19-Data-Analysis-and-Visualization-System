import requests
import json
from kafka import KafkaProducer
import time

def fetch_covid_data(api_url):
    response = requests.get(api_url)
    data = response.json()
    return data

def produce_messages(producer, topic, data):
    producer.send(topic, json.dumps(data).encode('utf-8'))

if __name__ == "__main__":
    api_url = "https://api.covid19api.com/summary"
    kafka_topic = "covid"
    kafka_producer = KafkaProducer(bootstrap_servers='localhost:9092')

    while True:
        data = fetch_covid_data(api_url)
        produce_messages(kafka_producer, kafka_topic, data)
        time.sleep(3600)  # Fetch new data every hour

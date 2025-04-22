# fluvio_streaming/consumer.py
import json
from threading import Thread
from fluvio import Fluvio

# Shared dictionary to store live prices
live_prices = {}

def handle_stock_update(record):
    data = json.loads(record.value_string())
    ticker = data.get("ticker")
    price = data.get("price")
    if ticker and price:
        live_prices[ticker] = price
        print(f"[Fluvio] {ticker}: ${price:.2f}")

def start_fluvio_consumer():
    def run_consumer():
        fluvio = Fluvio.connect()
        consumer = fluvio.partition_consumer("stock-updates", 0)
        print("[Fluvio] Listening for stock updates...")
        for record in consumer.stream():
            handle_stock_update(record)
    
    Thread(target=run_consumer, daemon=True).start()

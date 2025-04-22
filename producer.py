# producer.py
import fluvio
import json
import yfinance as yf

def fetch_stock_data(ticker):
    # Fetch stock data for the last day with 1-minute intervals
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d", interval="1m")  # Adjust as needed
    return data.to_dict(orient="records")

def produce_data_to_fluvio(ticker):
    # Connect to Fluvio
    client = fluvio.Fluvio()
    producer = client.topic("stock_data").producer()

    # Fetch live stock data
    stock_data = fetch_stock_data(ticker)

    # Send each data point to Fluvio
    for record in stock_data:
        producer.send(json.dumps(record).encode('utf-8'))
        print(f"Sent data: {record}")

    producer.flush()
    client.close()

if __name__ == "__main__":
    ticker = "AAPL"  # Example ticker (Apple)
    produce_data_to_fluvio(ticker)

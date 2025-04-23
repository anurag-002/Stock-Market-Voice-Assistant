import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.fetch import fetch_stock_data

import fluvio
import json
from utils.fetch import fetch_stock_data

# Initialize the Fluvio producer
async def produce_stock_data(ticker: str, topic_name: str):
    try:
        # Connect to Fluvio
        client = await fluvio.connect()
        producer = client.create_producer(topic_name)
        
        # Fetch the stock data
        stock_data = fetch_stock_data(ticker)
        
        # Convert stock data to a dictionary and then to JSON format
        stock_data_json = stock_data.to_dict()
        
        # Publish the data to Fluvio
        await producer.send(json.dumps(stock_data_json).encode())
        
        print(f"Stock data for {ticker} sent to Fluvio topic {topic_name}.")
        
        # Close the producer connection
        await producer.flush()
        await producer.close()
    except Exception as e:
        print(f"Error in Fluvio producer: {str(e)}")

# Example usage:
# asyncio.run(produce_stock_data("AAPL", "stock-topic"))

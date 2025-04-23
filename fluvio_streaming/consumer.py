import fluvio
import json

# Initialize the Fluvio consumer
async def consume_stock_data(topic_name: str):
    try:
        # Connect to Fluvio
        client = await fluvio.connect()
        consumer = client.create_consumer(topic_name)
        
        # Start consuming messages
        async for message in consumer.stream():
            # Decode the message
            stock_data = json.loads(message.value.decode())
            
            # Process the stock data (you can replace this with your actual logic)
            print(f"Received stock data: {stock_data}")
            
        # Close the consumer connection
        await consumer.close()
    except Exception as e:
        print(f"Error in Fluvio consumer: {str(e)}")

# Example usage:
# asyncio.run(consume_stock_data("stock-topic"))

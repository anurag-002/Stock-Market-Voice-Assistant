# main.py
from producer import produce_data_to_fluvio
from fluvio_streaming import consume_data_from_fluvio

def run_producer():
    ticker = "AAPL"  # Change to the stock you want
    produce_data_to_fluvio(ticker)

def run_consumer():
    consume_data_from_fluvio()

if __name__ == "__main__":
    # Change this to either run the producer or the consumer
    run_producer()  # For producing data
    # run_consumer()  # For consuming data

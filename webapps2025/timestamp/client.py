import os
import thriftpy2 as thriftpy
from thriftpy2.rpc import make_client
from thriftpy2.thrift import TException


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 10000


# Load timestamp.thrift file
timestamp_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__), "timestamp.thrift"),
    module_name="timestamp_thrift"
)
service = timestamp_thrift.TimestampService


def get_timestamp():
    try:
        client = make_client(service, SERVER_ADDRESS, SERVER_PORT)
        result = client.getCurrentTimestamp()
        return result
    except TException as e:
        print(f"Thrift exception: {e}")
        return None


# For testing purposes - run this script directly to get a timestamp
# from the server.
if __name__ == "__main__":
    timestamp = get_timestamp()
    if timestamp:
        print(f"Current Timestamp: {timestamp}")
    else:
        print("Failed to retrieve timestamp.")

import os
import datetime
import threading
import thriftpy2 as thriftpy
from thriftpy2.rpc import make_server


SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 10000


# Load timestamp.thrift file
timestamp_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__), "timestamp.thrift"),
    module_name="timestamp_thrift"
)
service = timestamp_thrift.TimestampService


class TimestampHandler:

    def getCurrentTimestamp(self):
        """
        Returns the current timestamp in milliseconds since epoch.
        """
        # Get current UTC time
        utc_timestamp = datetime.datetime.utcnow()
        return str(utc_timestamp)


def start_server():
    handler = TimestampHandler()
    server = make_server(service, handler, SERVER_ADDRESS, SERVER_PORT)
    server.serve()


def run_server_in_thread():
    server_thread = threading.Thread(target=start_server, daemon=True)
    # Run thread as daemon so it will exit when Django stops
    server_thread.start()
    print(f"Thrift server running on {SERVER_ADDRESS}:{SERVER_PORT}")


# For testing purposes - run this script directly to start the server
if __name__ == "__main__":
    start_server()

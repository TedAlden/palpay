from django.apps import AppConfig
from .server import run_server_in_thread
from .client import get_timestamp


class TimestampConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'timestamp'

    def ready(self):
        # Start the Thrift server in a separate thread
        run_server_in_thread()

        # For testing purposes, call the client to get a timestamp when
        # the app is ready and print it in the console.
        print("Timestamp =", get_timestamp())

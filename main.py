import sys

from signal import signal, SIGINT
from server import WebServer


def shutdown_server(sig, unused):
    web_server.shutdown()
    sys.exit(1)


signal(SIGINT, shutdown_server)
web_server = WebServer(8081)
print("Use Ctrl+C to shut down server")
web_server.start()


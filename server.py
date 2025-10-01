#!/usr/bin/env python3

import os
import sys
import argparse
from http.server import HTTPServer

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from transaction_api import TransactionAPIHandler


class ModularAPIHandler(TransactionAPIHandler):    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


def run_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ModularAPIHandler)

    print(f"MoMo SMS API Server running on port {port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MoMo SMS API Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    
    args = parser.parse_args()
    run_server(args.port)

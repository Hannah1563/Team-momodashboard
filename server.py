#!/usr/bin/env python3

import os
import sys
import urllib
import argparse
from http.server import HTTPServer

# Add the api directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

from transaction_api import TransactionAPIHandler


class ModularAPIHandler(TransactionAPIHandler):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Route to transaction module
        if path.startswith('/transactions'):
            self._handle_transaction_routes(path, parsed_url)
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_POST(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Route to transaction module
        if path.startswith('/transactions'):
            self._handle_transaction_routes(path, parsed_url)
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_PUT(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Route to transaction module
        if path.startswith('/transactions'):
            self._handle_transaction_routes(path, parsed_url)
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_DELETE(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        # Route to transaction module
        if path.startswith('/transactions'):
            self._handle_transaction_routes(path, parsed_url)
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def _handle_transaction_routes(self, path, parsed_url):
        if path == '/transactions':
            self._handle_get_all_transactions()
        elif path.startswith('/transactions/'):
            transaction_id = self._get_transaction_id_from_path()
            if transaction_id:
                if self.command == 'GET':
                    self._handle_get_transaction(transaction_id)
                elif self.command == 'PUT':
                    self._handle_update_transaction(transaction_id)
                elif self.command == 'DELETE':
                    self._handle_delete_transaction(transaction_id)
                else:
                    self._send_error_response(405, "Method not allowed")
            else:
                self._send_error_response(400, "Invalid transaction ID format")
        else:
            self._send_error_response(404, "Endpoint not found")


def run_server(port: int = 8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, ModularAPIHandler)

    print(f"MoMo SMS Modular API Server running on port {port}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MoMo SMS Modular API Server')
    parser.add_argument('--port', type=int, default=8000, help='Port to run the server on (default: 8000)')
    
    args = parser.parse_args()
    run_server(args.port)

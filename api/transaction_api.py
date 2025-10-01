#!/usr/bin/env python3

import os
import sys
import json
import base64
import urllib.parse
from typing import Dict, Any, Optional, List
from http.server import BaseHTTPRequestHandler

# Add the dsa directory to the path to import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'dsa'))

from xml_parser import SMSDataParser  # pyright: ignore[reportMissingImports]
from search_algorithms import TransactionSearch  # pyright: ignore[reportMissingImports]


class TransactionAPIHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        # Load transaction data
        self.transactions = self._load_transaction_data()
        self.search_engine = TransactionSearch(self.transactions)
        super().__init__(*args, **kwargs)
    
    def _load_transaction_data(self) -> List[Dict[str, Any]]:
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            xml_file_path = os.path.join(project_root, 'data', 'raw', 'modified_sms_v2.xml')
            
            parser = SMSDataParser(xml_file_path)
            transactions = parser.parse_xml()
            
            if not transactions:
                print("Warning: No transactions loaded from XML file")
                return []
            
            print(f"Loaded {len(transactions)} transactions for API")
            return transactions
            
        except Exception as e:
            print(f"Error loading transaction data: {e}")
            return []
    
    def _authenticate(self) -> bool:
        auth_header = self.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Basic '):
            return False
        
        try:
            encoded_credentials = auth_header[6:]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':', 1)
            
            return username == 'admin' and password == 'password123'
            
        except Exception:
            return False
    
    def _send_response(self, status_code: int, data: Dict[str, Any]):   
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
        
        response_json = json.dumps(data, indent=2)
        self.wfile.write(response_json.encode('utf-8'))
    
    def _send_error_response(self, status_code: int, error_message: str, error_code: str = None):
        error_data = {
            "success": False,
            "error": {
                "code": error_code or f"HTTP_{status_code}",
                "message": error_message
            }
        }
        self._send_response(status_code, error_data)
    
    def _send_success_response(self, data: Any, message: str = None):
        response_data = {
            "success": True,
            "data": data
        }
        if message:
            response_data["message"] = message
        self._send_response(200, response_data)
    
    def _parse_json_body(self) -> Optional[Dict[str, Any]]:
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length == 0:
                return None
            
            body = self.rfile.read(content_length)
            return json.loads(body.decode('utf-8'))
        except Exception:
            return None
    
    def _get_transaction_id_from_path(self) -> Optional[int]:
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            path_parts = parsed_url.path.strip('/').split('/')
            if len(path_parts) >= 2 and path_parts[0] == 'transactions':
                return int(path_parts[1])
        except (ValueError, IndexError):
            pass
        return None
    
    def do_GET(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path == '/transactions':
            self._handle_get_all_transactions()
        elif path.startswith('/transactions/'):
            transaction_id = self._get_transaction_id_from_path()
            if transaction_id:
                self._handle_get_transaction(transaction_id)
            else:
                self._send_error_response(400, "Invalid transaction ID format")
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_POST(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        if self.path == '/transactions':
            self._handle_create_transaction()
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_PUT(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path.startswith('/transactions/'):
            transaction_id = self._get_transaction_id_from_path()
            if transaction_id:
                self._handle_update_transaction(transaction_id)
            else:
                self._send_error_response(400, "Invalid transaction ID format")
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def do_DELETE(self):
        if not self._authenticate():
            self._send_error_response(401, "Unauthorized. Please provide valid Basic Authentication credentials.")
            return
        
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path
        
        if path.startswith('/transactions/'):
            transaction_id = self._get_transaction_id_from_path()
            if transaction_id:
                self._handle_delete_transaction(transaction_id)
            else:
                self._send_error_response(400, "Invalid transaction ID format")
        else:
            self._send_error_response(404, "Endpoint not found")
    
    def _handle_get_all_transactions(self):
        try:
            parsed_url = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            
            # Filter by type if specified
            transaction_type = query_params.get('type', [None])[0]
            if transaction_type:
                filtered_transactions = [t for t in self.transactions if t.get('type') == transaction_type]
            else:
                filtered_transactions = self.transactions
            
            # Pagination
            page = int(query_params.get('page', [1])[0])
            per_page = int(query_params.get('per_page', [20])[0])
            
            start_idx = (page - 1) * per_page
            end_idx = start_idx + per_page
            
            paginated_transactions = filtered_transactions[start_idx:end_idx]
            
            response_data = {
                "transactions": paginated_transactions,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(filtered_transactions),
                    "total_pages": (len(filtered_transactions) + per_page - 1) // per_page
                }
            }
            
            self._send_success_response(response_data)
            
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_get_transaction(self, transaction_id: int):
        try:
            transaction = self.search_engine.dictionary_lookup_by_id(transaction_id)
            
            if transaction:
                self._send_success_response({"transaction": transaction})
            else:
                self._send_error_response(404, f"Transaction with ID {transaction_id} not found", "TRANSACTION_NOT_FOUND")
                
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_create_transaction(self):
        try:
            data = self._parse_json_body()
            
            if not data:
                self._send_error_response(400, "Request body must contain valid JSON")
                return
            
            # Validate required fields
            required_fields = ['type', 'amount', 'sender', 'receiver']
            for field in required_fields:
                if field not in data:
                    self._send_error_response(400, f"Missing required field: {field}")
                    return
            
            # Generate new transaction ID
            max_id = max([t['id'] for t in self.transactions]) if self.transactions else 0
            new_id = max_id + 1
            
            # Create new transaction
            new_transaction = {
                'id': new_id,
                'type': data['type'],
                'amount': float(data['amount']),
                'currency': data.get('currency', 'RWF'),
                'sender': data['sender'],
                'receiver': data['receiver'],
                'timestamp': data.get('timestamp', '2024-09-27T12:00:00Z'),
                'status': data.get('status', 'Completed'),
                'reference': data.get('reference', f'TXN{new_id:09d}'),
                'description': data.get('description', '')
            }
            
            # Add to transactions list
            self.transactions.append(new_transaction)
            
            # Update search engine
            self.search_engine = TransactionSearch(self.transactions)
            
            self._send_success_response({"transaction": new_transaction}, "Transaction created successfully")
            
        except ValueError as e:
            self._send_error_response(400, f"Invalid data format: {str(e)}")
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_update_transaction(self, transaction_id: int):
        try:
            transaction = self.search_engine.dictionary_lookup_by_id(transaction_id)
            
            if not transaction:
                self._send_error_response(404, f"Transaction with ID {transaction_id} not found", "TRANSACTION_NOT_FOUND")
                return
            
            data = self._parse_json_body()
            
            if not data:
                self._send_error_response(400, "Request body must contain valid JSON")
                return
            
            # Update transaction fields
            for field, value in data.items():
                if field in transaction:
                    if field == 'amount':
                        transaction[field] = float(value)
                    else:
                        transaction[field] = value
            
            # Update search engine
            self.search_engine = TransactionSearch(self.transactions)
            
            self._send_success_response({"transaction": transaction}, "Transaction updated successfully")
            
        except ValueError as e:
            self._send_error_response(400, f"Invalid data format: {str(e)}")
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")
    
    def _handle_delete_transaction(self, transaction_id: int):
        try:
            transaction = self.search_engine.dictionary_lookup_by_id(transaction_id)
            
            if not transaction:
                self._send_error_response(404, f"Transaction with ID {transaction_id} not found", "TRANSACTION_NOT_FOUND")
                return
            
            # Remove transaction from list
            self.transactions = [t for t in self.transactions if t['id'] != transaction_id]
            
            # Update search engine
            self.search_engine = TransactionSearch(self.transactions)
            
            self._send_success_response({"deleted_transaction": transaction}, "Transaction deleted successfully")
            
        except Exception as e:
            self._send_error_response(500, f"Internal server error: {str(e)}")
#!/usr/bin/env python3

import os
import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any


class SMSDataParser:
    def __init__(self, xml_file_path: str):
        self.xml_file_path = xml_file_path
        self.transactions = []
        
    def parse_xml(self) -> List[Dict[str, Any]]:

        try:
            # Parse the XML file
            tree = ET.parse(self.xml_file_path)
            root = tree.getroot()
            
            # Extract transaction data
            for transaction in root.findall('transaction'):
                transaction_data = self._extract_transaction_data(transaction)
                if transaction_data:
                    self.transactions.append(transaction_data)
            
            print(f"Successfully parsed {len(self.transactions)} transactions from XML")
            return self.transactions
            
        except ET.ParseError as e:
            print(f"XML parsing error: {e}")
            return []
        except FileNotFoundError:
            print(f"XML file not found: {self.xml_file_path}")
            return []
        except Exception as e:
            print(f"Unexpected error during parsing: {e}")
            return []
    
    def _extract_transaction_data(self, transaction_element) -> Dict[str, Any]:
        try:
            # Extract basic transaction information
            transaction_id = transaction_element.get('id')
            transaction_type = self._get_element_text(transaction_element, 'type')
            amount = self._get_element_text(transaction_element, 'amount')
            currency = self._get_element_text(transaction_element, 'currency')
            sender = self._get_element_text(transaction_element, 'sender')
            receiver = self._get_element_text(transaction_element, 'receiver')
            timestamp = self._get_element_text(transaction_element, 'timestamp')
            status = self._get_element_text(transaction_element, 'status')
            reference = self._get_element_text(transaction_element, 'reference')
            description = self._get_element_text(transaction_element, 'description')
            
            # Validate and convert data types
            transaction_data = {
                'id': int(transaction_id) if transaction_id else None,
                'type': transaction_type,
                'amount': float(amount) if amount else 0.0,
                'currency': currency or 'RWF',
                'sender': sender,
                'receiver': receiver,
                'timestamp': timestamp,
                'status': status,
                'reference': reference,
                'description': description
            }
            
            return transaction_data
            
        except (ValueError, TypeError) as e:
            print(f"Error extracting transaction data: {e}")
            return None
    
    def _get_element_text(self, parent_element, tag_name: str) -> str:

        element = parent_element.find(tag_name)
        return element.text if element is not None and element.text else ""
    
    def save_to_json(self, output_file_path: str) -> bool:

        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {len(self.transactions)} transactions to {output_file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def get_transactions(self) -> List[Dict[str, Any]]:

        return self.transactions
    
    def get_transaction_by_id(self, transaction_id: int) -> Dict[str, Any]:

        for transaction in self.transactions:
            if transaction.get('id') == transaction_id:
                return transaction
        return None
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:

        return [t for t in self.transactions if t.get('type') == transaction_type]
    
    def get_transactions_by_sender(self, sender_phone: str) -> List[Dict[str, Any]]:

        return [t for t in self.transactions if t.get('sender') == sender_phone]
    
    def get_transactions_by_receiver(self, receiver_phone: str) -> List[Dict[str, Any]]:

        return [t for t in self.transactions if t.get('receiver') == receiver_phone]


def main():

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    xml_file_path = os.path.join(project_root, 'data', 'raw', 'modified_sms_v2.xml')
    
    # Initialize parser
    parser = SMSDataParser(xml_file_path)
    
    # Parse XML
    transactions = parser.parse_xml()
    
    if transactions:
        print(f"\nParsed {len(transactions)} transactions:")
        print("-" * 50)
        
        # Display first few transactions
        for i, transaction in enumerate(transactions[:3]):
            print(f"Transaction {i+1}:")
            print(f"  ID: {transaction['id']}")
            print(f"  Type: {transaction['type']}")
            print(f"  Amount: {transaction['amount']} {transaction['currency']}")
            print(f"  Sender: {transaction['sender']}")
            print(f"  Receiver: {transaction['receiver']}")
            print(f"  Status: {transaction['status']}")
            print()
        
        # Save to JSON
        json_output_path = os.path.join(project_root, 'data', 'processed', 'transactions.json')
        os.makedirs(os.path.dirname(json_output_path), exist_ok=True)
        parser.save_to_json(json_output_path)
        
    else:
        print("No transactions were parsed from the XML file.")


if __name__ == "__main__":
    main()

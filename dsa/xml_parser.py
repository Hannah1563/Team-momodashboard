#!/usr/bin/env python3
"""
XML Parser Module for MoMo SMS Data Processing
Converts SMS records from XML format to JSON objects
"""

import xml.etree.ElementTree as ET
import json
from datetime import datetime
from typing import List, Dict, Any
import os


class SMSDataParser:
    """Parser for SMS transaction data in XML format"""
    
    def __init__(self, xml_file_path: str):
        """
        Initialize the parser with XML file path
        
        Args:
            xml_file_path (str): Path to the XML file containing SMS data
        """
        self.xml_file_path = xml_file_path
        self.transactions = []
        
    def parse_xml(self) -> List[Dict[str, Any]]:
        """
        Parse XML file and convert SMS records to JSON objects
        
        Returns:
            List[Dict[str, Any]]: List of transaction dictionaries
        """
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
        """
        Extract transaction data from XML element
        
        Args:
            transaction_element: XML element containing transaction data
            
        Returns:
            Dict[str, Any]: Transaction data dictionary
        """
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
        """
        Safely get text content from XML element
        
        Args:
            parent_element: Parent XML element
            tag_name (str): Name of the child element
            
        Returns:
            str: Text content or empty string if not found
        """
        element = parent_element.find(tag_name)
        return element.text if element is not None and element.text else ""
    
    def save_to_json(self, output_file_path: str) -> bool:
        """
        Save parsed transactions to JSON file
        
        Args:
            output_file_path (str): Path to output JSON file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(self.transactions, f, indent=2, ensure_ascii=False)
            
            print(f"Successfully saved {len(self.transactions)} transactions to {output_file_path}")
            return True
            
        except Exception as e:
            print(f"Error saving to JSON: {e}")
            return False
    
    def get_transactions(self) -> List[Dict[str, Any]]:
        """
        Get the parsed transactions
        
        Returns:
            List[Dict[str, Any]]: List of transaction dictionaries
        """
        return self.transactions
    
    def get_transaction_by_id(self, transaction_id: int) -> Dict[str, Any]:
        """
        Get a specific transaction by ID
        
        Args:
            transaction_id (int): ID of the transaction to retrieve
            
        Returns:
            Dict[str, Any]: Transaction data or None if not found
        """
        for transaction in self.transactions:
            if transaction.get('id') == transaction_id:
                return transaction
        return None
    
    def get_transactions_by_type(self, transaction_type: str) -> List[Dict[str, Any]]:
        """
        Get all transactions of a specific type
        
        Args:
            transaction_type (str): Type of transactions to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        return [t for t in self.transactions if t.get('type') == transaction_type]
    
    def get_transactions_by_sender(self, sender_phone: str) -> List[Dict[str, Any]]:
        """
        Get all transactions sent by a specific phone number
        
        Args:
            sender_phone (str): Phone number of the sender
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        return [t for t in self.transactions if t.get('sender') == sender_phone]
    
    def get_transactions_by_receiver(self, receiver_phone: str) -> List[Dict[str, Any]]:
        """
        Get all transactions received by a specific phone number
        
        Args:
            receiver_phone (str): Phone number of the receiver
            
        Returns:
            List[Dict[str, Any]]: List of matching transactions
        """
        return [t for t in self.transactions if t.get('receiver') == receiver_phone]


def main():
    """Main function to demonstrate XML parsing"""
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
        
        # Demonstrate search functionality
        print("Search Examples:")
        print("-" * 20)
        
        # Search by ID
        transaction_5 = parser.get_transaction_by_id(5)
        if transaction_5:
            print(f"Transaction 5: {transaction_5['type']} - {transaction_5['amount']} {transaction_5['currency']}")
        
        # Search by type
        transfer_transactions = parser.get_transactions_by_type('Transfer')
        print(f"Found {len(transfer_transactions)} Transfer transactions")
        
        # Search by sender
        sender_transactions = parser.get_transactions_by_sender('+250788123456')
        print(f"Found {len(sender_transactions)} transactions from +250788123456")
        
    else:
        print("No transactions were parsed from the XML file.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import time
import requests
from requests.auth import HTTPBasicAuth


class APITester:    
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.auth = HTTPBasicAuth('admin', 'password123')
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, message: str = ""):
        status = "PASS" if success else "FAIL"
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {message}")
    
    def test_server_connection(self):
        try:
            response = requests.get(f"{self.base_url}/transactions", auth=self.auth, timeout=5)
            self.log_test("Server Connection", True, f"Server responding (Status: {response.status_code})")
            return True
        except requests.exceptions.ConnectionError:
            self.log_test("Server Connection", False, "Server not running or unreachable")
            return False
        except Exception as e:
            self.log_test("Server Connection", False, f"Unexpected error: {str(e)}")
            return False
    
    def test_authentication_success(self):
        try:
            response = requests.get(f"{self.base_url}/transactions", auth=self.auth)
            success = response.status_code == 200
            self.log_test("Authentication Success", success, 
                         f"Status: {response.status_code}" if success else f"Unexpected status: {response.status_code}")
            return success
        except Exception as e:
            self.log_test("Authentication Success", False, f"Error: {str(e)}")
            return False
    
    def test_authentication_failure(self):
        try:
            # Test without authentication
            response = requests.get(f"{self.base_url}/transactions")
            success = response.status_code == 401
            self.log_test("Authentication Failure (No Auth)", success,
                         f"Status: {response.status_code}" if success else f"Expected 401, got {response.status_code}")
            
            # Test with wrong credentials
            wrong_auth = HTTPBasicAuth('wrong', 'credentials')
            response = requests.get(f"{self.base_url}/transactions", auth=wrong_auth)
            success = response.status_code == 401
            self.log_test("Authentication Failure (Wrong Creds)", success,
                         f"Status: {response.status_code}" if success else f"Expected 401, got {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Authentication Failure", False, f"Error: {str(e)}")
            return False
    
    def test_get_all_transactions(self):
        try:
            response = requests.get(f"{self.base_url}/transactions", auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_count = len(data.get('data', {}).get('transactions', []))
                self.log_test("GET All Transactions", True, f"Retrieved {transaction_count} transactions")
            else:
                self.log_test("GET All Transactions", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("GET All Transactions", False, f"Error: {str(e)}")
            return False
    
    def test_get_transaction_by_id(self):
        try:
            # Test with existing ID
            response = requests.get(f"{self.base_url}/transactions/1", auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_id = data.get('data', {}).get('transaction', {}).get('id')
                self.log_test("GET Transaction by ID (Valid)", True, f"Retrieved transaction {transaction_id}")
            else:
                self.log_test("GET Transaction by ID (Valid)", False, f"Status: {response.status_code}")
            
            # Test with non-existing ID
            response = requests.get(f"{self.base_url}/transactions/99999", auth=self.auth)
            success = response.status_code == 404
            self.log_test("GET Transaction by ID (Invalid)", success,
                         f"Status: {response.status_code}" if success else f"Expected 404, got {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("GET Transaction by ID", False, f"Error: {str(e)}")
            return False
    
    def test_create_transaction(self):
        try:
            new_transaction = {
                "type": "Transfer",
                "amount": 15000,
                "sender": "+250788123456",
                "receiver": "+250789234567",
                "currency": "RWF",
                "description": "API test transaction"
            }
            
            response = requests.post(f"{self.base_url}/transactions", 
                                  json=new_transaction, auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transaction_id = data.get('data', {}).get('transaction', {}).get('id')
                self.log_test("POST Create Transaction", True, f"Created transaction {transaction_id}")
                return transaction_id
            else:
                self.log_test("POST Create Transaction", False, f"Status: {response.status_code}")
                return None
                
        except Exception as e:
            self.log_test("POST Create Transaction", False, f"Error: {str(e)}")
            return None
    
    def test_update_transaction(self, transaction_id):
        if not transaction_id:
            self.log_test("PUT Update Transaction", False, "No transaction ID provided")
            return False
        
        try:
            update_data = {
                "amount": 20000,
                "description": "Updated via API test"
            }
            
            response = requests.put(f"{self.base_url}/transactions/{transaction_id}", 
                                 json=update_data, auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                updated_amount = data.get('data', {}).get('transaction', {}).get('amount')
                self.log_test("PUT Update Transaction", True, f"Updated transaction {transaction_id} (amount: {updated_amount})")
            else:
                self.log_test("PUT Update Transaction", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("PUT Update Transaction", False, f"Error: {str(e)}")
            return False
    
    def test_delete_transaction(self, transaction_id):
        if not transaction_id:
            self.log_test("DELETE Transaction", False, "No transaction ID provided")
            return False
        
        try:
            response = requests.delete(f"{self.base_url}/transactions/{transaction_id}", auth=self.auth)
            success = response.status_code == 200
            
            if success:
                self.log_test("DELETE Transaction", True, f"Deleted transaction {transaction_id}")
            else:
                self.log_test("DELETE Transaction", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("DELETE Transaction", False, f"Error: {str(e)}")
            return False
    
    def test_query_parameters(self):
        try:
            # Test type filtering
            response = requests.get(f"{self.base_url}/transactions?type=Transfer", auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                transactions = data.get('data', {}).get('transactions', [])
                transfer_count = len(transactions)
                self.log_test("Query Parameters (Type Filter)", True, f"Found {transfer_count} Transfer transactions")
            else:
                self.log_test("Query Parameters (Type Filter)", False, f"Status: {response.status_code}")
            
            # Test pagination
            response = requests.get(f"{self.base_url}/transactions?page=1&per_page=5", auth=self.auth)
            success = response.status_code == 200
            
            if success:
                data = response.json()
                pagination = data.get('data', {}).get('pagination', {})
                page = pagination.get('page', 0)
                per_page = pagination.get('per_page', 0)
                self.log_test("Query Parameters (Pagination)", True, f"Page {page}, {per_page} per page")
            else:
                self.log_test("Query Parameters (Pagination)", False, f"Status: {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Query Parameters", False, f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        try:
            # Test invalid JSON
            response = requests.post(f"{self.base_url}/transactions", 
                                  data="invalid json", 
                                  headers={"Content-Type": "application/json"},
                                  auth=self.auth)
            success = response.status_code == 400
            self.log_test("Error Handling (Invalid JSON)", success,
                         f"Status: {response.status_code}" if success else f"Expected 400, got {response.status_code}")
            
            # Test missing required fields
            incomplete_transaction = {
                "type": "Transfer",
                "amount": 1000
                # Missing sender and receiver
            }
            response = requests.post(f"{self.base_url}/transactions", 
                                  json=incomplete_transaction, auth=self.auth)
            success = response.status_code == 400
            self.log_test("Error Handling (Missing Fields)", success,
                         f"Status: {response.status_code}" if success else f"Expected 400, got {response.status_code}")
            
            return success
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        print("=" * 60)
        print("MoMo SMS Transaction API Test Suite")
        print("=" * 60)
        print()
        
        # Check server connection first
        if not self.test_server_connection():
            print("Server is not running. Please start the API server first.")
            print("Run: python api/transaction_api.py")
            return
        
        print()
        
        # Authentication tests
        print("Authentication Tests:")
        print("-" * 30)
        self.test_authentication_success()
        self.test_authentication_failure()
        print()
        
        # CRUD operation tests
        print("CRUD Operation Tests:")
        print("-" * 30)
        self.test_get_all_transactions()
        self.test_get_transaction_by_id()
        
        # Create a transaction for update/delete tests
        created_id = self.test_create_transaction()
        if created_id:
            self.test_update_transaction(created_id)
            self.test_delete_transaction(created_id)
        
        print()
        
        # Summary
        self.print_test_summary()
    
    def print_test_summary(self):
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        print()
        
        if failed_tests > 0:
            print("Failed Tests:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['message']}")
            print()
        
        print("All tests completed!")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='Test MoMo SMS Transaction API')
    parser.add_argument('--url', default='http://localhost:8000', 
                       help='API base URL (default: http://localhost:8000)')
    
    args = parser.parse_args()
    
    tester = APITester(args.url)
    tester.run_all_tests()


if __name__ == "__main__":
    main()

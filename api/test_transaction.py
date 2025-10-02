#!/usr/bin/env python3

import requests
from requests.auth import HTTPBasicAuth

def test_api():
    base_url = "http://localhost:8000"
    auth = HTTPBasicAuth('admin', 'password123')
    
    print("API Tests")
    print("=" * 30)
    
    passed = 0
    failed = 0
    
    # GET /transactions tests
    print("\nGET /transactions Tests:")
    try:
        response = requests.get(f"{base_url}/transactions", auth=auth)
        if response.status_code == 200:
            print("✅ GET all transactions")
            passed += 1
        else:
            print(f"❌ GET all transactions - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET all transactions - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions?type=Transfer", auth=auth)
        if response.status_code == 200:
            print("✅ GET transactions with filter")
            passed += 1
        else:
            print(f"❌ GET transactions with filter - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET transactions with filter - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions?page=1&per_page=5", auth=auth)
        if response.status_code == 200:
            print("✅ GET transactions with pagination")
            passed += 1
        else:
            print(f"❌ GET transactions with pagination - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET transactions with pagination - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions", auth=HTTPBasicAuth('wrong', 'password'))
        if response.status_code == 401:
            print("✅ GET transactions without auth")
            passed += 1
        else:
            print(f"❌ GET transactions without auth - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET transactions without auth - Error: {e}")
        failed += 1
    
    # GET /transactions/{id} tests
    print("\nGET /transactions/{id} Tests:")
    try:
        response = requests.get(f"{base_url}/transactions/1", auth=auth)
        if response.status_code == 200:
            print("✅ GET specific transaction")
            passed += 1
        else:
            print(f"❌ GET specific transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET specific transaction - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions/99999", auth=auth)
        if response.status_code == 404:
            print("✅ GET non-existent transaction")
            passed += 1
        else:
            print(f"❌ GET non-existent transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET non-existent transaction - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions/abc", auth=auth)
        if response.status_code == 400:
            print("✅ GET transaction with invalid ID")
            passed += 1
        else:
            print(f"❌ GET transaction with invalid ID - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET transaction with invalid ID - Error: {e}")
        failed += 1
    
    try:
        response = requests.get(f"{base_url}/transactions/0", auth=auth)
        if response.status_code in [400, 404]:
            print("✅ GET transaction with edge case ID")
            passed += 1
        else:
            print(f"❌ GET transaction with edge case ID - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ GET transaction with edge case ID - Error: {e}")
        failed += 1
    
    # POST /transactions tests
    print("\nPOST /transactions Tests:")
    try:
        data = {"type": "Transfer", "amount": 1000, "sender": "+250788123456", "receiver": "+250789234567"}
        response = requests.post(f"{base_url}/transactions", json=data, auth=auth)
        if response.status_code == 200:
            print("✅ POST valid transaction")
            passed += 1
        else:
            print(f"❌ POST valid transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ POST valid transaction - Error: {e}")
        failed += 1
    
    try:
        data = {"type": "Transfer", "amount": 1000}  # Missing sender and receiver
        response = requests.post(f"{base_url}/transactions", json=data, auth=auth)
        if response.status_code == 400:
            print("✅ POST transaction missing fields")
            passed += 1
        else:
            print(f"❌ POST transaction missing fields - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ POST transaction missing fields - Error: {e}")
        failed += 1
    
    try:
        data = {"type": "Transfer", "amount": "invalid", "sender": "+250788123456", "receiver": "+250789234567"}
        response = requests.post(f"{base_url}/transactions", json=data, auth=auth)
        if response.status_code in [400, 500]:
            print("✅ POST transaction with invalid data")
            passed += 1
        else:
            print(f"❌ POST transaction with invalid data - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ POST transaction with invalid data - Error: {e}")
        failed += 1
    
    try:
        response = requests.post(f"{base_url}/transactions", data="invalid json", headers={"Content-Type": "application/json"}, auth=auth)
        if response.status_code in [400, 500]:
            print("✅ POST transaction with invalid JSON")
            passed += 1
        else:
            print(f"❌ POST transaction with invalid JSON - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ POST transaction with invalid JSON - Error: {e}")
        failed += 1
    
    # PUT /transactions/{id} tests
    print("\nPUT /transactions/{id} Tests:")
    try:
        data = {"amount": 2000}
        response = requests.put(f"{base_url}/transactions/1", json=data, auth=auth)
        if response.status_code == 200:
            print("✅ PUT update transaction")
            passed += 1
        else:
            print(f"❌ PUT update transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ PUT update transaction - Error: {e}")
        failed += 1
    
    try:
        data = {"amount": 2000}
        response = requests.put(f"{base_url}/transactions/99999", json=data, auth=auth)
        if response.status_code == 404:
            print("✅ PUT update non-existent transaction")
            passed += 1
        else:
            print(f"❌ PUT update non-existent transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ PUT update non-existent transaction - Error: {e}")
        failed += 1
    
    try:
        data = {"amount": "invalid"}
        response = requests.put(f"{base_url}/transactions/1", json=data, auth=auth)
        if response.status_code in [400, 500]:
            print("✅ PUT update with invalid data")
            passed += 1
        else:
            print(f"❌ PUT update with invalid data - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ PUT update with invalid data - Error: {e}")
        failed += 1
    
    try:
        data = {}
        response = requests.put(f"{base_url}/transactions/1", json=data, auth=auth)
        if response.status_code == 200:
            print("✅ PUT update with empty data")
            passed += 1
        else:
            print(f"❌ PUT update with empty data - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ PUT update with empty data - Error: {e}")
        failed += 1
    
    # DELETE /transactions/{id} tests
    print("\nDELETE /transactions/{id} Tests:")
    try:
        response = requests.delete(f"{base_url}/transactions/99999", auth=auth)
        if response.status_code == 404:
            print("✅ DELETE non-existent transaction")
            passed += 1
        else:
            print(f"❌ DELETE non-existent transaction - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ DELETE non-existent transaction - Error: {e}")
        failed += 1
    
    try:
        response = requests.delete(f"{base_url}/transactions/abc", auth=auth)
        if response.status_code == 400:
            print("✅ DELETE transaction with invalid ID")
            passed += 1
        else:
            print(f"❌ DELETE transaction with invalid ID - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ DELETE transaction with invalid ID - Error: {e}")
        failed += 1
    
    try:
        # First create a transaction to delete
        data = {"type": "Transfer", "amount": 1000, "sender": "+250788123456", "receiver": "+250789234567"}
        create_response = requests.post(f"{base_url}/transactions", json=data, auth=auth)
        if create_response.status_code == 200:
            transaction_id = create_response.json()['data']['transaction']['id']
            delete_response = requests.delete(f"{base_url}/transactions/{transaction_id}", auth=auth)
            if delete_response.status_code == 200:
                print("✅ DELETE valid transaction")
                passed += 1
            else:
                print(f"❌ DELETE valid transaction - Status: {delete_response.status_code}")
                failed += 1
        else:
            print("❌ DELETE valid transaction - Failed to create test transaction")
            failed += 1
    except Exception as e:
        print(f"❌ DELETE valid transaction - Error: {e}")
        failed += 1
    
    try:
        response = requests.delete(f"{base_url}/transactions/0", auth=auth)
        if response.status_code in [400, 404]:
            print("✅ DELETE transaction with edge case ID")
            passed += 1
        else:
            print(f"❌ DELETE transaction with edge case ID - Status: {response.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ DELETE transaction with edge case ID - Error: {e}")
        failed += 1
    
    print("\n" + "=" * 30)
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")

if __name__ == "__main__":
    test_api()

# MoMo SMS Transaction API Documentation

## Overview

The MoMo SMS Transaction API provides RESTful endpoints for managing mobile money transaction data. The API supports full CRUD operations with Basic Authentication security.

**Base URL:** `http://localhost:8000`  
**Authentication:** Basic Authentication (username: `admin`, password: `password123`)

## Authentication

All endpoints require Basic Authentication. Include the `Authorization` header with base64-encoded credentials:

```
Authorization: Basic YWRtaW46cGFzc3dvcmQxMjM=
```

### Why Basic Auth is Weak

Basic Authentication has several security limitations:

1. **Credentials in Plain Text**: Credentials are base64-encoded (not encrypted) and can be easily decoded
2. **No Session Management**: Each request requires credentials, increasing exposure risk
3. **No Token Expiration**: Credentials remain valid until changed
4. **Vulnerable to Replay Attacks**: Intercepted credentials can be reused
5. **No Multi-Factor Authentication**: Single point of failure

### Stronger Alternatives

For production systems, consider these more secure alternatives:

1. **JWT (JSON Web Tokens)**: Stateless tokens with expiration and digital signatures
2. **OAuth 2.0**: Industry-standard authorization framework with scopes and refresh tokens
3. **API Keys**: Unique keys with rotation capabilities
4. **Multi-Factor Authentication**: Additional security layers

## Endpoints

### 1. List All Transactions

**GET** `/transactions`

Retrieve all transactions with optional filtering and pagination.

#### Query Parameters

| Parameter  | Type    | Default | Description                                                   |
| ---------- | ------- | ------- | ------------------------------------------------------------- |
| `type`     | string  | -       | Filter by transaction type (Transfer, Payment, Deposit, etc.) |
| `page`     | integer | 1       | Page number for pagination                                    |
| `per_page` | integer | 20      | Number of transactions per page                               |

#### Request Example

```bash
curl -u admin:password123 "http://localhost:8000/transactions?type=Transfer&page=1&per_page=10"
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "transactions": [
      {
        "id": 1,
        "type": "Transfer",
        "amount": 5000.0,
        "currency": "RWF",
        "sender": "+250788123456",
        "receiver": "+250789234567",
        "timestamp": "2024-09-15T10:30:00Z",
        "status": "Completed",
        "reference": "TXN001234567",
        "description": "Payment for lunch"
      }
    ],
    "pagination": {
      "page": 1,
      "per_page": 10,
      "total": 25,
      "total_pages": 3
    }
  }
}
```

### 2. Get Specific Transaction

**GET** `/transactions/{id}`

Retrieve a specific transaction by its ID.

#### Path Parameters

| Parameter | Type    | Required | Description    |
| --------- | ------- | -------- | -------------- |
| `id`      | integer | Yes      | Transaction ID |

#### Request Example

```bash
curl -u admin:password123 "http://localhost:8000/transactions/1"
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "transaction": {
      "id": 1,
      "type": "Transfer",
      "amount": 5000.0,
      "currency": "RWF",
      "sender": "+250788123456",
      "receiver": "+250789234567",
      "timestamp": "2024-09-15T10:30:00Z",
      "status": "Completed",
      "reference": "TXN001234567",
      "description": "Payment for lunch"
    }
  }
}
```

#### Error Response (Transaction Not Found)

```json
{
  "success": false,
  "error": {
    "code": "TRANSACTION_NOT_FOUND",
    "message": "Transaction with ID 999 not found"
  }
}
```

### 3. Create New Transaction

**POST** `/transactions`

Create a new transaction record.

#### Request Body

| Field         | Type   | Required | Description                                         |
| ------------- | ------ | -------- | --------------------------------------------------- |
| `type`        | string | Yes      | Transaction type (Transfer, Payment, Deposit, etc.) |
| `amount`      | number | Yes      | Transaction amount                                  |
| `sender`      | string | Yes      | Sender phone number                                 |
| `receiver`    | string | Yes      | Receiver phone number                               |
| `currency`    | string | No       | Currency code (default: RWF)                        |
| `timestamp`   | string | No       | Transaction timestamp (ISO 8601)                    |
| `status`      | string | No       | Transaction status (default: Completed)             |
| `reference`   | string | No       | Transaction reference number                        |
| `description` | string | No       | Transaction description                             |

#### Request Example

```bash
curl -u admin:password123 -X POST "http://localhost:8000/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Transfer",
    "amount": 10000,
    "sender": "+250788123456",
    "receiver": "+250789234567",
    "currency": "RWF",
    "description": "Test transfer"
  }'
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "transaction": {
      "id": 26,
      "type": "Transfer",
      "amount": 10000.0,
      "currency": "RWF",
      "sender": "+250788123456",
      "receiver": "+250789234567",
      "timestamp": "2024-09-27T12:00:00Z",
      "status": "Completed",
      "reference": "TXN000000026",
      "description": "Test transfer"
    }
  },
  "message": "Transaction created successfully"
}
```

### 4. Update Existing Transaction

**PUT** `/transactions/{id}`

Update an existing transaction record.

#### Path Parameters

| Parameter | Type    | Required | Description              |
| --------- | ------- | -------- | ------------------------ |
| `id`      | integer | Yes      | Transaction ID to update |

#### Request Body

Any fields to update (all fields optional except `id`):

| Field         | Type   | Description                      |
| ------------- | ------ | -------------------------------- |
| `type`        | string | Transaction type                 |
| `amount`      | number | Transaction amount               |
| `sender`      | string | Sender phone number              |
| `receiver`    | string | Receiver phone number            |
| `currency`    | string | Currency code                    |
| `timestamp`   | string | Transaction timestamp (ISO 8601) |
| `status`      | string | Transaction status               |
| `reference`   | string | Transaction reference number     |
| `description` | string | Transaction description          |

#### Request Example

```bash
curl -u admin:password123 -X PUT "http://localhost:8000/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 7500,
    "description": "Updated lunch payment"
  }'
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "transaction": {
      "id": 1,
      "type": "Transfer",
      "amount": 7500.0,
      "currency": "RWF",
      "sender": "+250788123456",
      "receiver": "+250789234567",
      "timestamp": "2024-09-15T10:30:00Z",
      "status": "Completed",
      "reference": "TXN001234567",
      "description": "Updated lunch payment"
    }
  },
  "message": "Transaction updated successfully"
}
```

### 5. Delete Transaction

**DELETE** `/transactions/{id}`

Delete a transaction record.

#### Path Parameters

| Parameter | Type    | Required | Description              |
| --------- | ------- | -------- | ------------------------ |
| `id`      | integer | Yes      | Transaction ID to delete |

#### Request Example

```bash
curl -u admin:password123 -X DELETE "http://localhost:8000/transactions/1"
```

#### Response Example

```json
{
  "success": true,
  "data": {
    "deleted_transaction": {
      "id": 1,
      "type": "Transfer",
      "amount": 5000.0,
      "currency": "RWF",
      "sender": "+250788123456",
      "receiver": "+250789234567",
      "timestamp": "2024-09-15T10:30:00Z",
      "status": "Completed",
      "reference": "TXN001234567",
      "description": "Payment for lunch"
    }
  },
  "message": "Transaction deleted successfully"
}
```

## Error Codes

| Code                    | HTTP Status | Description                                                     |
| ----------------------- | ----------- | --------------------------------------------------------------- |
| `HTTP_400`              | 400         | Bad Request - Invalid request format or missing required fields |
| `HTTP_401`              | 401         | Unauthorized - Invalid or missing authentication credentials    |
| `HTTP_404`              | 404         | Not Found - Endpoint or resource not found                      |
| `HTTP_500`              | 500         | Internal Server Error - Server-side error                       |
| `TRANSACTION_NOT_FOUND` | 404         | Transaction with specified ID not found                         |

## Data Structures & Algorithms Integration

The API integrates efficient search algorithms for optimal performance:

### Search Algorithms Implemented

1. **Linear Search (O(n))**: Sequential scan through transaction list
2. **Dictionary Lookup (O(1))**: Hash table-based ID lookup
3. **Binary Search (O(log n))**: Sorted data search for amount-based queries

### Performance Comparison

For 25 transactions with 100 test iterations:

- **Dictionary Lookup**: ~0.000001 seconds average
- **Binary Search**: ~0.000002 seconds average
- **Linear Search**: ~0.000005 seconds average

**Why Dictionary Lookup is Faster:**

1. **Constant Time Complexity**: O(1) vs O(n) for linear search
2. **Hash Table Optimization**: Direct key-to-value mapping
3. **No Sequential Scanning**: Immediate access to target data
4. **Memory Efficiency**: Pre-computed index structure

### Alternative Data Structures

For even better performance, consider:

1. **B-Trees**: Efficient for range queries and large datasets
2. **Red-Black Trees**: Self-balancing binary search trees
3. **Skip Lists**: Probabilistic data structure with O(log n) operations
4. **Trie**: For prefix-based searches on phone numbers

## Testing Examples

### Using curl

```bash
# List all transactions
curl -u admin:password123 "http://localhost:8000/transactions"

# Get specific transaction
curl -u admin:password123 "http://localhost:8000/transactions/1"

# Create new transaction
curl -u admin:password123 -X POST "http://localhost:8000/transactions" \
  -H "Content-Type: application/json" \
  -d '{"type": "Transfer", "amount": 5000, "sender": "+250788123456", "receiver": "+250789234567"}'

# Update transaction
curl -u admin:password123 -X PUT "http://localhost:8000/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{"amount": 7500}'

# Delete transaction
curl -u admin:password123 -X DELETE "http://localhost:8000/transactions/1"
```

### Using Python requests

```python
import requests
from requests.auth import HTTPBasicAuth

base_url = "http://localhost:8000"
auth = HTTPBasicAuth('admin', 'password123')

# List transactions
response = requests.get(f"{base_url}/transactions", auth=auth)
print(response.json())

# Create transaction
new_transaction = {
    "type": "Transfer",
    "amount": 10000,
    "sender": "+250788123456",
    "receiver": "+250789234567",
    "description": "API test transaction"
}
response = requests.post(f"{base_url}/transactions", json=new_transaction, auth=auth)
print(response.json())
```

## Rate Limiting

Currently, no rate limiting is implemented. For production deployment, consider:

1. **Request Rate Limiting**: Limit requests per IP/user
2. **Concurrent Connection Limits**: Prevent resource exhaustion
3. **API Key Quotas**: Usage-based restrictions

## CORS Support

The API includes CORS headers for cross-origin requests:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Content-Type, Authorization`

## Data Validation

The API performs basic validation:

1. **Required Fields**: Ensures all mandatory fields are present
2. **Data Types**: Validates numeric and string formats
3. **ID Format**: Ensures transaction IDs are valid integers
4. **JSON Format**: Validates request body structure

## Security Considerations

1. **HTTPS**: Use HTTPS in production to encrypt data in transit
2. **Input Sanitization**: Validate and sanitize all input data
3. **SQL Injection**: Use parameterized queries (not applicable to current implementation)
4. **XSS Protection**: Sanitize output data
5. **Authentication**: Implement proper session management
6. **Authorization**: Add role-based access control

## Monitoring and Logging

Consider implementing:

1. **Request Logging**: Log all API requests and responses
2. **Error Tracking**: Monitor and alert on API errors
3. **Performance Metrics**: Track response times and throughput
4. **Usage Analytics**: Monitor API usage patterns

## Future Enhancements

1. **Database Integration**: Replace in-memory storage with persistent database
2. **Advanced Filtering**: Add more sophisticated query capabilities
3. **Bulk Operations**: Support batch create/update/delete operations
4. **Real-time Updates**: WebSocket support for live data updates
5. **API Versioning**: Support multiple API versions
6. **GraphQL**: Alternative query language for flexible data retrieval

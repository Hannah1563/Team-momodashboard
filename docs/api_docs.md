# MoMo SMS Transaction API Documentation

## Overview

The MoMo SMS Transaction API provides RESTful endpoints for managing mobile money transaction data. The API supports full CRUD operations with Basic Authentication.

**Base URL:** `http://localhost:8000`  
**Authentication:** Basic Authentication (username: `admin`, password: `password123`)

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

# MoMo SMS Data Analytics Platform - REST API Implementation

## Team Information

**Team Name:** Team 7

**Project Description:**
An enterprise-level full-stack application designed to process MoMo SMS data in XML format, clean and categorize transactions, store data in a relational database, and provide a comprehensive REST API with CRUD operations, authentication, and data structures & algorithms integration.

**Team Members:**

- TUYISHIMIRE Ishimwe Hannah
- BYIRINGIRO Saad
- BIENVENUE Cedric

## Project Overview

This application processes Mobile Money (MoMo) transaction data from SMS notifications in XML format, performing ETL operations to clean, normalize, and categorize the data. The REST API provides secure access to transaction data with full CRUD operations, Basic Authentication, and efficient search algorithms demonstrating data structures & algorithms concepts.

## System Architecture

[**Architecture Diagram**](https://drive.google.com/file/d/1eU6X-h50mTTEokCH-wUGPPrrBe-h7zKN/view?usp=sharing)

## Project Structure

```
.
├── README.md                         # Setup, run, overview
├── requirements.txt                  # Python dependencies
├── data/
│   ├── raw/                          # XML input data
│   │   └── modified_sms_v2.xml       # Sample SMS transaction data
│   └── processed/                    # Processed JSON outputs
├── api/                              # REST API implementation
│   ├── transaction_api.py            # Main API server with CRUD endpoints
│   └── test_api.py                   # API testing suite
├── dsa/                              # Data Structures & Algorithms
│   ├── xml_parser.py                 # XML parsing and JSON conversion
│   ├── search_algorithms.py          # Search algorithms implementation
│   └── test_dsa.py                   # DSA testing and performance analysis
├── docs/                             # Documentation
│   ├── api_docs.md                   # Comprehensive API documentation
│   ├── data_dictionary.md            # Database schema documentation
│   ├── design_rationale.md            # Design decisions and rationale
│   └── erd_diagram.png               # Entity relationship diagram
├── database/                         # Database schema
│   └── database_setup.sql             # MySQL database setup with sample data
├── examples/                         # Example data and schemas
│   └── json_schemas.json             # JSON schema examples
└── screenshots/                      # API testing screenshots (to be added)
```

## Prerequisites

- Python 3.8+
- Modern web browser (for testing)
- curl or Postman (for API testing)

## Features

### Core Functionality

- **XML Data Processing:** Parse and validate MoMo SMS data from XML files
- **REST API:** Full CRUD operations with Basic Authentication
- **Data Structures & Algorithms:** Efficient search algorithms with performance analysis
- **JSON Conversion:** Convert XML SMS records to JSON objects
- **Error Handling:** Comprehensive error responses and validation

### API Endpoints

- **GET /transactions** - List all transactions with filtering and pagination
- **GET /transactions/{id}** - Retrieve specific transaction by ID
- **POST /transactions** - Create new transaction record
- **PUT /transactions/{id}** - Update existing transaction
- **DELETE /transactions/{id}** - Delete transaction record

### Security Features

- **Basic Authentication:** Username/password protection for all endpoints
- **Input Validation:** Comprehensive data validation and sanitization
- **CORS Support:** Cross-origin request handling
- **Error Responses:** Standardized error codes and messages

### DSA Integration

- **Linear Search:** O(n) sequential search algorithm
- **Dictionary Lookup:** O(1) hash table-based search
- **Binary Search:** O(log n) sorted data search
- **Performance Analysis:** Comparative timing and efficiency analysis

## Scrum Board

**Project Management:** [Trello Board](https://trello.com/invite/b/68be95de19b85650e16f8e5a/ATTI35a0f9a81f8e1e87b1503d0cf8cb26b7A96AEAA4/my-trello-board)

## Database Design

### Database Schema

Our MoMo SMS data processing system uses a normalized MySQL database design with four core entities:

#### Core Tables:

1. **Users** - Customer information with phone numbers and contact details
2. **Transactions** - Main transaction records with amounts, timestamps, and status
3. **Transaction_Categories** - Transaction type definitions (Transfer, Payment, etc.)
4. **System_Logs** - Audit trail and system monitoring logs

### Database Features:

- **Referential Integrity:** Foreign key constraints ensure data consistency
- **Performance Optimization:** Strategic indexes on frequently queried fields
- **Data Validation:** CHECK constraints for phone numbers, email formats, and business rules
- **Audit Trail:** Comprehensive logging for compliance and debugging
- **Scalability:** Normalized design supports growth and additional transaction types

### Sample Data:

The database includes sample data with:

- 8 sample users with Rwandan phone numbers
- 8 transaction categories covering all major MoMo operations
- 8 sample transactions with realistic amounts and scenarios
- 12 system log entries demonstrating various event types

### JSON Data Modeling:

Complete JSON schemas are provided for:

- Individual entity representations
- Complex nested objects with related data
- API response formats
- Analytics dashboard data structures
- SQL-to-JSON mapping documentation

### Files:

- `database/database_setup.sql` - Complete database schema with sample data
- `examples/json_schemas.json` - JSON representations and API formats
- `docs/data_dictionary.md` - Detailed table and column documentation
- `docs/design_rationale.md` - Database design decisions and justifications
- `docs/erd_diagram.png` - Visual entity relationship diagram

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Team7-Momo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the API Server

```bash
python api/transaction_api.py
```

The API will start on `http://localhost:8000`

### 4. Test the API

```bash
# Test with curl
curl -u admin:password123 http://localhost:8000/transactions

# Or run the test suite
python api/test_api.py
```

### 5. Test DSA Module

```bash
python dsa/test_dsa.py
```

## Detailed Setup Instructions

### Environment Setup

1. Ensure Python 3.8+ is installed
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Components

#### 1. XML Parser

```bash
python dsa/xml_parser.py
```

This will parse the sample XML file and demonstrate JSON conversion.

#### 2. Search Algorithms

```bash
python dsa/search_algorithms.py
```

This will run performance analysis comparing different search algorithms.

#### 3. REST API Server

```bash
python api/transaction_api.py --port 8000
```

Options:

- `--port`: Specify port number (default: 8000)

#### 4. API Testing

```bash
python api/test_api.py --url http://localhost:8000
```

This will run comprehensive API tests including authentication, CRUD operations, and error handling.

## API Usage Examples

### Authentication

All API requests require Basic Authentication:

- Username: `admin`
- Password: `password123`

### Basic Operations

#### List All Transactions

```bash
curl -u admin:password123 "http://localhost:8000/transactions"
```

#### Get Specific Transaction

```bash
curl -u admin:password123 "http://localhost:8000/transactions/1"
```

#### Create New Transaction

```bash
curl -u admin:password123 -X POST "http://localhost:8000/transactions" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Transfer",
    "amount": 10000,
    "sender": "+250788123456",
    "receiver": "+250789234567",
    "description": "Test transaction"
  }'
```

#### Update Transaction

```bash
curl -u admin:password123 -X PUT "http://localhost:8000/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{"amount": 7500}'
```

#### Delete Transaction

```bash
curl -u admin:password123 -X DELETE "http://localhost:8000/transactions/1"
```

### Query Parameters

#### Filter by Type

```bash
curl -u admin:password123 "http://localhost:8000/transactions?type=Transfer"
```

#### Pagination

```bash
curl -u admin:password123 "http://localhost:8000/transactions?page=1&per_page=10"
```

## Data Structures & Algorithms

### Performance Analysis Results

For 25 transactions with 100 test iterations:

| Algorithm         | Average Time | Time Complexity | Use Case                 |
| ----------------- | ------------ | --------------- | ------------------------ |
| Dictionary Lookup | ~0.000001s   | O(1)            | ID-based searches        |
| Binary Search     | ~0.000002s   | O(log n)        | Sorted data searches     |
| Linear Search     | ~0.000005s   | O(n)            | Simple sequential search |

### Why Dictionary Lookup is Faster

1. **Constant Time Complexity**: O(1) vs O(n) for linear search
2. **Hash Table Optimization**: Direct key-to-value mapping
3. **No Sequential Scanning**: Immediate access to target data
4. **Memory Efficiency**: Pre-computed index structure

## Testing & Validation

### API Testing

The project includes comprehensive testing for all API endpoints:

#### Test Coverage

- ✅ Authentication (success and failure scenarios)
- ✅ CRUD Operations (Create, Read, Update, Delete)
- ✅ Query Parameters (filtering, pagination)
- ✅ Error Handling (invalid data, missing fields)
- ✅ Response Format Validation

#### Running Tests

```bash
# Run API test suite
python api/test_api.py

# Run DSA performance tests
python dsa/test_dsa.py

# Test XML parsing
python dsa/xml_parser.py
```

#### Test Results Example

```
============================================================
MoMo SMS Transaction API Test Suite
============================================================

✅ PASS Server Connection: Server responding (Status: 200)
✅ PASS Authentication Success: Status: 200
✅ PASS Authentication Failure (No Auth): Status: 401
✅ PASS Authentication Failure (Wrong Creds): Status: 401
✅ PASS GET All Transactions: Retrieved 25 transactions
✅ PASS GET Transaction by ID (Valid): Retrieved transaction 1
✅ PASS GET Transaction by ID (Invalid): Status: 404
✅ PASS POST Create Transaction: Created transaction 26
✅ PASS PUT Update Transaction: Updated transaction 26 (amount: 20000)
✅ PASS DELETE Transaction: Deleted transaction 26
✅ PASS Query Parameters (Type Filter): Found 8 Transfer transactions
✅ PASS Query Parameters (Pagination): Page 1, 5 per page
✅ PASS Error Handling (Invalid JSON): Status: 400
✅ PASS Error Handling (Missing Fields): Status: 400

============================================================
TEST SUMMARY
============================================================
Total Tests: 14
Passed: 14
Failed: 0
Success Rate: 100.0%
```

### DSA Performance Testing

The DSA module includes performance analysis comparing different search algorithms:

#### Performance Results

```
============================================================
SEARCH ALGORITHM PERFORMANCE ANALYSIS
============================================================
Total Transactions: 25
Test Iterations: 100

LINEAR SEARCH (O(n)):
  Average Time: 0.00000523 seconds
  Total Time: 0.00052300 seconds

DICTIONARY LOOKUP (O(1)):
  Average Time: 0.00000112 seconds
  Total Time: 0.00011200 seconds

BINARY SEARCH (O(log n)):
  Average Time: 0.00000245 seconds
  Total Time: 0.00024500 seconds

PERFORMANCE COMPARISON:
  Dictionary is 4.67x faster than Linear Search
  Binary Search is 2.13x faster than Linear Search
  Dictionary is 2.19x faster than Binary Search
```

### Manual Testing with curl

#### Successful GET with Authentication

```bash
curl -u admin:password123 http://localhost:8000/transactions
```

#### Unauthorized Request

```bash
curl http://localhost:8000/transactions
# Returns: 401 Unauthorized
```

#### Successful POST

```bash
curl -u admin:password123 -X POST "http://localhost:8000/transactions" \
  -H "Content-Type: application/json" \
  -d '{"type": "Transfer", "amount": 5000, "sender": "+250788123456", "receiver": "+250789234567"}'
```

#### Successful PUT

```bash
curl -u admin:password123 -X PUT "http://localhost:8000/transactions/1" \
  -H "Content-Type: application/json" \
  -d '{"amount": 7500}'
```

#### Successful DELETE

```bash
curl -u admin:password123 -X DELETE "http://localhost:8000/transactions/1"
```

## Security Analysis

### Basic Authentication Limitations

The current implementation uses Basic Authentication, which has several security weaknesses:

1. **Credentials in Plain Text**: Base64 encoding is not encryption
2. **No Session Management**: Each request requires credentials
3. **No Token Expiration**: Credentials remain valid until changed
4. **Vulnerable to Replay Attacks**: Intercepted credentials can be reused

### Recommended Security Improvements

For production deployment, consider:

1. **JWT Tokens**: Stateless authentication with expiration
2. **OAuth 2.0**: Industry-standard authorization framework
3. **HTTPS**: Encrypt all communications
4. **Rate Limiting**: Prevent abuse and DoS attacks
5. **Input Validation**: Comprehensive data sanitization
6. **API Keys**: Unique keys with rotation capabilities

## Technology Stack

- **Backend:** Python 3.8+ with http.server
- **Data Processing:** xml.etree.ElementTree, json
- **Authentication:** Basic Authentication (base64)
- **Testing:** requests library for API testing
- **Documentation:** Markdown with comprehensive examples
- **Version Control:** Git, GitHub

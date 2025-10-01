# MoMo SMS Data Analytics Platform

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

## Technology Stack

- **Backend:** Python 3.8+ with http.server
- **Data Processing:** xml.etree.ElementTree, json
- **Authentication:** Basic Authentication (base64)
- **Testing:** requests library for API testing
- **Documentation:** Markdown with comprehensive examples
- **Version Control:** Git, GitHub

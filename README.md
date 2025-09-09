# MoMo SMS Data Analytics Platform

## Team Information
**Team Name:** Team 7

**Project Description:** 
An enterprise-level full-stack application designed to process MoMo SMS data in XML format, clean and categorize transactions, store data in a relational database, and provide a comprehensive frontend interface for data analysis and visualization.

**Team Members:**
- TUYISHIMIRE Ishimwe Hannah
- BYIRINGIRO Saad  
- BIENVENUE Cedric

## Project Overview
This application processes Mobile Money (MoMo) transaction data from SMS notifications in XML format, performing ETL operations to clean, normalize, and categorize the data before storing it in a SQLite database. The frontend provides interactive dashboards and visualizations for transaction analysis.

## System Architecture
[**Architecture Diagram**](https://drive.google.com/file/d/1eU6X-h50mTTEokCH-wUGPPrrBe-h7zKN/view?usp=sharing)

## Project Structure
```
.
├── README.md                         # Setup, run, overview
├── .env.example                      # DATABASE_URL or path to SQLite
├── requirements.txt                  # lxml/ElementTree, dateutil, (FastAPI optional)
├── index.html                        # Dashboard entry (static)
├── web/
│   ├── styles.css                    # Dashboard styling
│   ├── chart_handler.js              # Fetch + render charts/tables
│   └── assets/                       # Images/icons (optional)
├── data/
│   ├── raw/                          # Provided XML input (git-ignored)
│   │   └── momo.xml
│   ├── processed/                    # Cleaned/derived outputs for frontend
│   │   └── dashboard.json            # Aggregates the dashboard reads
│   ├── db.sqlite3                    # SQLite DB file
│   └── logs/
│       ├── etl.log                   # Structured ETL logs
│       └── dead_letter/              # Unparsed/ignored XML snippets
├── etl/
│   ├── __init__.py
│   ├── config.py                     # File paths, thresholds, categories
│   ├── parse_xml.py                  # XML parsing (ElementTree/lxml)
│   ├── clean_normalize.py            # Amounts, dates, phone normalization
│   ├── categorize.py                 # Simple rules for transaction types
│   ├── load_db.py                    # Create tables + upsert to SQLite
│   └── run.py                        # CLI: parse -> clean -> categorize -> load -> export JSON
├── api/                              # Optional (bonus)
│   ├── __init__.py
│   ├── app.py                        # Minimal FastAPI with /transactions, /analytics
│   ├── db.py                         # SQLite connection helpers
│   └── schemas.py                    # Pydantic response models
├── scripts/
│   ├── run_etl.sh                    # python etl/run.py --xml data/raw/momo.xml
│   ├── export_json.sh                # Rebuild data/processed/dashboard.json
│   └── serve_frontend.sh             # python -m http.server 8000 (or Flask static)
└── tests/
    ├── test_parse_xml.py             # Small unit tests
    ├── test_clean_normalize.py
    └── test_categorize.py
```

## Prerequisites
- Python 3.8+
- SQLite3
- Modern web browser

## Features
- **XML Data Processing:** Parse and validate MoMo SMS data from XML files
- **Data Cleaning:** Normalize amounts, dates, and phone numbers
- **Transaction Categorization:** Automatic categorization based on configurable rules
- **Database Storage:** Efficient SQLite database with proper indexing
- **Interactive Dashboard:** Web-based visualization and analytics
- **RESTful API:** Optional API endpoints for data access
- **Error Handling:** Comprehensive logging and dead letter queue for failed records

## Scrum Board
**Project Management:** [Trello Board](https://trello.com/invite/b/68be95de19b85650e16f8e5a/ATTI35a0f9a81f8e1e87b1503d0cf8cb26b7A96AEAA4/my-trello-board)

## Technology Stack
- **Backend:** Python 3.8+, FastAPI (optional)
- **Database:** SQLite3
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Data Processing:** lxml/ElementTree, python-dateutil
- **Visualization:** Chart.js or D3.js
- **Testing:** pytest
- **Version Control:** Git, GitHub

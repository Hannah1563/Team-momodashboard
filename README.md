# Team-momodashboard
This is for team collaboration

M-money Dashboard

An enterprise-level full-stack application for processing and visualizing mobile money transactions.

✅ Project Overview
Team Name

TUYISHIMIRE Ishimwe Hannah

BYIRINGIRO Saad

Bienvenue cedric

Project Description

This project involves processing MoMo SMS data in XML format, cleaning and categorizing the data, storing it in a relational database, and building a frontend interface to analyze and visualize the data.
MOMO-Dashboard/

Project Structure

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


🔗 Links

GitHub Repository: [https://github.com/Hannah1563/Team-momodashboard.git]

System Architecture Diagram: [Insert link to your architecture diagram here]

Trello Board: [https://trello.com/invite/b/68be95de19b85650e16f8e5a/ATTI35a0f9a81f8e1e87b1503d0cf8cb26b7A96AEAA4/my-trello-board]



👥 Contributors


TUYISHIMIRE Ishimwe Hannah

BIRINGIRO Saad

BIENVENUE Cedric

📄 License
MIT License

Author
_Bought to life by :Hannah Tuyishimire Ishimwe
                   Saad Byiringiro
                   Cedric Bienvenue
                   
Created from a desire to understand and manage MOMO transactions better.

MIT License

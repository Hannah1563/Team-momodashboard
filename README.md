# Team-momodashboard
this is for team collaboration
Objective:
In this continuous formative assessment, you will demonstrate your ability to design and develop an enterprise-level fullstack application. Your task is to process MoMo SMS data in XML format, clean and categorize the data, store it in a relational database, and build a frontend interface to analyze and visualize the data. This assignment tests your skills in backend data processing, database management, and frontend development.

This first week's assignment will help you practice collaborative development workflows by setting up your team’s shared workspace, defining your system architecture, and organizing tasks using Agile practices.

Tasks
Team GitHub Repository

One member should create a team repository on GitHub.

Invite all teammates as collaborators.

Add a README.md file with your team name, project description, and member list.

Project Organization
Organize your project taking inspiration from the following structure. You don't need to have the files yet, but organize your directory in a way that makes sense
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
High Level System Architecture
Use a tool like Draw.ioLinks to an external site. or MiroLinks to an external site. to create a high-level draft system architecture
Put the link of the design in your README 
Scrum Board Setup

Create a Scrum board for your team (you can use GitHub Projects, Trello, or Jira).

Add at least three columns: To Do, In Progress, Done.

Populate the board with initial tasks for your project (e.g., repo setup, architecture diagram, research).

Share the board link in your README.md file.

Deliverables (to submit):
Link to your GitHub repository (with team members added).

Architecture diagram file/image in the repo.

Link to your Scrum board (added inside README.md).

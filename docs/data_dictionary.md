# Data Dictionary

## Users Table

| Column       | Data Type          | PK/FK | Description                         |
| ------------ | ------------------ | ----- | ----------------------------------- |
| user_id      | INT AUTO_INCREMENT | PK    | Unique identifier for each user     |
| full_name    | VARCHAR(100)       |       | Customer's full name                |
| phone_number | VARCHAR(20)        |       | Unique phone number of the customer |
| email        | VARCHAR(100)       |       | Optional email address              |
| created_at   | DATETIME           |       | Account creation timestamp          |

## Transactions Table

| Column                             | Data Type            | PK/FK | Description                                     |
| ---------------------------------- | -------------------- | ----- | ----------------------------------------------- |
| transaction_id                     | INT AUTO_INCREMENT   | PK    | Unique identifier for each transaction          |
| Users.user_id                      | ID of sending user   |
| Users.user_id                      | ID of receiving user |
| Transaction_Categories.category_id | Transaction type     |
| amount                             | DECIMAL(10,2)        |       | Transaction amount                              |
| currency                           | VARCHAR(10)          |       | Currency code (e.g., RWF, USD)                  |
| timestamp                          | DATETIME             |       | Time transaction was created                    |
| status                             | VARCHAR(20)          |       | Transaction status (Pending, Completed, Failed) |

## Transaction_Categories Table

| Column        | Data Type          | PK/FK | Description                             |
| ------------- | ------------------ | ----- | --------------------------------------- |
| category_id   | INT AUTO_INCREMENT | PK    | Unique identifier for each category     |
| category_name | VARCHAR(50)        |       | Category name (e.g., Transfer, Payment) |
| description   | TEXT               |       | Description of the category             |

## System_Logs Table

| Column                      | Data Type          | PK/FK | Description                          |
| --------------------------- | ------------------ | ----- | ------------------------------------ |
| log_id                      | INT AUTO_INCREMENT | PK    | Unique identifier for each log entry |
| Transactions.transaction_id | Linked transaction |
| log_type                    | VARCHAR(20)        |       | Log level (INFO, ERROR, SUCCESS)     |
| message                     | TEXT               |       | Detailed log message                 |
| created_at                  | DATETIME           |       | When the log entry was created       |

# Database Design Rationale

The database design for the MoMo SMS data processing system was created to ensure efficiency, scalability, and data integrity while meeting the project's business requirements. Four core entities were identified: Users, Transactions, Transaction_Categories, and System_Logs.

The Users table stores information about mobile money customers who participate in transactions, either as senders or receivers. Instead of duplicating sender and receiver details in every transaction record, foreign keys reference the Users table, which reduces redundancy and ensures consistency. This creates a self-referential one-to-many relationship where one user can appear in many transactions, both as sender and receiver.

The Transactions table acts as the central fact table. It contains key attributes such as amount, currency, timestamp, and status. Each transaction is linked to a Transaction_Category, allowing for classification (e.g., transfers, payments, deposits). Categorization improves reporting and analytics by enabling queries such as "total payments this month" or "top categories by frequency."

To ensure transparency and debugging capabilities, the System_Logs table records events related to transaction processing. This table enables auditing, error tracking, and system monitoring. Linking logs to transactions provides a detailed history of how each transaction was processed, supporting troubleshooting and compliance.

The schema has been normalized to avoid duplication and enforce referential integrity. Primary and foreign keys ensure accurate relationships, while indexes on frequently queried fields (phone_number, timestamp, category_id) improve performance. The design supports both current operational needs and future scaling requirements, including additional transaction types, user growth, and enhanced logging capabilities.

This structure balances efficiency, data accuracy, and scalability to support the comprehensive needs of the MoMo data processing system while maintaining optimal performance and data integrity.

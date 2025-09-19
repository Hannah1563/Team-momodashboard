-- =====================================================
-- MoMo SMS Data Analytics Platform - Database Setup
-- Week 2 Assignment - Database Design and Implementation
-- Team 7: Hannah, Saad, Cedric
-- =====================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS System_Logs;
DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS Transaction_Categories;
DROP TABLE IF EXISTS Users;

-- =====================================================
-- 1. USERS TABLE
-- Stores information about mobile money customers
-- =====================================================
CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each user',
    full_name VARCHAR(100) NOT NULL COMMENT 'Customer full name',
    phone_number VARCHAR(20) UNIQUE NOT NULL COMMENT 'Unique phone number (mobile money account)',
    email VARCHAR(100) COMMENT 'Optional email address',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Account creation timestamp',
    
    -- Constraints
    CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^[+]?[0-9]{10,15}$'),
    CONSTRAINT chk_email_format CHECK (email IS NULL OR email REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. TRANSACTION_CATEGORIES TABLE
-- Defines different types of mobile money transactions
-- =====================================================
CREATE TABLE Transaction_Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each category',
    category_name VARCHAR(50) NOT NULL UNIQUE COMMENT 'Category name (e.g., Transfer, Payment, Deposit)',
    description TEXT COMMENT 'Detailed description of the transaction category',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Category creation timestamp',
    
    -- Constraints
    CONSTRAINT chk_category_name CHECK (category_name IN ('Transfer', 'Payment', 'Deposit', 'Withdrawal', 'Bill Payment', 'Airtime Purchase', 'Cash In', 'Cash Out'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 3. TRANSACTIONS TABLE (Main Fact Table)
-- Central table storing all mobile money transactions
-- =====================================================
CREATE TABLE Transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each transaction',
    sender_id INT NOT NULL COMMENT 'ID of the user sending money',
    receiver_id INT NOT NULL COMMENT 'ID of the user receiving money',
    category_id INT NOT NULL COMMENT 'Transaction type category',
    amount DECIMAL(10,2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(10) DEFAULT 'RWF' COMMENT 'Currency code (RWF, USD, etc.)',
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Transaction timestamp',
    status VARCHAR(20) DEFAULT 'Completed' COMMENT 'Transaction status',
    reference_number VARCHAR(50) UNIQUE COMMENT 'Unique transaction reference from MoMo provider',
    description TEXT COMMENT 'Additional transaction details',
    
    -- Foreign Key Constraints
    CONSTRAINT fk_transaction_sender FOREIGN KEY (sender_id) REFERENCES Users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_receiver FOREIGN KEY (receiver_id) REFERENCES Users(user_id) ON DELETE RESTRICT,
    CONSTRAINT fk_transaction_category FOREIGN KEY (category_id) REFERENCES Transaction_Categories(category_id) ON DELETE RESTRICT,
    
    -- Business Logic Constraints
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_status_valid CHECK (status IN ('Pending', 'Completed', 'Failed', 'Cancelled')),
    CONSTRAINT chk_currency_valid CHECK (currency IN ('RWF', 'USD', 'EUR', 'GBP')),
    CONSTRAINT chk_not_self_transfer CHECK (sender_id != receiver_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 4. SYSTEM_LOGS TABLE
-- Audit trail and system monitoring
-- =====================================================
CREATE TABLE System_Logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Unique identifier for each log entry',
    transaction_id INT COMMENT 'Linked transaction (nullable for system events)',
    log_type VARCHAR(20) NOT NULL COMMENT 'Log level/type',
    message TEXT NOT NULL COMMENT 'Detailed log message',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT 'Log entry timestamp',
    user_id INT COMMENT 'User involved in the event (nullable)',
    
    -- Foreign Key Constraints
    CONSTRAINT fk_log_transaction FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id) ON DELETE SET NULL,
    CONSTRAINT fk_log_user FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE SET NULL,
    
    -- Constraints
    CONSTRAINT chk_log_type CHECK (log_type IN ('INFO', 'ERROR', 'WARNING', 'SUCCESS', 'DEBUG'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- INDEXES FOR PERFORMANCE OPTIMIZATION
-- =====================================================

-- Users table indexes
CREATE INDEX idx_users_phone ON Users(phone_number);
CREATE INDEX idx_users_email ON Users(email);
CREATE INDEX idx_users_created_at ON Users(created_at);

-- Transactions table indexes
CREATE INDEX idx_transactions_sender ON Transactions(sender_id);
CREATE INDEX idx_transactions_receiver ON Transactions(receiver_id);
CREATE INDEX idx_transactions_category ON Transactions(category_id);
CREATE INDEX idx_transactions_timestamp ON Transactions(timestamp);
CREATE INDEX idx_transactions_status ON Transactions(status);
CREATE INDEX idx_transactions_amount ON Transactions(amount);
CREATE INDEX idx_transactions_currency ON Transactions(currency);
CREATE INDEX idx_transactions_reference ON Transactions(reference_number);

-- System_Logs table indexes
CREATE INDEX idx_logs_transaction ON System_Logs(transaction_id);
CREATE INDEX idx_logs_type ON System_Logs(log_type);
CREATE INDEX idx_logs_created_at ON System_Logs(created_at);
CREATE INDEX idx_logs_user ON System_Logs(user_id);

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert Transaction Categories
INSERT INTO Transaction_Categories (category_name, description) VALUES
('Transfer', 'Peer-to-peer money transfer between users'),
('Payment', 'Payment for goods and services'),
('Deposit', 'Cash deposit to mobile money account'),
('Withdrawal', 'Cash withdrawal from mobile money account'),
('Bill Payment', 'Payment of utility bills and services'),
('Airtime Purchase', 'Purchase of mobile phone airtime'),
('Cash In', 'Cash deposit from agent or bank'),
('Cash Out', 'Cash withdrawal through agent');

-- Insert Sample Users
INSERT INTO Users (full_name, phone_number, email) VALUES
('John Mukamana', '+250788123456', 'john.mukamana@email.com'),
('Marie Uwimana', '+250789234567', 'marie.uwimana@email.com'),
('Peter Nkurunziza', '+250790345678', 'peter.nkurunziza@email.com'),
('Grace Mutesi', '+250791456789', 'grace.mutesi@email.com'),
('David Rukundo', '+250792567890', 'david.rukundo@email.com'),
('Agnes Nyirahabimana', '+250793678901', 'agnes.nyirahabimana@email.com'),
('Paul Nsengimana', '+250794789012', 'paul.nsengimana@email.com'),
('Immaculate Mukamana', '+250795890123', 'immaculate.mukamana@email.com');

-- Insert Sample Transactions
INSERT INTO Transactions (sender_id, receiver_id, category_id, amount, currency, timestamp, status, reference_number, description) VALUES
(1, 2, 1, 5000.00, 'RWF', '2024-09-15 10:30:00', 'Completed', 'TXN001234567', 'Payment for lunch'),
(2, 3, 1, 15000.00, 'RWF', '2024-09-15 14:20:00', 'Completed', 'TXN001234568', 'Family support'),
(3, 4, 2, 25000.00, 'RWF', '2024-09-16 09:15:00', 'Completed', 'TXN001234569', 'Market shopping payment'),
(4, 5, 5, 12000.00, 'RWF', '2024-09-16 16:45:00', 'Completed', 'TXN001234570', 'Electricity bill payment'),
(5, 6, 6, 5000.00, 'RWF', '2024-09-17 11:30:00', 'Completed', 'TXN001234571', 'Airtime top-up'),
(6, 7, 1, 8000.00, 'RWF', '2024-09-17 13:20:00', 'Completed', 'TXN001234572', 'Transport money'),
(7, 8, 3, 50000.00, 'RWF', '2024-09-18 08:00:00', 'Completed', 'TXN001234573', 'Salary deposit'),
(8, 1, 4, 20000.00, 'RWF', '2024-09-18 17:30:00', 'Completed', 'TXN001234574', 'Cash withdrawal');

-- Insert Sample System Logs
INSERT INTO System_Logs (transaction_id, log_type, message, user_id) VALUES
(1, 'SUCCESS', 'Transaction processed successfully', 1),
(1, 'INFO', 'SMS notification sent to receiver', 2),
(2, 'SUCCESS', 'Transfer completed within 30 seconds', 2),
(3, 'INFO', 'Payment verified and processed', 3),
(4, 'SUCCESS', 'Bill payment confirmed by utility provider', 4),
(5, 'INFO', 'Airtime credit added to recipient account', 5),
(6, 'SUCCESS', 'Transfer completed', 6),
(7, 'INFO', 'Large deposit transaction logged for compliance', 7),
(8, 'SUCCESS', 'Cash withdrawal authorized', 8),
(NULL, 'INFO', 'Daily transaction summary generated', NULL),
(NULL, 'INFO', 'System backup completed successfully', NULL),
(NULL, 'WARNING', 'High transaction volume detected', NULL);

-- =====================================================
-- SAMPLE QUERIES FOR TESTING
-- =====================================================

-- Query 1: Get all transactions for a specific user
-- SELECT t.*, u1.full_name as sender_name, u2.full_name as receiver_name, tc.category_name
-- FROM Transactions t
-- JOIN Users u1 ON t.sender_id = u1.user_id
-- JOIN Users u2 ON t.receiver_id = u2.user_id
-- JOIN Transaction_Categories tc ON t.category_id = tc.category_id
-- WHERE t.sender_id = 1 OR t.receiver_id = 1
-- ORDER BY t.timestamp DESC;

-- Query 2: Get transaction summary by category
-- SELECT tc.category_name, COUNT(*) as transaction_count, SUM(t.amount) as total_amount
-- FROM Transactions t
-- JOIN Transaction_Categories tc ON t.category_id = tc.category_id
-- WHERE t.status = 'Completed'
-- GROUP BY tc.category_id, tc.category_name
-- ORDER BY total_amount DESC;

-- Query 3: Get user transaction history with logs
-- SELECT u.full_name, u.phone_number, COUNT(t.transaction_id) as transaction_count,
--        SUM(CASE WHEN t.sender_id = u.user_id THEN t.amount ELSE 0 END) as total_sent,
--        SUM(CASE WHEN t.receiver_id = u.user_id THEN t.amount ELSE 0 END) as total_received
-- FROM Users u
-- LEFT JOIN Transactions t ON (u.user_id = t.sender_id OR u.user_id = t.receiver_id)
-- GROUP BY u.user_id, u.full_name, u.phone_number;

-- =====================================================
-- DATABASE SETUP COMPLETE
-- =====================================================

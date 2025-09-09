CREATE TABLE chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    farmer_id INTEGER,
    message TEXT,
    sender TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
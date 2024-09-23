attendance.db

sql

Verify

Open In Editor
Edit
Copy code
CREATE TABLE students (
    id TEXT PRIMARY KEY,
    name TEXT
);

CREATE TABLE attendance (
    id INTEGER PRIMARY KEY,
    user_id TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES students (id)
);

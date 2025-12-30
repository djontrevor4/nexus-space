"""Memory - долгосрочная память NEXUS"""
import sqlite3
import json
from pathlib import Path
from datetime import datetime

class Memory:
    def __init__(self, db_path=None):
        root = Path(__file__).parent.parent
        self.db_path = db_path or root / "data" / "nexus.db"
        self.db = sqlite3.connect(str(self.db_path))
        self._init_tables()

    def _init_tables(self):
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS findings (
                id INTEGER PRIMARY KEY,
                target TEXT,
                type TEXT,
                severity TEXT,
                data TEXT,
                found_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                agent TEXT,
                task TEXT,
                result TEXT,
                status TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS knowledge (
                id INTEGER PRIMARY KEY,
                key TEXT UNIQUE,
                value TEXT,
                updated_at TIMESTAMP
            );
            CREATE INDEX IF NOT EXISTS idx_findings_target ON findings(target);
            CREATE INDEX IF NOT EXISTS idx_findings_severity ON findings(severity);
        """)
        self.db.commit()

    def save_finding(self, target, ftype, severity, data):
        self.db.execute(
            "INSERT INTO findings (target, type, severity, data) VALUES (?,?,?,?)",
            (target, ftype, severity, json.dumps(data))
        )
        self.db.commit()

    def get_findings(self, target=None, severity=None, limit=50):
        sql = "SELECT * FROM findings WHERE 1=1"
        params = []
        if target:
            sql += " AND target LIKE ?"
            params.append(f"%{target}%")
        if severity:
            sql += " AND severity = ?"
            params.append(severity)
        sql += f" ORDER BY found_at DESC LIMIT {limit}"
        return self.db.execute(sql, params).fetchall()

    def remember(self, key, value):
        self.db.execute(
            "INSERT OR REPLACE INTO knowledge (key, value, updated_at) VALUES (?,?,?)",
            (key, json.dumps(value), datetime.now().isoformat())
        )
        self.db.commit()

    def recall(self, key):
        row = self.db.execute("SELECT value FROM knowledge WHERE key=?", (key,)).fetchone()
        return json.loads(row[0]) if row else None

    def stats(self):
        findings = self.db.execute("SELECT severity, COUNT(*) FROM findings GROUP BY severity").fetchall()
        tasks = self.db.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        return {"findings": dict(findings), "total_tasks": tasks}

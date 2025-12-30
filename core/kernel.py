"""NEXUS Kernel - центральное ядро"""
import os
import json
from pathlib import Path
from datetime import datetime

class Kernel:
    VERSION = "1.0.0"

    def __init__(self):
        self.root = Path(__file__).parent.parent
        self.started = datetime.now()
        self.state = "ready"
        self._load_config()

    def _load_config(self):
        cfg_path = self.root / "config" / "nexus.json"
        if cfg_path.exists():
            self.config = json.loads(cfg_path.read_text())
        else:
            self.config = {"mode": "active", "log_level": "INFO"}

    def log(self, level, msg, module="KERNEL"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}][{module}] {level}: {msg}"
        print(line)
        log_file = self.root / "logs" / f"{datetime.now().strftime('%Y-%m-%d')}.log"
        with open(log_file, "a") as f:
            f.write(line + "\n")

    def status(self):
        uptime = (datetime.now() - self.started).seconds
        return {
            "version": self.VERSION,
            "state": self.state,
            "uptime_sec": uptime,
            "root": str(self.root)
        }

import os
from pathlib import Path

SPACE_NAME = "nexus"
SPACE_ROOT = Path(__file__).parent.parent
DATA_DIR = SPACE_ROOT / "data"
LOGS_DIR = SPACE_ROOT / "logs"

VPS_ENDPOINT = "http://176.123.169.38:5000"
VPS_KEY = "claude2025"

GITHUB_USER = os.getenv("GITHUB_USER", "djontrevor4")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
TG_CHAT_ID = "1198523752"


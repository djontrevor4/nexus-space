"""Bridge Agent"""
import requests as req
from agents.base import BaseAgent

class BridgeAgent(BaseAgent):
    name = "bridge"
    VPS_URL = "http://176.123.169.38:5000"
    VPS_KEY = "claude2025"

    def execute(self, task):
        parts = task.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        if cmd == "termux":
            return self.termux(args)
        return self.vps(args if args else task)

    def vps(self, cmd):
        try:
            r = req.post(f"{self.VPS_URL}/vps", json={"key": self.VPS_KEY, "cmd": cmd}, timeout=30)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

    def termux(self, cmd):
        try:
            r = req.post(f"{self.VPS_URL}/termux", json={"key": self.VPS_KEY, "cmd": cmd}, timeout=30)
            return r.json()
        except Exception as e:
            return {"error": str(e)}

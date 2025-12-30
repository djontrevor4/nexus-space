"""Dispatcher - маршрутизация задач к агентам"""
import sys
from pathlib import Path

class Dispatcher:
    def __init__(self, kernel):
        self.kernel = kernel
        self.agents = {}
        self.routes = {
            "scan": "scanner",
            "hunt": "scanner", 
            "recon": "recon",
            "subdomain": "recon",
            "port": "recon",
            "exploit": "exploit",
            "report": "report",
            "exec": "bridge",
            "vps": "bridge",
            "termux": "bridge",
            "tg": "bridge"
        }
        self._load_agents()

    def _load_agents(self):
        # Импортируем напрямую из agents
        sys.path.insert(0, str(self.kernel.root))
        from agents import ScannerAgent, ReconAgent, BridgeAgent

        self.agents = {
            "scanner": ScannerAgent(),
            "recon": ReconAgent(),
            "bridge": BridgeAgent()
        }

    def route(self, task):
        cmd = task.split()[0].lower()
        return self.routes.get(cmd, "bridge")

    def dispatch(self, task):
        agent_name = self.route(task)
        self.kernel.log("INFO", f"Task -> {agent_name}: {task[:50]}", "DISPATCH")

        if agent_name in self.agents:
            return self.agents[agent_name].execute(task)

        return {"error": f"Agent {agent_name} not found"}

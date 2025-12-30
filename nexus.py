#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════╗
║  NEXUS - Neural EXecution Unified System                  ║
║  Центральная система управления и автоматизации           ║
╚═══════════════════════════════════════════════════════════╝
"""
import sys
import json
from pathlib import Path

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT))

from core.kernel import Kernel
from core.dispatcher import Dispatcher
from core.memory import Memory

class Nexus:
    def __init__(self):
        self.kernel = Kernel()
        self.dispatcher = Dispatcher(self.kernel)
        self.memory = Memory()
        self.kernel.log("INFO", "NEXUS initialized", "MAIN")

    def execute(self, task):
        """Выполнить задачу"""
        self.kernel.log("INFO", f"Execute: {task}", "MAIN")
        result = self.dispatcher.dispatch(task)

        # Сохраняем в память
        if isinstance(result, dict) and result.get("findings"):
            for f in result["findings"]:
                self.memory.save_finding(
                    target=result.get("target", "unknown"),
                    ftype=f.get("type", "info"),
                    severity=f.get("sev", "LOW"),
                    data=f
                )
        return result

    def status(self):
        """Полный статус системы"""
        return {
            "kernel": self.kernel.status(),
            "agents": list(self.dispatcher.agents.keys()),
            "memory": self.memory.stats(),
            "routes": list(self.dispatcher.routes.keys())
        }

    def query(self, q):
        """Запрос к памяти"""
        return self.memory.recall(q)

    def findings(self, target=None, severity=None):
        """Получить находки"""
        return self.memory.get_findings(target, severity)

def main():
    nx = Nexus()

    if len(sys.argv) < 2:
        print(json.dumps(nx.status(), indent=2, ensure_ascii=False))
        return

    cmd = sys.argv[1]
    args = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    if cmd == "status":
        print(json.dumps(nx.status(), indent=2, ensure_ascii=False))
    elif cmd == "findings":
        print(json.dumps(nx.findings(args or None), indent=2))
    elif cmd == "stats":
        print(json.dumps(nx.memory.stats(), indent=2))
    else:
        result = nx.execute(f"{cmd} {args}".strip())
        print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

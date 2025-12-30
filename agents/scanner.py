"""Scanner Agent - сканирование на уязвимости"""
import requests as req
import urllib3
urllib3.disable_warnings()

from agents.base import BaseAgent

class ScannerAgent(BaseAgent):
    name = "scanner"

    PATHS = ["/.env", "/.git/HEAD", "/robots.txt", "/api", "/swagger.json", "/graphql", "/admin"]

    HEADERS_CHECK = [
        ("X-Frame-Options", "MEDIUM", "Clickjacking"),
        ("Content-Security-Policy", "LOW", "No CSP"),
        ("Strict-Transport-Security", "MEDIUM", "No HSTS"),
    ]

    def execute(self, task):
        target = self.parse_target(task)
        return self.scan(target)

    def scan(self, target):
        base = f"https://{target}" if not target.startswith("http") else target
        findings = []

        try:
            r = req.get(base, timeout=10, verify=False)
            findings.append({"type": "INFO", "status": r.status_code})

            for header, sev, desc in self.HEADERS_CHECK:
                if header not in r.headers:
                    findings.append({"type": "HEADER", "sev": sev, "vuln": desc})

        except Exception as e:
            return {"target": target, "error": str(e), "findings": []}

        for path in self.PATHS:
            try:
                r2 = req.get(f"{base}{path}", timeout=5, allow_redirects=False, verify=False)
                if r2.status_code == 200:
                    findings.append({"type": "EXPOSED", "sev": "HIGH", "path": path})
            except:
                pass

        return {"target": target, "findings": findings}

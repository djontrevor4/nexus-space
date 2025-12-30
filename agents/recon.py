"""Recon Agent - разведка"""
import requests as req
import socket
from agents.base import BaseAgent

class ReconAgent(BaseAgent):
    name = "recon"

    def execute(self, task):
        target = self.parse_target(task)
        if "subdomain" in task.lower():
            return self.subdomains(target)
        return self.full_recon(target)

    def full_recon(self, target):
        domain = target.replace("https://","").replace("http://","").split("/")[0]
        result = {"target": domain, "ip": None, "subdomains": [], "tech": []}

        try:
            result["ip"] = socket.gethostbyname(domain)
        except:
            pass

        # crt.sh subdomains
        try:
            r = req.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=15)
            if r.status_code == 200:
                subs = set()
                for c in r.json():
                    for s in c.get("name_value","").split("\n"):
                        if domain in s:
                            subs.add(s.replace("*.",""))
                result["subdomains"] = list(subs)[:30]
        except:
            pass

        return result

    def subdomains(self, target):
        domain = target.replace("https://","").replace("http://","").split("/")[0]
        subs = []
        try:
            r = req.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=20)
            if r.status_code == 200:
                for c in r.json():
                    for s in c.get("name_value","").split("\n"):
                        if domain in s and s not in subs:
                            subs.append(s.replace("*.",""))
        except:
            pass
        return {"target": domain, "subdomains": subs[:50]}

"""Базовый класс агента"""
from abc import ABC, abstractmethod

class BaseAgent(ABC):
    name = "base"
    description = "Base agent class"

    @abstractmethod
    def execute(self, task):
        pass

    def parse_target(self, task):
        parts = task.split()
        return parts[-1] if len(parts) > 1 else parts[0]

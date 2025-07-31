from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Abstract base class for agentic workflows (evaluation, optimization, reporting, etc).
    """

    @abstractmethod
    def run(self, **kwargs) -> Any:
        pass

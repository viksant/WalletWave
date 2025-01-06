from abc import ABC, abstractmethod

class StrategyInterface(ABC):
    """
    Abstract base class for all strategies
    """
    @abstractmethod
    def execute(self):
        pass

from abc import ABC, abstractmethod

class BaseTool(ABC):
    """
    Base class for all tools.
    Every tool must implement run().
    """

    name = "Base Tool"
    description = "Abstract Tool"

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Execute the tool.
        """
        pass
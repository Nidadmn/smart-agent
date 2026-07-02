from abc import ABC, abstractmethod


class BaseTool(ABC):
    """
    Base class for all tools.
    Every tool must inherit from this class.
    """

    name = "Base Tool"
    description = "Abstract Tool"

    @abstractmethod
    def execute(self, *args, **kwargs):
        """
        Execute the tool.
        """
        pass
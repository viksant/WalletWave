from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """
    Abstract base class for all plugins. Every plugin must implement the following methods.
    """

    @abstractmethod
    def get_name(self) -> str:
        """
        Returns the name of the plugin.
        """
        pass

    @abstractmethod
    def get_description(self) -> str:
        """
        Returns a brief description of the plugin.
        """
        pass

    @abstractmethod
    def initialize(self, config: dict) -> None:
        """
        Called once to initialize the plugin with the given configuration.
        :param config: Dictionary containing plugin-specific configuration.
        """
        pass

    @abstractmethod
    def execute(self, data: any) -> any:
        """
        Executes the plugin's main functionality.
        :param data: Input data that the plugin will process.
        :return: Processed data.
        """
        pass

    @abstractmethod
    def finalize(self) -> None:
        """
        Called when the plugin is being unloaded to clean up resources.
        """
        pass
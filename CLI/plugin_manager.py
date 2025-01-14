import importlib
import os
import inspect
from WalletWave.plugins.utils.plugin_interface import PluginInterface

class PluginManager:
    """
    Manages plugins: loading, selecting, and executing them.
    """

    def __init__(self, plugin_directory: str = None):
        if plugin_directory is not None:
            self.plugin_directory = plugin_directory
        else:
            self.plugin_directory = "../WalletWave/plugins"
        self.plugins = []

    def load_plugins(self) -> None:
        """
        Dynamically loads plugins from the specified directory.
        """
        for file in os.listdir(self.plugin_directory):
            if file.endswith(".py") and file != "__init__.py":
                module_name = file[:-3]  # Remove the .py extension
                module = importlib.import_module(f"{self.plugin_directory}.{module_name}")
                for _, obj in inspect.getmembers(module, inspect.isclass):
                    if issubclass(obj, PluginInterface) and obj is not PluginInterface:
                        self.plugins.append(obj())

    def list_plugins(self) -> None:
        """
        Lists all available plugins with their descriptions.
        """
        for i, plugin in enumerate(self.plugins):
            print(f"[{i + 1}] {plugin.get_name()}: {plugin.get_description()}")

    def select_plugin(self, index: int):
        """
        Returns the selected plugin based on the index.
        """
        if 0 <= index < len(self.plugins):
            return self.plugins[index]
        else:
            raise ValueError("Invalid plugin index")

import argparse
import yaml
import os
from yaml import YAMLError

from WalletWave.utils.config_validators import *
from WalletWave.utils.logging_utils import setup_logger


class ConfigManager:
    """
    Wallet Wave configuration manager
    """
    def __init__(self, args = None):
        self.logger = setup_logger("ConfigManager")
        self._config_path = os.path.abspath(args.config)
        self._config_data = self._load_config()
        self._args = args
        self._final_config = self._merge_configurations()
        self._plugin_settings = self._load_plugin_settings()

    def _load_config(self):
        """ Load the configuration file"""
        try:
            with open(self._config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            self.logger.warning(f"Config file: '{self._config_path}' not found. Using defaults")
            return {}
        except YAMLError as e:
            self.logger.error(f"Failed to parse YAML in config file '{self._config_path}': {e}")
            return {} # todo quit program


    def _merge_configurations(self):
        """Config file and command-line arguments merger"""
        program_settings = self._config_data.get("program_settings", {})
        return {
            "export_path": validate_path(
                self._args.export_path if self._args and self._args.export_path else program_settings.get("export_path", "data")
            ),
            "verbose": validate_verbose(
                self._args.verbose if self._args and self._args.verbose else program_settings.get("verbose", False)
            ),
            "export_format": validate_export_format(
                self._args.export_format if self._args and self._args.export_format else program_settings.get("export_format", "csv")
            ),
        }

    def _load_plugin_settings(self):
        """ Load plugin-specific settings """
        plugins = self._config_data.get("plugin_settings", {})
        return {plugin: settings for plugin, settings in plugins.items()}

    @property
    def plugins(self):
        """ Return all plugin settings """
        return self._plugin_settings

    def get_plugin_setting(self, plugin, key, default=None):
        """ Get a specific setting for a plugin """
        return self._plugin_settings.get(plugin, {}).get(key, default)

    def set_plugin_setting(self, plugin, key, value):
        """ Set a specific setting for a plugin """
        if plugin not in self._plugin_settings:
            self._plugin_settings[plugin] = {}
        self._plugin_settings[plugin][key] = value

    def __getattr__(self, name):
        """ Get plugin settings as attributes """
        if name in self._plugin_settings:
            return self._plugin_settings[name]
        self.logger.warning(f"No plugin with {name} found, proceeding without plugin settings")
        return {}

    @property
    def export_path(self):
        return self._final_config["export_path"]

    @export_path.setter
    def export_path(self, new_path):
        self._final_config["export_path"] = validate_path(new_path)

    @property
    def verbose(self):
        return self._final_config["verbose"]

    @verbose.setter
    def verbose(self, verbose):
        self._final_config["verbose"] = validate_verbose(verbose)

    @property
    def export_format(self):
        return self._final_config["export_format"]

    @export_format.setter
    def export_format(self, export_format):
        self._final_config["export_format"] = validate_export_format(export_format)

    @property
    def config(self):
        return self._final_config

def parse_args():
    """ Parse command-line arguments"""
    parser = argparse.ArgumentParser(description="Smart Money Follower Configuration")
    parser.add_argument("--config", type=str, default="src/WalletWave/config.yaml", help="Path to the config file")
    parser.add_argument("--export_path", type=str, help="Path to export files")
    parser.add_argument("--verbose", type=bool, help="Verbose script logs")
    parser.add_argument("--export-format", type=str, choices=["csv", "txt"], help="Export format (csv or txt)")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse arguments
    args = parse_args()
    args.config = "config.yaml" # for testing purposes

    # Create ConfigManager instance
    config_manager = ConfigManager(args=args)

    # Access properties
    print("Final Configuration:")
    print(f"Export Path: {config_manager.export_path}")
    print(f"Verbose: {config_manager.verbose}")
    print(f"Export Format: {config_manager.export_format}")

    #plugin settings
    # get via attributes
    plugin_settings = config_manager.TopWallets
    print(plugin_settings.get("timeframe"))

    # get directly
    plugin_settings = config_manager.get_plugin_setting("TopWallets", "timeframe")
    print(plugin_settings)


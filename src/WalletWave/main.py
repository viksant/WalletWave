import logging

from CLI.menu import menu
from WalletWave.config import parse_args
from WalletWave.config import ConfigManager
from WalletWave.utils.file_utils import FileUtils
from WalletWave.utils.logging_utils import setup_logger


class WalletWave:
    """
    Main class
    """
    def __init__(self, config: ConfigManager):
        """
        Initializes the main app.
        """
        self.config = config
        self.logger = setup_logger("main", log_level=logging.INFO) # todo add verbose option
        self.file_utils = FileUtils(self.config.export_path)

    def execute(self, plugin):
        """
        Executes the selected plugin's lifecycle: initialize, execute, and finalize.
        :param plugin: The plugin object to execute.
        """
        try:
            # Step 1: Initialize the plugin
            self.logger.info(f"Initializing: {plugin.get_name()}")
            plugin.initialize()

            # Step 2: Execute the plugin
            self.logger.info("Executing plugin...")
            data = plugin.execute()

            # Step 3: Export plugin results
            if self.config.export_enabled:
                self.logger.info("Exporting plugin results..")
                self.export_data(data)
            else:
                self.logger.info("Exporting data has been set to False in the config file. Skipping export function.")

            # Step 4: Finalize the plugin
            self.logger.info("Finalizing plugin...")
            plugin.finalize()
        except Exception as e:
            self.logger.error(f"An error occurred while running the plugin: {e}")

    def export_data(self, data, export_format = 'csv'):
        """
        Wrapper method to export data using FileUtils.
        """
        self.logger.info("Exporting wallet data...")
        self.file_utils.export_wallet_data(data, export_format=export_format)


def main():
    """Entry point"""
    try:
        # parse command line args and init manager
        args = parse_args()
        manager = ConfigManager(args)

        # run menu
        action = menu(manager)

        #exit if prompted
        if action == "exit":
            return

        # WalletWave instance
        app = WalletWave(manager)

        selected_plugin = action[1]
        # Run
        app.execute(selected_plugin)
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
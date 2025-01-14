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
        self.logger = setup_logger("main") # todo add verbose option
        self.file_utils = FileUtils(self.config.path) # todo change path variable name to export path

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
            self.logger.info(f"Executing plugin...")
            data = plugin.execute(None) # todo: change the none type

            # Step 3: Export plugin results
            self.logger.info(f"Exporting plugin results..")
            self.export_data(data)

            # Step 4: Finalize the plugin
            self.logger.info(f"Finalizing plugin...")
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
        print(f"Action returned from menu: {action}")

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
import logging

from CLI.menu import menu
from WalletWave.config import parse_args
from WalletWave.config import ConfigManager
from WalletWave.utils.file_utils import FileUtils
from WalletWave.utils.logging_utils import get_logger, init_logging

class WalletWave:
    """
    Main class
    """
    def __init__(self, config: ConfigManager):
        """
        Initializes the main app.
        """
        self.config = config
        self.logger = get_logger("WalletWave")
        self.file_utils = FileUtils(self.config.export_path)

    async def execute(self, plugin):
        """
        Executes the selected plugin's lifecycle: initialize, execute, and finalize.
        :param plugin: The plugin object to execute.
        """
        try:
            # Step 1: Initialize the plugin
            self.logger.info(f"Initializing: {plugin.get_name()}")
            await plugin.initialize()

            # Step 2: Execute the plugin
            self.logger.info("Executing plugin...")
            data = await plugin.execute()

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


async def main():
    """Entry point"""
    try:
        args = parse_args()

        manager = ConfigManager(args)

        init_logging(manager.config)

        # run menu
        action = menu(manager)

        #exit if prompted
        if action == "exit":
            return

        # WalletWave instance
        app = await WalletWave(manager)

        selected_plugin = action[1]
        # Run
        await app.execute(selected_plugin)
    except ValueError as e:
        exit(1)

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except RuntimeError as e:
        print(f"Error: {e}")
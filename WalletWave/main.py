import logging
from WalletWave.config import parse_args
from config import ConfigManager
from utils.file_utils import FileUtils

class WalletWave:
    """
    Main class
    """
    def __init__(self, config: ConfigManager):
        """
        Initializes the main app.
        """
        self.config = config
        self.logger = logging.getLogger("main")
        logging.basicConfig(level=logging.INFO) # todo add verbose option
        self.file_utils = FileUtils(self.config.path) # todo change path variable name to export path

    def initialize(self):
        data = self.strategy()
        self.export_data(data)

    def strategy(self):
        self.logger.info("Running strategy...")
        data = ""
        return data

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

        # WalletWave instance
        app = WalletWave(manager)

        # Run
        app.initialize()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
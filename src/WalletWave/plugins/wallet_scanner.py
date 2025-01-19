from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.logging_utils import setup_logger
from WalletWave.config import ConfigManager


class SolanaWalletScanner(PluginInterface):
    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.gmgn = GmgnRepo()
        self.logger = setup_logger("SolanaWalletScanner")
        self.timeframe = None
        self.wallets = []

    def get_name(self) -> str:
        # return the name you want to show in the plugin menu
        return "Solana Wallet Scanner"

    def get_description(self) -> str:
        # return a short description of your plugin
        return "Scans a list of wallets and exports performance"

    def get_version(self) -> str:
        return "1.0.0"

    def initialize(self) -> None:
        # Step 1 of plugin lifecycle
        self.logger.info("Solana Wallet Scanner initialized")
        self.timeframe = self.config_manager.timeframe
        wallet_file_path = input("Please provide the export_path to the wallet file: ").strip()
        self._load_wallets(wallet_file_path)

        if not self.wallets:
            self.logger.error("No wallets loaded. Stopping plugin execution")
            raise RuntimeError("No wallets found in the specified file. Plugin cannot proceed")
        else:
            self.logger.info(f"Solana Wallet Scanner initialized with {len(self.wallets)} wallets")


    def execute(self) -> list:
        # Step 2 execute the plugin
        wallet_data = []
        self.logger.info("Executing Solana Wallet Scanner...")

        for wallet in self.wallets:
            try:
                wallet_info = self.gmgn.get_wallet_info(wallet, period=self.timeframe)
                wallet_data.append(wallet_info.to_summary(wallet))
                self.logger.info(f"Fetched data for wallet: {wallet}")
            except Exception as e:
                self.logger.error(f"Error fetching data for wallet {wallet}: {e}")

        self.logger.info(f"Scanned {len(wallet_data)}")
        return wallet_data


    def finalize(self) -> None:
        self.logger.info("Solana Wallet Scanner finalized")

    def _load_wallets(self, file_path: str) -> None:
        """
            Load wallets address from a text file
            :param file_path: Path to the text file containing wallets.
        """

        try:
            with open(file_path, 'r') as file:
                self.wallets = [line.strip() for line in file if line.strip()]
            self.logger.info(f"Loaded {len(self.wallets)} wallets from {file_path}.")
        except FileNotFoundError:
            self.logger.error(f"Wallet file not found: {file_path}")
        except Exception as e:
            self.logger.error(f"Error reading wallet file: {e}")
from datetime import datetime
import logging
import time

from WalletWave.config import ConfigManager
from WalletWave.services.strategies.strategy_interface import StrategyInterface
from WalletWave.utils.gmgn.client import gmgn
from WalletWave.utils.logging_utils import setup_logger


class TopWalletStrategy(StrategyInterface):
    """
    todo
    """
    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the top_wallet_strategy object.

        """
        self.gmgn = gmgn()
        self.logger = setup_logger("TopWalletStrategy", log_level=logging.INFO)
        self.config = config_manager.config

    def execute(self):
        self.run_strategy()

    def get_top_wallets(self, timeframe="7d", wallet_tag="smart_degen"):
        """
        Fetch top performing wallets using the getTrendingWallets endpoint.

        :param timeframe: Time period for trending wallets (default "7d").
        :param wallet_tag: Tag to filter wallets (default "smart_degen").
        :return: List of top performing wallets.
        """
        try:
            response = self.gmgn.getTrendingWallets(timeframe, wallet_tag)
            return response['rank']
        except Exception as e:
            self.logger.error(f"Error fetching top wallets: {e}")
            return []

    def analyze_wallet_activity(self, wallet_address, period="7d"):
        """
        Analyze recent trading activity of a wallet using the getWalletInfo endpoint.

        :param wallet_address: Address of the wallet to analyze.
        :param period: Time period for wallet analysis (default "7d").
        :return: Wallet activity data.
        """
        try:
            response = self.gmgn.getWalletInfo(walletAddress=wallet_address, period=period)
            return response
        except Exception as e:
            self.logger.error(f"Error analyzing wallet activity: {e}")
            return {}

    def evaluate_token(self, token_address):
        """
        Evaluate a token using the getTokenInfo and getTokenUsdPrice endpoints.

        :param token_address: Address of the token to evaluate.
        :return: Token information and USD price.
        """
        try:
            token_info = self.gmgn.getTokenInfo(contractAddress=token_address)
            token_price = self.gmgn.getTokenUsdPrice(contractAddress=token_address)
            return token_info, token_price
        except Exception as e:
            self.logger.error(f"Error evaluating token: {e}")
            return {}, {}

    def print_analysis_output(self, wallets):
        """
        Print the analysis output in a tabulated format.

        :param wallets: List of wallets to print.
        """
        headers = ["Rank", "Wallet Address", "Realized Profit (SOL or USD)", "Buy Transactions", "Sell Transactions",
                   "Last Active"]
        table_data = []

        for idx, wallet in enumerate(wallets):
            last_active = datetime.utcfromtimestamp(wallet.get('last_active_timestamp', 0)).strftime(
                '%Y-%m-%d %H:%M:%S')
            table_data.append([
                idx + 1,
                wallet.get('wallet_address', 'N/A'),
                wallet.get('realized_profit', 'N/A'),
                wallet.get('buy', 'N/A'),
                wallet.get('sell', 'N/A'),
                last_active
            ])

        print("Note: The 'Realized Profit' is represented in SOL.")

    def run_strategy(self):
        """
        Orchestrate the overall strategy execution.
        """
        try:
            # Step 1: Get top wallets
            top_wallets = self.get_top_wallets(timeframe=self.config.timeframe, wallet_tag=self.config.wallet_tag)
            if not top_wallets:
                self.logger.warning("No top wallets found.")
                return

            wallet_data = []

            # Step 2: Analyze each wallet's activity
            for wallet in top_wallets:
                wallet_address = wallet.get('wallet_address')
                wallet_activity = self.analyze_wallet_activity(wallet_address, period=self.config.timeframe)

                # Log wallet activity data vertically
                self.logger.info(f"Wallet Activity for {wallet_address}:")
                for key, value in wallet_activity.items():
                    self.logger.info(f"{key}: {value}")

                # Filter wallets with a win rate higher than 0.6
                winrate = wallet_activity.get('winrate', 0)
                if winrate is not None and winrate >= self.config.win_rate:
                    wallet_info = {
                        'wallet_address': wallet_address,
                        'realized_profit': wallet_activity.get('realized_profit', 'N/A'),
                        'buy': wallet_activity.get('buy', 'N/A'),
                        'sell': wallet_activity.get('sell', 'N/A'),
                        'last_active_timestamp': wallet_activity.get('last_active_timestamp', 0)
                    }

                    wallet_data.append(wallet_info)

                    # Step 3: Evaluate tokens traded by the wallet
                    for trade in wallet_activity.get('trades', []):
                        token_address = trade.get('token_address')
                        token_info, token_price = self.evaluate_token(token_address)
                        self.logger.info(f"Token Info for {token_address}: {token_info}")
                        self.logger.info(f"Token Price for {token_address}: {token_price}")

                    time.sleep(1)  # Rate limiting

            # Step 4: return data
            return wallet_data

            # Step 5: Print the analysis output
            #self.print_analysis_output(wallet_data)

        except Exception as e:
            self.logger.error(f"Error running strategy: {e}")


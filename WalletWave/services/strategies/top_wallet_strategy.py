from datetime import datetime
import logging
import time
from typing import List

from WalletWave.config import ConfigManager
from WalletWave.services.strategies.strategy_interface import StrategyInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.gmgn_client.schemas.wallet_info import WalletInfo
from WalletWave.utils.logging_utils import setup_logger
from WalletWave.utils.gmgn_client.utils.dataclass_transformer import to_dict


class TopWalletStrategy(StrategyInterface):
    """
    todo
    """
    def __init__(self, config_manager: ConfigManager):
        """
        Initializes the top_wallet_strategy object.

        """
        self.gmgn = GmgnRepo()
        self.logger = setup_logger("TopWalletStrategy", log_level=logging.INFO)
        self.config = config_manager
        self.timeframe = config_manager.timeframe
        self.wallet_tag = config_manager.wallet_tag
        self.win_rate = config_manager.win_rate

    def execute(self):
        return self.run_strategy()

    def get_top_wallets(self, timeframe="7d", wallet_tag="smart_degen"):
        """
        Fetch top performing wallets using the getTrendingWallets endpoint.

        :param timeframe: Time period for trending wallets (default "7d").
        :param wallet_tag: Tag to filter wallets (default "smart_degen").
        :return: List of top performing wallets.
        """
        try:
            response = self.gmgn.get_trending_wallets(timeframe, wallet_tag)
            return response.rank
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
            response = self.gmgn.get_wallet_info(wallet_address=wallet_address, period=period)
            return response
        except Exception as e:
            self.logger.error(f"Error analyzing wallet activity: {e}")
            return {}

    # todo: not being used. repurpose or remove
    def evaluate_token(self, token_address):
        """
        Evaluate a token using the getTokenInfo and getTokenUsdPrice endpoints.

        :param token_address: Address of the token to evaluate.
        :return: Token information and USD price.
        """
        try:
            token_info = self.gmgn.get_token_info(contract_address=token_address)
            # token_price = self.gmgn_client.getTokenUsdPrice(contract_address=token_address)
            return token_info, 3 # todo add token price
        except Exception as e:
            self.logger.error(f"Error evaluating token: {e}")
            return {}, {}

    def run_strategy(self):
        """
        Orchestrate the overall strategy execution.
        """
        try:
            # Step 1: Get top wallets
            top_wallets = self.get_top_wallets(timeframe=self.timeframe, wallet_tag=self.wallet_tag)
            if not top_wallets:
                self.logger.warning("No top wallets found.")
                return

            wallet_data: List[WalletInfo] = []

            # Step 2: Analyze each wallet's activity
            for wallet in top_wallets:
                wallet_address = wallet.wallet_address
                wallet_activity = self.analyze_wallet_activity(wallet_address, period=self.timeframe)

                # Check if wallet_activity is valid
                if not wallet_activity or not hasattr(wallet_activity, "to_summary"):
                    self.logger.warning(
                        f"Skipping wallet {wallet_address} due to empty or invalid activity data: {wallet_activity}")
                    continue

                # Log wallet activity data vertically
                self.logger.info(f"Wallet Activity for {wallet_address}:")
                self.logger.info(wallet_activity.to_summary(wallet_address))

                # Filter wallets with a win rate higher than configured win_rate
                winrate = wallet_activity.wallet_data.winrate
                if winrate is not None and winrate >= self.win_rate:
                    wallet_dict = to_dict(wallet_activity.wallet_data, extra_fields={"wallet_address": wallet_address})
                    wallet_data.append(wallet_dict)

                time.sleep(1)  # Rate limiting

            # Step 4: return data
            return wallet_data

        except Exception as e:
            self.logger.error(f"Error running strategy: {e}")


import logging
import time
from typing import List

from WalletWave.plugins.utils.plugin_interface import PluginInterface
from WalletWave.repositories.gmgn_repo import GmgnRepo
from WalletWave.utils.logging_utils import setup_logger
from WalletWave.config import ConfigManager

from WalletWave.utils.config_validators import *


def custom_summary(wallet_address, wallet_data):
    return {
        "wallet_address": wallet_address,
        "realized_profit": wallet_data.realized_profit,
        "buy": wallet_data.buy,
        "sell": wallet_data.sell,
        "total_value": wallet_data.total_value,
        "followers_count": wallet_data.followers_count,
        "winrate": wallet_data.winrate,
    }


class TopWallets(PluginInterface):

    def __init__(self, config_manager: ConfigManager):
        super().__init__(config_manager)
        self.plugin_settings = config_manager.TopWallets #dynamically get plugin settings
        self.gmgn = GmgnRepo()
        self.logger = setup_logger(self.plugin_class, log_level=logging.INFO)

    def get_name(self) -> str:
        return "Top Wallets"

    def get_description(self) -> str:
        return "Plugin that gathers Top performing wallets"

    def get_version(self) -> str:
        return "2.0.0"

    def initialize(self) -> None:
        self.logger.info("TopWallets plugin initialized.")

    def execute(self) -> any:
        """
        Execute the plugin
        """
        timeframe = validate_timeframe(self.plugin_settings.get("timeframe"))
        wallet_tag = validate_wallet_tag(self.plugin_settings.get("wallet_tag"))

        filtered_wallets = []
        try:
            # Step 1: Get the top wallets
            top_wallets = self.get_top_wallets(timeframe=timeframe, wallet_tag=wallet_tag)
            if not top_wallets:
                self.logger.warning("No top wallets found.")
                return []

            wallet_tuples = []

            # Step 2: Analyze each wallet activity
            for wallet in top_wallets:
                wallet_address = wallet.wallet_address
                wallet_activity = self.analyze_wallet_activity(wallet_address, period=timeframe)

                if not wallet_activity:
                    self.logger.warning(
                        f"Skipping wallet {wallet_address} due to empty or invalid data: {wallet_activity}"
                    )
                    continue

                # log wallet info
                self.logger.info(wallet_activity.to_summary(
                    wallet_address, summary_func=custom_summary)
                )

                # create a tuple that combines the activity and wallet address
                # wallet activity endpoint does not return the wallet address so we will combine it here
                wallet_tuples.append((wallet_activity, wallet_address))

            # Step 3: Filter wallets by winrate
            filtered_wallets = self.filter_by_winrate(wallet_tuples)

            # log the result
            self.logger.info(f"Filtered {len(filtered_wallets)} wallets.")

            time.sleep(1) #rate limiter
            return filtered_wallets

        except Exception as e:
            self.logger.error(f"Error running plugin: {e}")
            return filtered_wallets

    def finalize(self) -> None:
        self.logger.info("TopWallets plugin finalized")

    #custom function
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
            self.logger.error(f"Error analyzing: {e}")

    #custom function
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

    # custom function
    def filter_by_winrate(self, wallet_tuples: List[tuple]) -> List[dict]:
        """
        Filters wallets based on win rate and converts the result to a list of dictionaries.

        :param wallet_tuples: List of tuples (wallet_activity, wallet_address).
        :return: List of dictionaries with filtered wallet data.
        """
        user_defined_win_rate = validate_win_rate(self.plugin_settings.get("win_rate"))

        filtered_wallets = []

        self.logger.info(f"Searching for wallets that have a winrate greater than or equal to {user_defined_win_rate}")
        for wallet_activity, wallet_address in wallet_tuples:
            winrate = wallet_activity.wallet_data.winrate
            if winrate is not None and winrate >= user_defined_win_rate:
                wallet_dict = wallet_activity.to_summary(wallet_address)
                filtered_wallets.append(wallet_dict)
                self.logger.info(f"Wallet {wallet_address} passed with winrate: {winrate}.")
            else:
                self.logger.info(f"Wallet {wallet_address} failed with winrate: {winrate}.")

        return filtered_wallets

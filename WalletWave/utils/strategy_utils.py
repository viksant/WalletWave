from enum import Enum

from WalletWave.config import ConfigManager
from WalletWave.services.strategies.top_wallet_strategy import TopWalletStrategy


class StrategyTypes(Enum):
    TOP_WALLETS = "TopWalletsStrategy"

    @staticmethod
    def get_strategy(strategy_type, config: ConfigManager):
        if strategy_type == StrategyTypes.TOP_WALLETS:
            return TopWalletStrategy(config_manager=config)


class StrategyUtils:
    """
    todo
    """
    def __init__(self, config: ConfigManager, strategy: StrategyTypes):
        """
        Initializes the strategy_utils object.

        """
        self.strategy = StrategyTypes.get_strategy(strategy, config)

    def execute(self):
        return self.strategy.execute()






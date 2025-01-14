from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class TagRank:
    fresh_wallet: Optional[int] = None


@dataclass
class WalletInfo:
    twitter_bind: bool
    twitter_fans_num: int
    eth_balance: str
    sol_balance: str
    trx_balance: str
    balance: str
    total_value: float
    unrealized_profit: float
    unrealized_pnl: float
    realized_profit: float
    pnl: float
    pnl_7d: float
    pnl_30d: float
    realized_profit_7d: float
    realized_profit_30d: float
    all_pnl: float
    total_profit: float
    total_profit_pnl: float
    buy_30d: int
    sell_30d: int
    buy_7d: int
    sell_7d: int
    buy: int
    sell: int
    token_num: int
    profit_num: int
    pnl_lt_minus_dot5_num: int
    pnl_minus_dot5_0x_num: int
    pnl_lt_2x_num: int
    pnl_2x_5x_num: int
    pnl_gt_5x_num: int
    last_active_timestamp: int
    followers_count: int
    is_contract: bool
    updated_at: int
    avg_holding_peroid: float

    # Fields with default values
    token_avg_cost: Optional[float] = 0.0
    token_sold_avg_profit: Optional[float] = 0.0
    history_bought_cost: Optional[float] = 0.0
    winrate: Optional[float] = 0.0
    twitter_username: Optional[str] = None
    twitter_name: Optional[str] = None
    ens: Optional[str] = None
    avatar: Optional[str] = None
    name: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    tag_rank: TagRank = field(default_factory=TagRank)
    refresh_requested_at: Optional[int] = None


@dataclass
class WalletInfoResponse:
    code: int
    msg: str
    data: WalletInfo

    @property
    def wallet_data(self) -> WalletInfo:
        """
        Property to return the core wallet data.

        Returns:
            WalletInfo: The wallet data object.
        """
        return self.data

    def to_summary(self, wallet_address: str) -> dict:
        return {
            "wallet_address": wallet_address,
            "realized_profit": self.wallet_data.realized_profit,
            "buy": self.wallet_data.buy,
            "sell": self.wallet_data.sell,
            "last_active_stamp": self.wallet_data.last_active_timestamp,
            "winrate": self.wallet_data.winrate,
        }

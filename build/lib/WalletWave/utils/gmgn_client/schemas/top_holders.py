from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Status:
    hold: Optional[int] = None
    bought_more: Optional[int] = None
    sold_part: Optional[int] = None
    sold: Optional[int] = None
    transfered: Optional[int] = None
    bought_rate: Optional[str] = None
    holding_rate: Optional[str] = None
    top_10_holder_rate: Optional[float] = None
    smart_pos: List[str] = field(default_factory=list)
    smart_count_hold: Optional[int] = None
    smart_count_bought_more: Optional[int] = None
    smart_count_sold_part: Optional[int] = None
    smart_count_sold: Optional[int] = None
    smart_count_transfered: Optional[int] = None
    transfer_pos: List[str] = field(default_factory=list)

@dataclass
class HolderInfo:
    token_address: str
    wallet_address: str
    first_bought_amount: str
    first_bought_tax_amount: str
    buy_amount: str
    sell_amount: str
    is_fast_sniper: int
    balance: str
    history_bought_amount: str
    history_sold_amount: str
    status: str
    maker_token_tags: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

@dataclass
class HoldersData:
    chain: str
    holder_count: int
    statusNow: Status
    statusOld: Status
    sold_diff: int
    sold_part_diff: int
    hold_diff: int
    bought_more: int
    holderInfo: List[HolderInfo] = field(default_factory=list)

@dataclass
class TopHoldersResponse:
    code: int
    msg: str
    data: HoldersData




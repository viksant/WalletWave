from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class RouterInfo:
    """
    Represents the routing details for token swaps in the DeFi activity.

    Attributes:
        token1 (str): The first token in the swap.
        token1_decimals (int): The decimal places for the first token.
        amount1 (str): The amount of the first token in the swap.
        token2 (str): The second token in the swap.
        token2_decimals (int): The decimal places for the second token.
        amount2 (str): The amount of the second token in the swap.
    """
    token1: str
    token1_decimals: int
    amount1: str
    token2: str
    token2_decimals: int
    amount2: str

    @staticmethod
    def from_dict(obj: dict) -> 'RouterInfo':
        return RouterInfo(
            token1=str(obj["token1"]),
            token1_decimals=int(obj["token1_decimals"]),
            amount1=str(obj["amount1"]),
            token2=str(obj["token2"]),
            token2_decimals=int(obj["token2_decimals"]),
            amount2=str(obj["amount2"]),
        )

@dataclass
class AmountInfo:
    """
    Represents the token amount details in a DeFi activity.

    Attributes:
        token1 (str): The first token in the activity.
        token1_decimals (int): Decimal places for the first token.
        amount1 (int): The amount of the first token.
        token2 (str): The second token in the activity.
        token2_decimals (int): Decimal places for the second token.
        amount2 (int): The amount of the second token.
        routers (List[RouterInfo]): The list of routing details.
    """
    token1: str
    token1_decimals: int
    amount1: int
    token2: str
    token2_decimals: int
    amount2: int
    routers: List[RouterInfo]

    @staticmethod
    def from_dict(obj: dict) -> 'AmountInfo':
        return AmountInfo(
            token1=str(obj["token1"]),
            token1_decimals=int(obj["token1_decimals"]),
            amount1=int(obj["amount1"]),
            token2=str(obj["token2"]),
            token2_decimals=int(obj["token2_decimals"]),
            amount2=int(obj["amount2"]),
            routers=[RouterInfo.from_dict(router) for router in obj.get("routers", [])],
        )

@dataclass
class DefiActivity:
    """
    Represents a single DeFi activity in the Solscan API response.

    Attributes:
        block_id (int): The unique identifier of the block containing the activity.
        trans_id (str): The unique transaction identifier.
        block_time (int): The Unix timestamp of the block time.
        time (datetime): The ISO 8601 formatted datetime of the activity.
        activity_type (str): The type of DeFi activity.
        from_address (str): The Solana wallet address initiating the activity.
        to_address (str): The Solana wallet address involved in the activity.
        sources (List[str]): The list of source addresses for the activity.
        platform (str): The platform associated with the activity.
        amount_info (AmountInfo): Detailed information about token amounts in the activity.
    """
    block_id: int
    trans_id: str
    block_time: int
    time: datetime
    activity_type: str
    from_address: str
    to_address: str
    sources: List[str]
    platform: str
    amount_info: AmountInfo

    @staticmethod
    def from_dict(obj: dict) -> 'DefiActivity':
        return DefiActivity(
            block_id=int(obj["block_id"]),
            trans_id=str(obj["trans_id"]),
            block_time=int(obj["block_time"]),
            time=datetime.fromisoformat(obj["time"].replace("Z", "+00:00")),
            activity_type=str(obj["activity_type"]),
            from_address=str(obj["from_address"]),
            to_address=str(obj["to_address"]),
            sources=[str(source) for source in obj.get("sources", [])],
            platform=str(obj["platform"]),
            amount_info=AmountInfo.from_dict(obj["amount_info"]),
        )

from dataclasses import dataclass
from datetime import datetime

@dataclass
class BalanceChangeActivity:
    """
    Represents a balance change activity in the Solscan API response.

    Attributes:
        block_id (int): The unique identifier of the block containing the activity.
        block_time (int): The Unix timestamp of the block time.
        time (datetime): The ISO 8601 formatted datetime of the activity.
        trans_id (str): The unique transaction identifier.
        address (str): The Solana wallet address involved in the activity.
        token_address (str): The address of the token associated with the activity.
        token_account (str): The token account involved in the activity.
        token_decimals (int): The number of decimal places for the token.
        amount (int): The amount of the token involved in the balance change.
        pre_balance (int): The balance before the activity occurred.
        post_balance (int): The balance after the activity occurred.
        change_type (str): The type of balance change (e.g., 'inc' or 'dec').
        fee (int): The fee associated with the transaction.
    """

    block_id: int
    block_time: int
    time: datetime
    trans_id: str
    address: str
    token_address: str
    token_account: str
    token_decimals: int
    amount: int
    pre_balance: int
    post_balance: int
    change_type: str
    fee: int

    @staticmethod
    def from_dict(obj: dict) -> 'BalanceChangeActivity':
        """
        Creates a BalanceChangeActivity instance from a dictionary.

        Args:
            obj (dict): A dictionary representation of the BalanceChangeActivity.

        Returns:
            BalanceChangeActivity: An instance of BalanceChangeActivity.
        """
        return BalanceChangeActivity(
            block_id=int(obj["block_id"]),
            block_time=int(obj["block_time"]),
            time=datetime.fromisoformat(obj["time"].replace("Z", "+00:00")),
            trans_id=str(obj["trans_id"]),
            address=str(obj["address"]),
            token_address=str(obj["token_address"]),
            token_account=str(obj["token_account"]),
            token_decimals=int(obj["token_decimals"]),
            amount=int(obj["amount"]),
            pre_balance=int(obj["pre_balance"]),
            post_balance=int(obj["post_balance"]),
            change_type=str(obj["change_type"]),
            fee=int(obj["fee"]),
        )

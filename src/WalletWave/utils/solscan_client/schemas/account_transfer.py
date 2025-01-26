from dataclasses import dataclass
from datetime import datetime


@dataclass
class AccountTransfer:
    """
    Represents a single account transfer in the Solscan API response.

    Attributes:
        block_id (int): The unique identifier of the block containing the transaction.
        trans_id (str): The unique identifier of the transaction.
        block_time (int): The Unix timestamp when the block was created.
        time (datetime): The ISO 8601 formatted datetime of the transaction.
        activity_type (str): The type of activity, e.g., 'ACTIVITY_SPL_TRANSFER'.
        from_address (str): The Solana wallet address initiating the transfer.
        to_address (str): The Solana wallet address receiving the transfer.
        token_address (str): The address of the token being transferred.
        token_decimals (int): The number of decimal places for the token.
        amount (int): The amount of tokens transferred, in smallest units.
        flow (str): Indicates whether the flow of funds is 'in' or 'out'.
    """

    block_id: int
    trans_id: str
    block_time: int
    time: datetime
    activity_type: str
    from_address: str
    to_address: str
    token_address: str
    token_decimals: int
    amount: int
    flow: str

    @staticmethod
    def from_dict(obj: dict) -> 'AccountTransfer':
        """
        Creates an AccountTransfer instance from a dictionary.

        Args:
            obj (dict): A dictionary representation of the AccountTransfer.

        Returns:
            AccountTransfer: An instance of AccountTransfer.
        """
        return AccountTransfer(
            block_id=int(obj["block_id"]),
            trans_id=str(obj["trans_id"]),
            block_time=int(obj["block_time"]),
            time=datetime.fromisoformat(obj["time"].replace("Z", "+00:00")),
            activity_type=str(obj["activity_type"]),
            from_address=str(obj["from_address"]),
            to_address=str(obj["to_address"]),
            token_address=str(obj["token_address"]),
            token_decimals=int(obj["token_decimals"]),
            amount=int(obj["amount"]),
            flow=str(obj["flow"]),
        )

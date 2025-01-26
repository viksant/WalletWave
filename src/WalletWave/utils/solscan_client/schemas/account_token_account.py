from dataclasses import dataclass

@dataclass
class AccountTokenAccount:
    """
    Represents a token account in the Solscan API response.

    Attributes:
        token_account (str): The unique identifier of the token account.
        token_address (str): The address of the token associated with the account.
        amount (int): The amount of tokens in the account, in smallest units.
        token_decimals (int): The number of decimal places for the token.
        owner (str): The Solana wallet address that owns the token account.
    """

    token_account: str
    token_address: str
    amount: int
    token_decimals: int
    owner: str

    @staticmethod
    def from_dict(obj: dict) -> 'AccountTokenAccount':
        """
        Creates an AccountTokenAccount instance from a dictionary.

        Args:
            obj (dict): A dictionary representation of the AccountTokenAccount.

        Returns:
            AccountTokenAccount: An instance of AccountTokenAccount.
        """
        return AccountTokenAccount(
            token_account=str(obj["token_account"]),
            token_address=str(obj["token_address"]),
            amount=int(obj["amount"]),
            token_decimals=int(obj["token_decimals"]),
            owner=str(obj["owner"]),
        )

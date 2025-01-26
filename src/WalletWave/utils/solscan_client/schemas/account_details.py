from dataclasses import dataclass

@dataclass
class AccountDetail:
    """
    Represents the detailed information of an account in the Solscan API response.

    Attributes:
        account (str): The public key of the account.
        lamports (int): The number of lamports in the account.
        type (str): The type of the account (e.g., "system_account").
        executable (bool): Indicates whether the account is executable.
        owner_program (str): The public key of the program owning the account.
        rent_epoch (int): The epoch at which the account will be exempt from rent.
        is_oncurve (bool): Indicates whether the account is an on-curve address.
    """

    account: str
    lamports: int
    type: str
    executable: bool
    owner_program: str
    rent_epoch: int
    is_oncurve: bool

    @staticmethod
    def from_dict(obj: dict) -> 'AccountDetail':
        """
        Creates an AccountDetail instance from a dictionary.

        Args:
            obj (dict): A dictionary representation of the AccountDetail.

        Returns:
            AccountDetail: An instance of AccountDetail.
        """
        return AccountDetail(
            account=str(obj["account"]),
            lamports=int(obj["lamports"]),
            type=str(obj["type"]),
            executable=bool(obj["executable"]),
            owner_program=str(obj["owner_program"]),
            rent_epoch=int(obj["rent_epoch"]),
            is_oncurve=bool(obj["is_oncurve"]),
        )

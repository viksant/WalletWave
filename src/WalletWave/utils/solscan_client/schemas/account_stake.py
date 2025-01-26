from dataclasses import dataclass
from typing import List

@dataclass
class StakeAccount:
    """
    Represents a stake account in the Solscan API response.

    Attributes:
        amount (int): The total amount of stake in the account.
        role (List[str]): The roles associated with the account (e.g., "staker", "withdrawer").
        status (str): The status of the stake account (e.g., "active").
        type (str): The type of the stake account (e.g., "active").
        voter (str): The public key of the voter account associated with the stake.
        active_stake_amount (int): The amount of actively staked tokens.
        delegated_stake_amount (int): The amount of delegated stake.
        sol_balance (int): The SOL balance of the stake account.
        total_reward (str): The total reward earned by the stake account.
        stake_account (str): The public key of the stake account.
        activation_epoch (int): The epoch at which the stake was activated.
        stake_type (int): The type of the stake account (usually an integer identifier).
    """

    amount: int
    role: List[str]
    status: str
    type: str
    voter: str
    active_stake_amount: int
    delegated_stake_amount: int
    sol_balance: int
    total_reward: str
    stake_account: str
    activation_epoch: int
    stake_type: int

    @staticmethod
    def from_dict(obj: dict) -> 'StakeAccount':
        """
        Creates a StakeAccount instance from a dictionary.

        Args:
            obj (dict): A dictionary representation of the StakeAccount.

        Returns:
            StakeAccount: An instance of StakeAccount.
        """
        return StakeAccount(
            amount=int(obj["amount"]),
            role=[str(r) for r in obj["role"]],
            status=str(obj["status"]),
            type=str(obj["type"]),
            voter=str(obj["voter"]),
            active_stake_amount=int(obj["active_stake_amount"]),
            delegated_stake_amount=int(obj["delegated_stake_amount"]),
            sol_balance=int(obj["sol_balance"]),
            total_reward=str(obj["total_reward"]),
            stake_account=str(obj["stake_account"]),
            activation_epoch=int(obj["activation_epoch"]),
            stake_type=int(obj["stake_type"]),
        )

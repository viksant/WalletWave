from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass
class ParsedInstruction:
    """
    Represents a single parsed instruction in a transaction.

    Attributes:
        type (str): The type of instruction (e.g., "cancelAllAndPlaceOrders").
        program (str): The program involved in the instruction (e.g., "openbook_v2").
        program_id (str): The program ID of the instruction.
    """
    type: str
    program: str
    program_id: str

    @staticmethod
    def from_dict(obj: dict) -> 'ParsedInstruction':
        return ParsedInstruction(
            type=str(obj["type"]),
            program=str(obj["program"]),
            program_id=str(obj["program_id"]),
        )

@dataclass
class AccountTransaction:
    """
    Represents a single transaction for a Solana account.

    Attributes:
        slot (int): The slot number of the transaction.
        fee (int): The fee paid for the transaction.
        status (str): The status of the transaction (e.g., "Success", "Fail").
        signer (List[str]): The list of signer wallet addresses.
        block_time (int): The Unix timestamp of the block time.
        tx_hash (str): The hash of the transaction.
        parsed_instructions (List[ParsedInstruction]): The list of parsed instructions in the transaction.
        program_ids (List[str]): The list of program IDs involved in the transaction.
        time (datetime): The ISO 8601 formatted datetime of the transaction.
    """
    slot: int
    fee: int
    status: str
    signer: List[str]
    block_time: int
    tx_hash: str
    parsed_instructions: List[ParsedInstruction]
    program_ids: List[str]
    time: datetime

    @staticmethod
    def from_dict(obj: dict) -> 'AccountTransaction':
        return AccountTransaction(
            slot=int(obj["slot"]),
            fee=int(obj["fee"]),
            status=str(obj["status"]),
            signer=[str(s) for s in obj["signer"]],
            block_time=int(obj["block_time"]),
            tx_hash=str(obj["tx_hash"]),
            parsed_instructions=[
                ParsedInstruction.from_dict(instr)
                for instr in obj.get("parsed_instructions", [])
            ],
            program_ids=[str(pid) for pid in obj.get("program_ids", [])],
            time=datetime.fromisoformat(obj["time"].replace("Z", "+00:00")),
        )

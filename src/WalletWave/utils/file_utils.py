import os
import csv
import logging
from datetime import datetime
from dataclasses import asdict
from pathlib import Path

from WalletWave.utils.formatting_utils import format_timestamp, format_percentage, format_currency
from WalletWave.utils.logging_utils import setup_logger


def _apply_formatting(item: dict) -> dict:
    """
    Applies formatting based on field names.

    :param item: A dictionary representing a single data entry.
    :return: A dictionary with formatted values.
    """
    formatted_item = {}
    for key, value in item.items():
        if "timestamp" in key or "date" in key:
            formatted_item[key] = format_timestamp(value) if value else value
        elif any(keyword in key for keyword in ["winrate", "pnl"]):
            formatted_item[key] = format_percentage(value) if value is not None else value
        elif any(keyword in key for keyword in ["profit", "value", "cost"]):
            formatted_item[key] = format_currency(value) if value is not None else value
        else:
            formatted_item[key] = value
    return formatted_item


class FileUtils:
    """
        A utility module to handle import and exports of data to/from files
    """
    def __init__(self, export_path: str, import_path: str = None):
        self.export_path = Path(export_path)
        self.import_path = Path(import_path) if import_path else None
        self.logger = setup_logger("FileUtils", log_level=logging.INFO)

    def _generate_file_path(self, export_format: str, timestamp_format: str) -> Path:
        timestamp = datetime.now().strftime(timestamp_format)
        file_name = f"wallet_list_{timestamp}.{export_format}"
        return self.export_path / file_name

    def export_wallet_data(self, data: list, export_format: str, timestamp_format: str = "%Y%m%d_%H%M%S"):
        """
        Export the wallet analysis data to the specified format.

        :param data: List of wallet data dictionaries.
        :param export_format: csv or txt file format.
        :param timestamp_format: Format string for the timestamp in the filename (default: "%Y%m%d_%H%M%S").
        """
        if not data:
            self.logger.warning("No data to export")
            return

        # Convert all entries to dictionaries and apply formatting in one step
        data_dicts = [
            _apply_formatting(asdict(entry)) if hasattr(entry, "__dataclass_fields__") else _apply_formatting(entry)
            for entry in data
        ]

        # Make sure the export dir exists
        self.export_path.mkdir(parents=True, exist_ok=True)

        # Generate file export_path
        file_path = self._generate_file_path(export_format, timestamp_format)

        if export_format == "csv":
            with file_path.open(mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data_dicts[0].keys())
                writer.writeheader()
                writer.writerows(data_dicts)
        elif export_format == "txt":
            with file_path.open(mode="w", encoding="utf-8") as file:
                for wallet in data_dicts:
                    for key, value in wallet.items():
                        file.write(f"{key}: {value}\n")
                    file.write("\n")
        else:
            self.logger.error(f"Unsupported export format: {export_format}")
            return

        self.logger.info(f"Exporting {len(data_dicts)} entries to {export_format} format.")
        self.logger.info(f"Data exported successfully to {file_path}")




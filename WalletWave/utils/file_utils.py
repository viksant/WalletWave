import os
import csv
import logging
from datetime import datetime


class FileUtils:
    """
        A utility module to handle import and exports of data to/from files
    """
    def __init__(self, export_path, import_path = None):
        self.export_path = export_path
        self.import_path = import_path
        self.logger = logging.getLogger("FileUtils")
        logging.basicConfig(level=logging.INFO)

    def export_wallet_data(self, data, export_format):
        """
        Export the wallet analysis data to the specified format.

        :param data: List of wallet data dictionaries.
        :param export_format: csv or txt file format
        """
        file_path = ""
        if not data:
            self.logger.warning("No data to export")
            return

        os.makedirs(self.export_path, exist_ok=True)

        if export_format == "csv":
            file_path = os.path.join(self.export_path, f"wallet_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            with open(file_path, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        elif export_format == "txt":
            file_path = os.path.join(self.export_path, f"wallet_list_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            with open(file_path, mode="w") as file:
                for wallet in data:
                    for key, value in wallet.items():
                        file.write(f"{key}: {value}\n")
                    file.write("\n")

        print(f"Data exported to {file_path if file_path else self.export_path}")




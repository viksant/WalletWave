from WalletWave.utils.gmgn_client.client import Gmgn
from WalletWave.utils.gmgn_client.utils.gmgn_endpoints import GmgnEndpoints
from typing import Optional, Dict, Any

class GmgnRepo:
    def __init__(self):
        """
        Initializes the GmgnRepo object.
        """
        self.client = Gmgn()
        self.endpoint = GmgnEndpoints


    def get_trending_wallets(self, timeframe: str, wallet_tag: str, order: str = "desc") -> dict:
        """
        Fetches trending wallets for a given timeframe and wallet tag.

        Args:
            timeframe (str): The timeframe for trending wallets (e.g., "1d", "7d", "30d").
            wallet_tag (str): The wallet tag to filter by (e.g., "smart_degen").
            order (str): Order to sort the wallets ("desc", "asc") Default: "desc"

        Returns:
            dict: The response from the GMGN API containing trending wallet data.

        Raises:
            ValueError: If the provided timeframe or wallet tag is invalid.
        """
        valid_timeframes = ["1d", "7d", "30d"]
        valid_wallet_tags = ["all", "pump_smart", "smart_degen", "reowned", "snipe_bot"]

        if timeframe not in valid_timeframes or wallet_tag not in valid_wallet_tags:
            raise ValueError("Invalid timeframe or wallet tag")

        params = {
            "tag": wallet_tag,
            "orderby": f"pnl_{timeframe}",
            "direction": order,
        }

        # Build the endpoint URL
        url = self.endpoint.get_url(self.endpoint.TRENDING_WALLETS, timeframe=timeframe)

        # Make the request
        return self.client.make_request(url, params)

    def get_token_info(self, contract_address: str) -> dict:
        if not contract_address:
            raise ValueError("Must provide a contract address")
        url = self.endpoint.get_url(self.endpoint.TOKEN_INFO, contract_address=contract_address)

        #make request
        return self.client.make_request(url)

    def get_wallet_info(self, wallet_address: str, period: str = "7d") -> dict:
        valid_periods = ["7d", "30d"]
        if not wallet_address:
            raise ValueError("Must provide a wallet address")
        if period not in valid_periods:
            raise ValueError(f"Invalid period: {period}")

        params = {"period": period}

        url = self.endpoint.get_url(self.endpoint.WALLET_INFO, wallet_address=wallet_address)

        return self.client.make_request(url, params)





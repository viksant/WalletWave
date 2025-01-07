import random
import tls_client
from fake_useragent import UserAgent
from typing import Optional, Dict, Any
from requests.exceptions import HTTPError

from WalletWave.utils.config_validators import validate_wallet_tag

# TODO: Implement additional features like fetching transaction history or token analytics if supported by the API.
# TODO: Add support for other blockchain networks in addition to Solana.
# TODO: Create a CLI or web-based interface for interacting with the `Gmgn` class.
# TODO: Explore multithreading or async requests to improve performance for concurrent API calls.
# TODO: Add pagination handling for endpoints that return large datasets.
# TODO: Consider integrating database support (e.g., SQLite, PostgreSQL) for persistent storage of API responses.

class AgentMapper:
    """
    Maps tls_client client_identifiers to corresponding user-agents and platforms
    with realistic operating system alignment.
    """

    # TODO: Expand `identifier_mapping` to include more browser and platform options if needed.
    # TODO: Add logging for debugging when generating user-agent strings.
    # TODO: Write unit tests for `AgentMapper` to ensure correct mapping and user-agent generation.
    # TODO: Consider caching user-agent results to improve performance if the same identifier is used multiple times.

    def __init__(self):
        # Mapping of tls_client identifiers to browser, platform, and OS
        self.identifier_mapping = {
            # Chrome (desktop only)
            **{
                f"chrome_{version}": {
                    "browser": "Chrome",
                    "platform": "desktop",
                    "os": "Windows",
                }
                for version in range(103, 121)
            },
            # Safari (desktop only)
            "safari_15_6_1": {"browser": "Safari", "platform": "desktop", "os": "Mac OS X"},
            "safari_16_0": {"browser": "Safari", "platform": "desktop", "os": "Mac OS X"},
            # iOS (Safari)
            "safari_ios_15_5": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            "safari_ios_15_6": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            "safari_ios_16_0": {"browser": "Mobile Safari", "platform": "mobile", "os": "iOS"},
            # Firefox (desktop only)
            **{
                f"firefox_{version}": {
                    "browser": "Firefox",
                    "platform": "desktop",
                    "os": "Linux",
                }
                for version in [102, 104, 105, 106, 108, 110, 117, 120]
            },
            # Opera (desktop only)
            "opera_89": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            "opera_90": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            "opera_91": {"browser": "Opera", "platform": "desktop", "os": "Windows"},
            # OkHttp (Android)
            **{
                f"okhttp4_android_{version}": {
                    "browser": "Chrome Mobile",
                    "platform": "mobile",
                    "os": "Android",
                }
                for version in range(7, 14)
            },
        }

    def get_user_agent(self, client_identifier: str) -> str:
        # validate client_identifier
        mapping = self.identifier_mapping.get(client_identifier)
        if not mapping:
            raise ValueError(f"Unsupported client identifier: {client_identifier}")

        browser = mapping["browser"]
        platform = mapping["platform"]
        os_type = mapping["os"]

        # generate user-agent
        ua = UserAgent(browsers=[browser], platforms=[platform], os=[os_type])
        return ua.random

    def get_random_client_and_agent(self) -> tuple[str, str]:
        # choose a random client_identifier and generate matching user-agent
        client_identifier = random.choice(list(self.identifier_mapping.keys()))
        user_agent = self.get_user_agent(client_identifier)
        return client_identifier, user_agent


class Gmgn:
    BASE_URL = "https://gmgn.ai/defi/quotation"

    # TODO: Add logging to track successful and failed API requests.
    # TODO: Write unit tests for all `Gmgn` methods (e.g., `get_token_info`, `get_trending_wallets`, `get_wallet_info`).
    # TODO: Consolidate validation logic (e.g., for `timeframe`, `wallet_tag`, `period`) into reusable utility functions.
    # TODO: Add retries for `_make_request` to handle transient network errors or timeouts.
    # TODO: Add an optional timeout parameter to `_make_request` for better control over request time.
    # TODO: Refactor `_generate_headers` to allow more dynamic header configurations if needed in the future.
    # TODO: Modularize the code into separate files (e.g., `agent_mapper.py`, `gmgn.py`, `validators.py`) for better maintainability.
    # TODO: Implement caching for frequently accessed endpoints (e.g., `get_token_info`) to reduce API load.
    # TODO: Add detailed docstrings for all methods to ensure clarity for future developers.
    # TODO: Validate wallet address format in `get_wallet_info` to avoid unnecessary API calls.
    # TODO: Explore rate-limiting compliance for `gmgn.ai` API to avoid potential issues. (2 seconds)

    def __init__(self):
        self.agent_mapper = AgentMapper
        self.session = tls_client.Session(random_tls_extension_order=True)
        self.client, self.agent = self.agent_mapper.get_random_client_and_agent()
        self.headers = self._generate_headers()

    def _generate_headers(self) -> Dict[str, str]:
        return {
            "Host": "gmgn.ai",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.9",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": "https://gmgn.ai/?chain=sol",
            "user-agent": self.agent,
        }

    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
        url = f"{self.BASE_URL}{endpoint}"
        try:
            response = self.session.get(url, headers=self.headers, params=params)

            if response.status_code >= 400:
                raise RuntimeError(f"HTTP error {response.status_code}: {response.text}")

            return response.json()
        except Exception as err:
            raise RuntimeError(f"Request failed: {err}")

    def get_token_info(self, contract_address: str) -> dict:
        if not contract_address:
            raise ValueError("Must provide a contract address")
        return self._make_request(f"/v1/tokens/sol/{contract_address}")

    def get_trending_wallets(self, timeframe: str = "7d", wallet_tag: str = "smart_degen") -> dict:
        valid_timeframes = ["1d", "7d", "30d"]
        valid_wallet_tags = ["all", "pump_smart", "smart_degen", "reowned", "snipe_bot"]

        if timeframe not in valid_timeframes or wallet_tag not in valid_wallet_tags:
            raise ValueError("Invalid timeframe or wallet tag")

        params = {
            "tag": wallet_tag,
            "orderby": f"pnl_{timeframe}",
            "direction": "desc",
        }

        return self._make_request(f"/v1/rank/sol/wallets/{timeframe}", params)

    def get_wallet_info(self, wallet_address: str, period: str = "7d") -> dict:
        valid_periods = ["7d", "30d"]
        if not wallet_address:
            raise ValueError("Must provide a wallet address")
        if period not in valid_periods:
            raise ValueError(f"Invalid period: {period}")

        params = {"period": period}
        return self._make_request(f"/v1/smartmoney/sol/walletNew/{wallet_address}", params)

if __name__ == "__main__":
    agent_mapper = AgentMapper()
    client, agent = agent_mapper.get_random_client_and_agent()
    print(f"Client Identifier: {client}")
    print(f"User-Agent: {agent}")
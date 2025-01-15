import logging
import random
import tls_client
from typing import Optional, Dict, Any
import time

from WalletWave.utils.gmgn_client.utils.agent_mapper import AgentMapper
from WalletWave.utils.logging_utils import setup_logger


# TODO: Implement additional features like fetching transaction history or token analytics if supported by the API.
# TODO: Add support for other blockchain networks in addition to Solana.
# TODO: Create a CLI or web-based interface for interacting with the `Gmgn` class.
# TODO: Explore multithreading or async requests to improve performance for concurrent API calls.
# TODO: Add pagination handling for endpoints that return large datasets.
# TODO: Consider integrating database support (e.g., SQLite, PostgreSQL) for persistent storage of API responses.

class Gmgn:
    # TODO: Add logging to track successful and failed API requests.
    # TODO: Write unit tests for all `Gmgn` methods (e.g., `get_token_info`, `get_trending_wallets`, `get_wallet_info`).
    # TODO: Consolidate validation logic (e.g., for `timeframe`, `wallet_tag`, `period`) into reusable utility functions.
    # TODO: Add retries for `_make_request` to handle transient network errors or timeouts.
    # TODO: Add an optional timeout parameter to `_make_request` for better control over request time.
    # TODO: Refactor `_generate_headers` to allow more dynamic header configurations if needed in the future.
    # TODO: Modularize the code into separate files (e.g., `agent_mapper.py`, `gmgn_client.py`, `validators.py`) for better maintainability.
    # TODO: Implement caching for frequently accessed endpoints (e.g., `get_token_info`) to reduce API load.
    # TODO: Add detailed docstrings for all methods to ensure clarity for future developers.
    # TODO: Validate wallet address format in `get_wallet_info` to avoid unnecessary API calls.
    # TODO: Explore rate-limiting compliance for `gmgn_client.ai` API to avoid potential issues. (2 seconds)

    def __init__(self, max_requests_range: tuple = (1, 10)):
        self.logger = setup_logger("Gmgn Client", log_level=logging.INFO)
        self.agent_mapper = AgentMapper()
        self.session = tls_client.Session(random_tls_extension_order=True)
        self.client, self.agent, self.headers = None, None, None
        self.request_count = 0
        self.max_requests_range = max_requests_range
        self.max_requests = random.randint(*self.max_requests_range)
        self.error_count = 0

        self.logger.debug("Initiating Gmgn Client...")
        self._rotate_headers()

    def _generate_headers(self) -> Dict[str, str]:
        self.logger.debug("Generating headers for the request.")
        return {
            "Host": "gmgn_client.ai",
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "dnt": "1",
            "priority": "u=1, i",
            "referer": "https://gmgn.ai/?chain=sol",
            "user-agent": self.agent,
        }

    def _rotate_headers(self):
        # todo add timeout method
        self.client, self.agent = self.agent_mapper.get_random_client_and_agent()
        self.headers = self._generate_headers()

    def _clear_cookies(self):
        self.logger.warning("Lets destroy cookies!")
        self.session.cookies.clear()
        self.logger.info("Cookies cleared...")

    def make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> dict:
        url = endpoint
        self.logger.debug(f"Preparing request to URL: {url} with params: {params}")

        try:
            self.request_count += 1
            if self.request_count % self.max_requests == 0:
                self.logger.info("Max requests reached, rotating headers...")
                self._rotate_headers()
                self.logger.info(f"Rotated Headers -> Client: {self.client}, User-Agent: {self.agent}")
                self.max_requests = random.randint(*self.max_requests_range)
                self.request_count = 0


            time.sleep(2)
            self.logger.debug("Sending request...")
            response = self.session.get(url, headers=self.headers, params=params)

            # rotate on rate-limit or block errors
            if response.status_code in [429, 403]:
                self.error_count += 1
                self.logger.warning(f"Received HTTP {response.status_code}, rotating headers and retrying...")
                self._rotate_headers()
                if self.error_count == 3:
                    self.logger.error("Multiple consecutive failures, clearing cookies and retrying...")
                    self._clear_cookies()
                    self.error_count = 0
                time.sleep(random.randint(5, 10)) # backoff
                return self.make_request(endpoint, params)

            if response.status_code >= 400:
                raise RuntimeError(f"HTTP error {response.status_code}: {response.text}")

            self.logger.info(f"Request to {url} completed successfully.")
            return response.json()
        except Exception as err:
            raise RuntimeError(f"Request failed: {err}")

if __name__ == "__main__":
    agent_mapper = AgentMapper()
    client, agent = agent_mapper.get_random_client_and_agent()
    print(f"Client Identifier: {client}")
    print(f"User-Agent: {agent}")
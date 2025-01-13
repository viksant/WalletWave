import random
from fake_useragent import UserAgent

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
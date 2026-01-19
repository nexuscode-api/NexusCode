import yaml
import random
from typing import Dict, Optional, List

class KeyRotator:
    """
    Manages the lifecycle, validation, and rotation of API keys.
    """

    def __init__(self, key_pool_path: str):
        self.key_pool_path = key_pool_path
        self.pool = self._load_pool()

    def _load_pool(self) -> List[Dict]:
        """Loads the key pool configuration from YAML file."""
        try:
            with open(self.key_pool_path, 'r') as file:
                data = yaml.safe_load(file)
                return data.get('pool', [])
        except Exception as e:
            print(f"[!] Critical Error loading KeyPool: {e}")
            return []

    def get_best_candidate(self, preferred_provider: str = None) -> Optional[Dict]:
        """
        Selects the best available API key based on latency and status.
        Algorithm:
        1. Filter by ACTIVE status.
        2. If provider specified, filter by provider.
        3. Sort by latency (ascending).
        4. Return top candidate.
        """
        # Filter only active keys
        candidates = [k for k in self.pool if k['status'] == 'ACTIVE']

        if not candidates:
            return None

        # If user wants specific provider (e.g., 'OpenAI')
        if preferred_provider:
            provider_candidates = [k for k in candidates if k['provider'].lower() == preferred_provider.lower()]
            if provider_candidates:
                candidates = provider_candidates

        # Sort by lowest latency (fastest response)
        candidates.sort(key=lambda x: x.get('latency_ms', 9999))
        
        return candidates[0]

    def report_status(self, key_signature: str, new_status: str):
        """
        Updates the status of a key (e.g., if Rate Limit is hit during use).
        In a real app, this would write back to the DB or YAML.
        """
        for key in self.pool:
            # Identifying key by partial signature for security
            if key['api_key'] == key_signature:
                key['status'] = new_status
                break

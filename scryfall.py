import requests
import time
from typing import Optional, Dict, List, Any


class ScryfallClient:
    BASE_URL = "https://api.scryfall.com"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'MTG-Card-Search/1.0'
        })
    
    def search_cards(self, query: str, page: int = 1) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/cards/search"
        params = {
            'q': query,
            'page': page
        }
        return self._request_with_retry(url, params)
    
    def _request_with_retry(self, url: str, params: Optional[Dict] = None, max_retries: int = 3) -> Dict[str, Any]:
        for attempt in range(max_retries):
            try:
                time.sleep(0.1)
                response = self.session.get(url, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 503 and attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"API unavailable, retrying in {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                raise
        raise Exception("Max retries exceeded")
    
    def get_named_card(self, name: str, fuzzy: bool = True) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/cards/named"
        params = {'fuzzy' if fuzzy else 'exact': name}
        return self._request_with_retry(url, params)
    
    def random_card(self) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/cards/random"
        return self._request_with_retry(url)

    def get_card_by_id(self, scryfall_id: str) -> Dict[str, Any]:
        """Get a card by its Scryfall ID."""
        url = f"{self.BASE_URL}/cards/{scryfall_id}"
        return self._request_with_retry(url)

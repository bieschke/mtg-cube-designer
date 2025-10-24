"""
Collection manager for analyzing and filtering MTG cards from a CSV export.

This module helps explore an existing card collection, with smart caching
to respect Scryfall API rate limits.
"""

import csv
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Set
from dataclasses import dataclass
from scryfall import ScryfallClient


@dataclass
class Card:
    """Represents a card in the collection with enriched Scryfall data."""
    name: str
    quantity: int
    scryfall_id: str

    # Enriched data from Scryfall
    colors: List[str] = None
    color_identity: List[str] = None
    mana_cost: str = None
    cmc: float = 0.0
    type_line: str = ""
    oracle_text: str = ""
    power: str = None
    toughness: str = None
    keywords: List[str] = None
    rarity: str = ""
    set_name: str = ""

    def __post_init__(self):
        """Initialize mutable defaults."""
        if self.colors is None:
            self.colors = []
        if self.color_identity is None:
            self.color_identity = []
        if self.keywords is None:
            self.keywords = []

    @property
    def is_creature(self) -> bool:
        """Check if card is a creature."""
        return "Creature" in self.type_line

    @property
    def is_instant(self) -> bool:
        """Check if card is an instant."""
        return "Instant" in self.type_line

    @property
    def is_sorcery(self) -> bool:
        """Check if card is a sorcery."""
        return "Sorcery" in self.type_line

    @property
    def is_artifact(self) -> bool:
        """Check if card is an artifact."""
        return "Artifact" in self.type_line

    @property
    def is_enchantment(self) -> bool:
        """Check if card is an enchantment."""
        return "Enchantment" in self.type_line

    @property
    def is_planeswalker(self) -> bool:
        """Check if card is a planeswalker."""
        return "Planeswalker" in self.type_line

    @property
    def is_land(self) -> bool:
        """Check if card is a land."""
        return "Land" in self.type_line

    @property
    def is_multicolor(self) -> bool:
        """Check if card is multicolor."""
        return len(self.colors) > 1


class Collection:
    """Manages a card collection with smart caching and filtering."""

    CACHE_FILE = "collection_cache.json"

    def __init__(self, csv_path: str):
        """Initialize collection from CSV export."""
        self.csv_path = csv_path
        self.cards: List[Card] = []
        self.scryfall = ScryfallClient()
        self.cache_path = Path(__file__).parent / self.CACHE_FILE
        self._load_collection()

    def _load_collection(self):
        """Load collection from CSV and enrich with cached Scryfall data."""
        print(f"Loading collection from {self.csv_path}...")

        # Load cache if it exists
        cache = self._load_cache()

        # Parse CSV
        raw_cards = []
        with open(self.csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_cards.append({
                    'name': row['Name'],
                    'quantity': int(row['Quantity']),
                    'scryfall_id': row['Scryfall ID']
                })

        print(f"Found {len(raw_cards)} unique cards ({sum(c['quantity'] for c in raw_cards)} total)")

        # Enrich with Scryfall data
        needs_fetch = []
        for raw_card in raw_cards:
            scryfall_id = raw_card['scryfall_id']

            if scryfall_id in cache:
                # Use cached data
                card_data = cache[scryfall_id]
            else:
                # Need to fetch from API
                needs_fetch.append(raw_card)
                continue

            card = self._create_card_from_data(raw_card, card_data)
            self.cards.append(card)

        # Fetch missing cards from Scryfall
        if needs_fetch:
            print(f"\nFetching {len(needs_fetch)} cards from Scryfall...")
            self._fetch_and_cache_cards(needs_fetch, cache)

        print(f"✓ Collection loaded: {len(self.cards)} cards ready\n")

    def _fetch_and_cache_cards(self, cards_to_fetch: List[Dict], cache: Dict):
        """Fetch missing cards from Scryfall and update cache."""
        for i, raw_card in enumerate(cards_to_fetch, 1):
            scryfall_id = raw_card['scryfall_id']

            # Fetch from API with rate limiting
            try:
                response = self.scryfall.get_card_by_id(scryfall_id)

                # Cache the response
                cache[scryfall_id] = response

                # Create card
                card = self._create_card_from_data(raw_card, response)
                self.cards.append(card)

                # Progress indicator
                if i % 10 == 0:
                    print(f"  Fetched {i}/{len(cards_to_fetch)} cards...")

                # Rate limiting: Scryfall allows ~10 requests/second
                time.sleep(0.1)

            except Exception as e:
                print(f"  Warning: Could not fetch {raw_card['name']}: {e}")

        # Save updated cache
        self._save_cache(cache)
        print(f"  Cache updated!\n")

    def _create_card_from_data(self, raw_card: Dict, scryfall_data: Dict) -> Card:
        """Create a Card object from raw CSV data and Scryfall response."""
        return Card(
            name=raw_card['name'],
            quantity=raw_card['quantity'],
            scryfall_id=raw_card['scryfall_id'],
            colors=scryfall_data.get('colors', []),
            color_identity=scryfall_data.get('color_identity', []),
            mana_cost=scryfall_data.get('mana_cost', ''),
            cmc=scryfall_data.get('cmc', 0),
            type_line=scryfall_data.get('type_line', ''),
            oracle_text=scryfall_data.get('oracle_text', ''),
            power=scryfall_data.get('power'),
            toughness=scryfall_data.get('toughness'),
            keywords=scryfall_data.get('keywords', []),
            rarity=scryfall_data.get('rarity', ''),
            set_name=scryfall_data.get('set_name', '')
        )

    def _load_cache(self) -> Dict:
        """Load cache from disk."""
        if self.cache_path.exists():
            with open(self.cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_cache(self, cache: Dict):
        """Save cache to disk."""
        with open(self.cache_path, 'w', encoding='utf-8') as f:
            json.dump(cache, f, indent=2)

    def filter(
        self,
        colors: Optional[List[str]] = None,
        color_identity: Optional[List[str]] = None,
        types: Optional[List[str]] = None,
        max_cmc: Optional[float] = None,
        min_cmc: Optional[float] = None,
        keywords: Optional[List[str]] = None,
        text_contains: Optional[str] = None,
        rarity: Optional[str] = None,
        multicolor_only: bool = False,
        monocolor_only: bool = False
    ) -> List[Card]:
        """
        Filter cards based on various criteria.

        Args:
            colors: Cards that are exactly these colors (e.g., ['R', 'G'])
            color_identity: Cards whose color identity includes these colors
            types: Card types (e.g., ['Creature', 'Instant'])
            max_cmc: Maximum converted mana cost
            min_cmc: Minimum converted mana cost
            keywords: Keywords the card must have (e.g., ['Flying', 'Haste'])
            text_contains: Text that must appear in oracle text (case-insensitive)
            rarity: Card rarity ('common', 'uncommon', 'rare', 'mythic')
            multicolor_only: Only multicolor cards
            monocolor_only: Only monocolor cards

        Returns:
            List of cards matching all criteria
        """
        results = self.cards.copy()

        if colors is not None:
            results = [c for c in results if set(c.colors) == set(colors)]

        if color_identity is not None:
            results = [c for c in results if set(c.color_identity) <= set(color_identity)]

        if types is not None:
            results = [c for c in results if any(t in c.type_line for t in types)]

        if max_cmc is not None:
            results = [c for c in results if c.cmc <= max_cmc]

        if min_cmc is not None:
            results = [c for c in results if c.cmc >= min_cmc]

        if keywords is not None:
            results = [c for c in results
                      if any(kw.lower() in [k.lower() for k in c.keywords] for kw in keywords)]

        if text_contains is not None:
            text_lower = text_contains.lower()
            results = [c for c in results if text_lower in c.oracle_text.lower()]

        if rarity is not None:
            results = [c for c in results if c.rarity.lower() == rarity.lower()]

        if multicolor_only:
            results = [c for c in results if c.is_multicolor]

        if monocolor_only:
            results = [c for c in results if len(c.colors) == 1]

        return results

    def get_stats(self) -> Dict:
        """Get collection statistics."""
        stats = {
            'total_unique': len(self.cards),
            'total_cards': sum(c.quantity for c in self.cards),
            'by_color': {},
            'by_type': {},
            'by_cmc': {},
            'by_rarity': {}
        }

        # Color distribution
        for color in ['W', 'U', 'B', 'R', 'G']:
            stats['by_color'][color] = len([c for c in self.cards if color in c.colors])
        stats['by_color']['Multicolor'] = len([c for c in self.cards if c.is_multicolor])
        stats['by_color']['Colorless'] = len([c for c in self.cards if not c.colors and not c.is_land])

        # Type distribution
        type_checks = [
            ('Creature', 'is_creature'),
            ('Instant', 'is_instant'),
            ('Sorcery', 'is_sorcery'),
            ('Artifact', 'is_artifact'),
            ('Enchantment', 'is_enchantment'),
            ('Planeswalker', 'is_planeswalker'),
            ('Land', 'is_land')
        ]
        for type_name, attr in type_checks:
            stats['by_type'][type_name] = len([c for c in self.cards if getattr(c, attr)])

        # CMC distribution
        for cmc in range(8):
            stats['by_cmc'][str(cmc)] = len([c for c in self.cards if c.cmc == cmc])
        stats['by_cmc']['8+'] = len([c for c in self.cards if c.cmc >= 8])

        # Rarity distribution
        for rarity in ['common', 'uncommon', 'rare', 'mythic']:
            stats['by_rarity'][rarity] = len([c for c in self.cards if c.rarity.lower() == rarity])

        return stats


def print_cards(cards: List[Card], limit: int = 20):
    """Pretty print a list of cards."""
    if not cards:
        print("No cards found.")
        return

    print(f"\nFound {len(cards)} cards:")
    print("-" * 80)

    for i, card in enumerate(cards[:limit], 1):
        colors = ''.join(card.colors) if card.colors else 'C'
        print(f"{i:3}. {card.name:40} {colors:6} {card.mana_cost:15} {card.type_line}")

    if len(cards) > limit:
        print(f"\n... and {len(cards) - limit} more cards")
    print()


if __name__ == "__main__":
    # Example usage
    collection = Collection("/Users/eric/Downloads/Wudini Collection Export Oct 24 2025.csv")

    # Show stats
    stats = collection.get_stats()
    print("Collection Statistics:")
    print(f"  Total unique cards: {stats['total_unique']}")
    print(f"  Total cards: {stats['total_cards']}")
    print(f"\nBy color:")
    for color, count in stats['by_color'].items():
        print(f"    {color}: {count}")
    print(f"\nBy type:")
    for type_name, count in stats['by_type'].items():
        print(f"    {type_name}: {count}")

    # Example filters
    print("\n" + "="*80)
    print("Example: Red creatures with CMC <= 3")
    red_aggro = collection.filter(color_identity=['R'], types=['Creature'], max_cmc=3)
    print_cards(red_aggro, limit=10)

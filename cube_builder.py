"""
Cube builder and manager.

Helps construct a cube list from the collection with tracking and export.
"""

import json
from pathlib import Path
from typing import List, Dict, Set
from collection import Collection, Card


class CubeBuilder:
    """Manages cube construction and exports."""

    def __init__(self, collection: Collection, cube_name: str = "my_cube", cube_dir: str = "cubes"):
        self.collection = collection
        self.cube_name = cube_name
        self.cube_dir = Path(cube_dir) / cube_name
        self.cube_dir.mkdir(parents=True, exist_ok=True)
        self.cube_file = self.cube_dir / "cube.json"
        self.cube_cards: List[Card] = []
        self._load_cube()

    def _load_cube(self):
        """Load existing cube from file if it exists."""
        if self.cube_file.exists():
            with open(self.cube_file, 'r') as f:
                data = json.load(f)
                card_names = data.get('cards', [])
                # Find cards in collection by name
                for name in card_names:
                    card = self._find_card_by_name(name)
                    if card:
                        self.cube_cards.append(card)
                print(f"Loaded {len(self.cube_cards)} cards from {self.cube_file}")

    def _save_cube(self):
        """Save cube to file."""
        data = {
            'cards': [c.name for c in self.cube_cards],
            'size': len(self.cube_cards)
        }
        with open(self.cube_file, 'w') as f:
            json.dump(data, f, indent=2)

    def _find_card_by_name(self, name: str) -> Card:
        """Find a card in the collection by name."""
        for card in self.collection.cards:
            if card.name.lower() == name.lower():
                return card
        return None

    def add_card(self, card_name: str) -> bool:
        """Add a card to the cube by name."""
        card = self._find_card_by_name(card_name)
        if not card:
            print(f"❌ Card not found in collection: {card_name}")
            return False

        # Check if already in cube
        if any(c.name == card.name for c in self.cube_cards):
            print(f"⚠️  {card.name} already in cube")
            return False

        self.cube_cards.append(card)
        self._save_cube()
        print(f"✓ Added {card.name}")
        return True

    def add_cards(self, card_names: List[str]):
        """Add multiple cards at once."""
        for name in card_names:
            self.add_card(name)

    def remove_card(self, card_name: str) -> bool:
        """Remove a card from the cube."""
        for i, card in enumerate(self.cube_cards):
            if card.name.lower() == card_name.lower():
                removed = self.cube_cards.pop(i)
                self._save_cube()
                print(f"✓ Removed {removed.name}")
                return True
        print(f"❌ Card not in cube: {card_name}")
        return False

    def get_stats(self) -> Dict:
        """Get cube statistics."""
        stats = {
            'total': len(self.cube_cards),
            'by_color': {},
            'by_type': {},
            'by_cmc': {},
            'monocolor': 0,
            'multicolor': 0,
            'colorless': 0
        }

        # Color distribution
        for color in ['W', 'U', 'B', 'R', 'G']:
            stats['by_color'][color] = len([c for c in self.cube_cards if color in c.colors and len(c.colors) == 1])

        stats['monocolor'] = sum(stats['by_color'].values())
        stats['multicolor'] = len([c for c in self.cube_cards if len(c.colors) > 1])
        stats['colorless'] = len([c for c in self.cube_cards if not c.colors])

        # Type distribution
        type_checks = [
            ('Creature', lambda c: c.is_creature),
            ('Instant', lambda c: c.is_instant),
            ('Sorcery', lambda c: c.is_sorcery),
            ('Artifact', lambda c: c.is_artifact),
            ('Enchantment', lambda c: c.is_enchantment),
            ('Planeswalker', lambda c: c.is_planeswalker),
            ('Land', lambda c: c.is_land)
        ]
        for type_name, check_fn in type_checks:
            stats['by_type'][type_name] = len([c for c in self.cube_cards if check_fn(c)])

        # CMC distribution
        for cmc in range(8):
            stats['by_cmc'][str(cmc)] = len([c for c in self.cube_cards if c.cmc == cmc])
        stats['by_cmc']['8+'] = len([c for c in self.cube_cards if c.cmc >= 8])

        return stats

    def print_stats(self):
        """Print cube statistics."""
        stats = self.get_stats()

        print("\n" + "="*80)
        print(f"CUBE STATISTICS ({stats['total']} cards)")
        print("="*80)

        print(f"\nColors:")
        print(f"  White:      {stats['by_color']['W']:3d}")
        print(f"  Blue:       {stats['by_color']['U']:3d}")
        print(f"  Black:      {stats['by_color']['B']:3d}")
        print(f"  Red:        {stats['by_color']['R']:3d}")
        print(f"  Green:      {stats['by_color']['G']:3d}")
        print(f"  Multicolor: {stats['multicolor']:3d}")
        print(f"  Colorless:  {stats['colorless']:3d}")

        print(f"\nTypes:")
        for type_name, count in stats['by_type'].items():
            print(f"  {type_name:12s} {count:3d}")

        print(f"\nMana Curve:")
        for cmc, count in stats['by_cmc'].items():
            bar = '█' * count
            print(f"  {cmc:3s} {bar} ({count})")

    def list_cards(self, sort_by: str = 'cmc'):
        """List all cards in the cube."""
        if not self.cube_cards:
            print("Cube is empty!")
            return

        if sort_by == 'cmc':
            sorted_cards = sorted(self.cube_cards, key=lambda c: (c.cmc, c.name))
        elif sort_by == 'color':
            sorted_cards = sorted(self.cube_cards, key=lambda c: (''.join(c.colors) or 'Z', c.cmc, c.name))
        elif sort_by == 'type':
            sorted_cards = sorted(self.cube_cards, key=lambda c: (c.type_line, c.cmc, c.name))
        else:
            sorted_cards = sorted(self.cube_cards, key=lambda c: c.name)

        print(f"\n{'#':<4} {'Name':<40} {'Colors':<8} {'Mana':<10} {'Type'}")
        print("-" * 80)
        for i, card in enumerate(sorted_cards, 1):
            colors = ''.join(card.colors) if card.colors else 'C'
            type_short = card.type_line.split('—')[0].strip()
            print(f"{i:<4} {card.name:<40} {colors:<8} {card.mana_cost:<10} {type_short}")

    def export_to_cubecobra(self, filename: str = "cubecobra.txt"):
        """Export cube list in CubeCobra format (one card name per line)."""
        if not self.cube_cards:
            print("Cube is empty!")
            return

        output_path = self.cube_dir / filename
        with open(output_path, 'w') as f:
            for card in sorted(self.cube_cards, key=lambda c: c.name):
                f.write(f"{card.name}\n")

        print(f"✓ Exported {len(self.cube_cards)} cards to {output_path}")
        print(f"  Upload this file to CubeCobra.com")


if __name__ == "__main__":
    # Example usage
    collection = Collection("/Users/eric/Downloads/Wudini Collection Export Oct 24 2025.csv")

    # Create a new cube or load existing one
    builder = CubeBuilder(collection, cube_name="example_cube")

    # Show current stats
    builder.print_stats()

    # Example: add some iconic fast cards
    print("\n" + "="*80)
    print("Adding some starter cards...")
    print("="*80)

    starter_cards = [
        # Red aggro staples
        "Lightning Bolt",
        "Monastery Swiftspear",
        "Goblin Guide",

        # White efficient creatures
        "Mother of Runes",
        "Path to Exile",

        # Green ramp
        "Llanowar Elves",
        "Birds of Paradise",

        # Mana rocks
        "Sol Ring",
    ]

    builder.add_cards(starter_cards)
    builder.print_stats()

    print(f"\nCube saved to: {builder.cube_dir}")

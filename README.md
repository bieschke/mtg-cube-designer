# MTG Cube Designer

An intelligent tool that interviews Cube designers and generates optimal, custom-tailored Magic: The Gathering Cube lists for specific game nights.

## Vision

Building a production-grade assistant that:
- Interviews Cube organizers about their specific game night
- Learns about players, their preferences, skill levels, and favorite archetypes
- Understands the theme, format, and vibe for the evening
- Generates a perfectly tailored Cube list
- Outputs in CubeCobra.com compatible format

## Current Status

**Foundation Layer**: Basic card search functionality via Scryfall API

### What Works Now
- Search Magic cards using flexible queries
- Retrieve card details from Scryfall
- Command-line interface for card lookups

### Example Usage
```bash
# Search for cards
python search.py "lightning bolt"
python search.py "c:blue t:instant"
python search.py "cmc=3 color:red"
```

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/mtg-cube-designer.git
cd mtg-cube-designer

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Roadmap

- [ ] Interactive interview system
- [ ] Card selection algorithms based on player preferences
- [ ] Archetype balancing and synergy detection
- [ ] CubeCobra format export
- [ ] Cube size and complexity customization
- [ ] Theme-based card filtering

## Design Philosophy

This tool is **100% interview-driven**. No hardcoded assumptions about "correct" Cube design - the human expert guides the process based on what they want for that particular game night.

## Tech Stack

- Python 3
- [Scryfall API](https://scryfall.com/docs/api) for card data
- Designed for reliability and regular real-world use

## Contributing

This is a personal project, but suggestions and ideas are welcome!

## License

MIT

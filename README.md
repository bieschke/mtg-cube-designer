# MTG Cube Designer

A collaborative tool for designing custom Magic: The Gathering Cubes with Claude Code. Build perfectly tailored Cube lists through natural conversation, card-by-card selection, and expert guidance.

## How It Works

This isn't a standalone tool - it's a **collaborative design system** powered by Claude Code. You and Claude work together to:

1. **Define the Cube parameters** (players, format, constraints)
2. **Select cards one at a time** (or in batches) from your collection
3. **Balance and optimize** the final list
4. **Export to CubeCobra** format

## Quick Start

### Prerequisites

1. **Install Claude Code**: [claude.com/claude-code](https://claude.com/claude-code)
2. **Export your collection**: Get a CSV from your collection manager (e.g., Moxfield, Archidekt)
3. **Have Python 3** installed

### Installation

```bash
# Clone the repository
git clone https://github.com/bieschke/mtg-cube-designer.git
cd mtg-cube-designer

# Install dependencies
pip install -r requirements.txt
```

### Usage

Start Claude Code in this directory and begin the conversation:

```bash
cd mtg-cube-designer
claude
```

Then tell Claude what you want to build:

```
I want to design a cube for a 2-player game night next month
```

Claude will:
- Ask questions about your goals (one at a time!)
- Analyze your collection
- Propose cards and await your approval
- Track constraints you specify (no counters, no flip cards, etc.)
- Build the cube collaboratively with you
- Export everything when done

### Example Session

See [`cubes/eric_austin_nov2025/`](cubes/eric_austin_nov2025/) for a complete example of a cube design session.

**That session resulted in:**
- 135-card cube optimized for fast 2-player grid draft
- No counters, no flip cards, minimal text (per player preferences)
- Ultra-aggressive curve (51 one-drops!)
- Complete documentation of design decisions
- CubeCobra-ready export

## How the Collaboration Works

### CLAUDE.md
Read [`CLAUDE.md`](CLAUDE.md) for the complete guide on how Claude approaches cube design:
- Asks questions ONE AT A TIME
- Proposes cards in batches (after asking!)
- Remembers constraints throughout the session
- Builds tools to help explore your collection

### Your Collection

Place your collection CSV export in the project:

```bash
/Users/you/mtg-cube-designer/
  your-collection.csv    # Your exported collection
```

Claude will:
1. Parse your collection
2. Cache Scryfall data locally (for speed)
3. Only propose cards you actually own

### Files Created

Each cube design session creates a self-contained directory:

```
cubes/
  your_cube_name/
    README.md         # Design documentation
    cube.json         # Cube data (can reload later)
    cubecobra.txt     # Upload this to CubeCobra!
```

## Tools Built

The project includes reusable Python tools:

- **`collection.py`**: Parse collection CSVs, filter cards by criteria, cache Scryfall data
- **`cube_builder.py`**: Add/remove cards, track stats, export to CubeCobra
- **`check_mana.py`**: Analyze mana base and fixing available
- **`explore.py`**: Example queries for finding aggressive cards

These tools are used BY Claude during the collaborative design process. You don't run them directly - Claude uses them to help build your cube.

## Design Philosophy

### 100% Collaborative
No automated "AI designs your cube" - YOU are the expert, Claude is your assistant. Every card gets your approval.

### Your Collection Only
We only work with cards you actually own. No theoretical "best cube" - practical cubes you can build tonight.

### Session Documentation
Every design session is documented with:
- Design constraints and goals
- Card selections with reasoning
- Rejected cards and why
- Learnings for future cubes

### Fast Iteration
Built for real game nights. Design a cube, play it, iterate based on what worked.

## Example Workflows

### "I want a cube for next Friday's game night"
Claude asks about players, format, and builds collaboratively with you.

### "I want to explore tribal themes in my collection"
Claude helps you filter and explore, proposing synergistic cards.

### "Can we make this cube faster?"
Claude analyzes curve, proposes swaps to lower CMC.

## Tech Stack

- **Python 3**: Collection analysis and cube building
- **Scryfall API**: Card data and oracle text
- **Claude Code**: Collaborative design interface
- **CubeCobra**: Export format for sharing/drafting

## Contributing

This is a personal project, but suggestions and ideas are welcome! Open an issue or PR.

## Example Cubes

Check out [`cubes/`](cubes/) for completed cube designs with full documentation.

## License

MIT

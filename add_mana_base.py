"""
Auto-select the best mana base for the aggro cube.
"""

from collection import Collection
from cube_builder import CubeBuilder

# Load collection and builder
collection = Collection("/Users/eric/Downloads/Wudini Collection Export Oct 24 2025.csv")
builder = CubeBuilder(collection)

print("\n" + "="*80)
print("AUTO-SELECTING MANA BASE FOR FAST CUBE")
print("="*80)

# Get all lands
lands = collection.filter(types=['Land'])

# Categorize lands by speed (faster = better for aggro)
print("\nAnalyzing lands...")

# Pain lands - always untapped, perfect for aggro
pain_lands = [
    "Adarkar Wastes", "Battlefield Forge", "Brushland", "Caves of Koilos",
    "Karplusan Forest", "Llanowar Wastes", "Shivan Reef", "Sulfurous Springs",
    "Underground River", "Yavimaya Coast"
]

# Check lands - usually untapped in 2-color decks
check_lands = [
    "Clifftop Retreat", "Dragonskull Summit", "Drowned Catacomb", "Glacial Fortress",
    "Hinterland Harbor", "Isolated Chapel", "Rootbound Crag", "Sulfur Falls",
    "Sunpetal Grove", "Woodland Cemetery"
]

# Fast lands - untapped early (perfect for aggro)
fast_lands = [
    "Spirebluff Canal", "Stormcarved Coast"
]

# Snarl lands - usually untapped with basics
snarl_lands = [
    "Frostboil Snarl", "Furycalm Snarl", "Necroblossom Snarl", "Shineshadow Snarl",
    "Vineglimmer Snarl"
]

# Shadow lands - good in 2-color
shadow_lands = [
    "Choked Estuary", "Foreboding Ruins", "Game Trail", "Shipwreck Marsh"
]

# Valley lands
valley_lands = [
    "Darkwater Catacombs", "Mossfire Valley", "Shadowblood Ridge", "Skycloud Expanse",
    "Sungrass Prairie"
]

# Priority order for speed
priority_lands = (
    pain_lands +      # Tier 1: Always untapped
    check_lands +     # Tier 2: Usually untapped
    fast_lands +      # Tier 3: Untapped early
    snarl_lands +     # Tier 4: Usually untapped
    shadow_lands +    # Tier 5: Good in 2-color
    valley_lands      # Tier 6: Decent fixing
)

# Add the first 28 lands we have from the priority list
selected_lands = []
for land_name in priority_lands:
    card = builder._find_card_by_name(land_name)
    if card:
        selected_lands.append(card.name)
        if len(selected_lands) >= 28:
            break

print(f"\nSelected {len(selected_lands)} dual lands:")
for i, land in enumerate(selected_lands, 1):
    print(f"  {i:2}. {land}")

# Add lands to cube
print("\nAdding lands to cube...")
builder.add_cards(selected_lands)

# Add mana rocks
print("\n" + "="*80)
print("ADDING MANA ROCKS")
print("="*80)

mana_rocks = [
    "Sol Ring",          # Best rock
    "Arcane Signet",     # Universal signet
    "Mind Stone",        # Draws a card late
    "Dimir Signet",      # Good for UB/UR/BR colors
]

print(f"\nSelected {len(mana_rocks)} mana rocks:")
for rock in mana_rocks:
    print(f"  - {rock}")

builder.add_cards(mana_rocks)

# Show stats
print("\n" + "="*80)
print("MANA BASE COMPLETE")
print("="*80)
builder.print_stats()

print("\nMana base ready! You have:")
print(f"  - {len(selected_lands)} dual lands")
print(f"  - {len(mana_rocks)} mana rocks")
print(f"  - 9 cards already added (Lightning Bolt, etc.)")
print(f"  - {135 - len(selected_lands) - len(mana_rocks) - 9} slots remaining for spells")

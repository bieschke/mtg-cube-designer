"""
Check mana fixing available in the collection.
"""

from collection import Collection, print_cards

# Load collection
collection = Collection("/Users/eric/Downloads/Wudini Collection Export Oct 24 2025.csv")

print("\n" + "="*80)
print("MANA FIXING ANALYSIS")
print("="*80)

# Get all lands
lands = collection.filter(types=['Land'])

# Non-basic lands that produce multiple colors
print("\n### DUAL LANDS (produce 2+ colors)")
dual_lands = []
for land in lands:
    # Check for lands that produce multiple colors or have color names
    oracle_lower = land.oracle_text.lower()
    if any(word in oracle_lower for word in ['add {w}', 'add {u}', 'add {b}', 'add {r}', 'add {g}']):
        # Count how many different mana symbols appear
        mana_count = sum([1 for color in ['{w}', '{u}', '{b}', '{r}', '{g}'] if color in oracle_lower])
        if mana_count >= 2:
            dual_lands.append(land)
    # Also check for "any color" lands
    elif 'any color' in oracle_lower or 'any type' in oracle_lower:
        dual_lands.append(land)

print(f"Found {len(dual_lands)} dual/fixing lands")
print_cards(sorted(dual_lands, key=lambda c: c.name), limit=100)

# Color-specific duals
print("\n### DUAL LANDS BY COLOR PAIR")
color_pairs = {
    'WU': ('Azorius', ['plains', 'island']),
    'UB': ('Dimir', ['island', 'swamp']),
    'BR': ('Rakdos', ['swamp', 'mountain']),
    'RG': ('Gruul', ['mountain', 'forest']),
    'GW': ('Selesnya', ['forest', 'plains']),
    'WB': ('Orzhov', ['plains', 'swamp']),
    'UR': ('Izzet', ['island', 'mountain']),
    'BG': ('Golgari', ['swamp', 'forest']),
    'RW': ('Boros', ['mountain', 'plains']),
    'GU': ('Simic', ['forest', 'island'])
}

pair_counts = {}
for pair_code, (guild_name, land_types) in color_pairs.items():
    count = 0
    for land in dual_lands:
        oracle_lower = land.oracle_text.lower()
        name_lower = land.name.lower()
        # Check if this land produces both colors in the pair or mentions both land types
        if (any(t in oracle_lower or t in name_lower for t in land_types) or
            guild_name.lower() in name_lower):
            count += 1
    pair_counts[pair_code] = count

for pair_code, count in sorted(pair_counts.items(), key=lambda x: -x[1]):
    print(f"  {pair_code} ({color_pairs[pair_code][0]}): {count} lands")

# Fetchlands and other generic fixing
print("\n### GENERIC FIXING (works for any color)")
generic_fixing = [l for l in lands if 'any color' in l.oracle_text.lower() or
                  'search' in l.oracle_text.lower() and 'basic' in l.oracle_text.lower()]
print(f"Found {len(generic_fixing)} generic fixers")
print_cards(generic_fixing, limit=50)

# Mana rocks
print("\n### MANA ROCKS (artifact fixing)")
artifacts = collection.filter(types=['Artifact'])
mana_rocks = [a for a in artifacts if any(word in a.oracle_text.lower()
              for word in ['add {', '{t}: add'])]
print(f"Found {len(mana_rocks)} mana rocks")
print_cards(sorted(mana_rocks, key=lambda c: c.cmc), limit=30)

# Summary
print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total dual lands: {len(dual_lands)}")
print(f"Generic fixing lands: {len(generic_fixing)}")
print(f"Mana rocks: {len(mana_rocks)}")
print(f"Total mana fixing: {len(dual_lands) + len(mana_rocks)}")

print("\n### RECOMMENDATION:")
total_fixing = len(dual_lands) + len(mana_rocks)
if total_fixing >= 40:
    print("✓ STRONG fixing - can support 5 colors easily")
elif total_fixing >= 20:
    print("⚠ MODERATE fixing - 3-4 colors recommended")
else:
    print("⚠ LIMITED fixing - 2-3 colors recommended for consistency")

"""
Interactive exploration tool for the collection.
"""

from collection import Collection, print_cards

# Load collection (will use cache)
collection = Collection("/Users/eric/Downloads/Wudini Collection Export Oct 24 2025.csv")

print("\n" + "="*80)
print("EXPLORING AGGRESSIVE, SIMPLE CARDS FOR FAST CUBE")
print("="*80)

# 1-drop creatures
print("\n### 1-DROP CREATURES (all colors)")
one_drops = collection.filter(types=['Creature'], max_cmc=1, min_cmc=1)
# Exclude tokens
one_drops = [c for c in one_drops if 'Token' not in c.type_line]
print_cards(sorted(one_drops, key=lambda c: (len(c.colors), c.name)), limit=50)

# 2-drop creatures
print("\n### 2-DROP CREATURES (all colors)")
two_drops = collection.filter(types=['Creature'], max_cmc=2, min_cmc=2)
two_drops = [c for c in two_drops if 'Token' not in c.type_line]
print_cards(sorted(two_drops, key=lambda c: (len(c.colors), c.name)), limit=50)

# Cheap removal/interaction
print("\n### CHEAP REMOVAL (CMC <= 2)")
removal = collection.filter(types=['Instant', 'Sorcery'], max_cmc=2)
# Look for cards with destroy, damage, exile in text
removal = [c for c in removal if any(word in c.oracle_text.lower()
                                      for word in ['destroy', 'damage', 'exile', 'counter', 'return'])]
print_cards(sorted(removal, key=lambda c: (c.cmc, len(c.colors), c.name)), limit=30)

# Simple combat tricks
print("\n### COMBAT TRICKS (CMC <= 2)")
tricks = collection.filter(types=['Instant'], max_cmc=2)
# Look for pump spells
tricks = [c for c in tricks if any(word in c.oracle_text.lower()
                                    for word in ['+', 'gets', 'protection', 'indestructible'])]
print_cards(sorted(tricks, key=lambda c: (c.cmc, len(c.colors), c.name)), limit=30)

# Simple 3-drops (finishers for aggro)
print("\n### 3-DROP CREATURES (aggressive finishers)")
three_drops = collection.filter(types=['Creature'], max_cmc=3, min_cmc=3)
three_drops = [c for c in three_drops if 'Token' not in c.type_line]
# Prioritize creatures with keywords (simple text)
three_drops_with_keywords = [c for c in three_drops if c.keywords]
print_cards(sorted(three_drops_with_keywords, key=lambda c: (len(c.colors), c.name)), limit=40)

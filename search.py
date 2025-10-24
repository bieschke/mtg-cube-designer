#!/usr/bin/env python3
import sys
import requests
from scryfall import ScryfallClient


def format_card(card: dict) -> str:
    lines = []
    lines.append(f"\n{'=' * 60}")
    lines.append(f"Name: {card.get('name', 'Unknown')}")
    lines.append(f"Mana Cost: {card.get('mana_cost', 'N/A')}")
    lines.append(f"Type: {card.get('type_line', 'N/A')}")
    
    if 'oracle_text' in card:
        lines.append(f"Text: {card['oracle_text']}")
    
    if 'power' in card and 'toughness' in card:
        lines.append(f"P/T: {card['power']}/{card['toughness']}")
    
    lines.append(f"Set: {card.get('set_name', 'Unknown')} ({card.get('set', '').upper()})")
    lines.append(f"Rarity: {card.get('rarity', 'Unknown').capitalize()}")
    
    if 'prices' in card and card['prices'].get('usd'):
        lines.append(f"Price: ${card['prices']['usd']}")
    
    lines.append('=' * 60)
    return '\n'.join(lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python search.py <query>")
        print("Examples:")
        print("  python search.py 'lightning bolt'")
        print("  python search.py 'c:blue t:instant'")
        print("  python search.py 'cmc=3 color:red'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    client = ScryfallClient()
    
    try:
        print(f"Searching for: {query}")
        page = 1
        all_cards = []
        
        while True:
            result = client.search_cards(query, page)
            
            if page == 1:
                total = result.get('total_cards', 0)
                print(f"Found {total} cards, fetching all pages...")
            
            all_cards.extend(result.get('data', []))
            
            if not result.get('has_more'):
                break
            
            page += 1
        
        print(f"\nRetrieved {len(all_cards)} cards\n")
        
        for card in all_cards:
            print(format_card(card))
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"No cards found matching: {query}")
        else:
            print(f"API Error ({e.response.status_code}): {e.response.json().get('details', str(e))}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

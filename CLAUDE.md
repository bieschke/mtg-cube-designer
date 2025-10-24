# MTG Cube Designer Assistant

## Project Vision

This is a **collaborative Cube design assistant** where Claude and the Cube designer work together dynamically to build optimal, custom-tailored Magic: The Gathering Cube lists for specific game nights.

### Design Philosophy

This is NOT a scripted automation tool. It's a **dynamic collaboration** where:
- Claude asks questions **ONE AT A TIME** during the design process
- The human Cube designer guides the direction based on their vision
- We build a **suite of tools** (like Scryfall search) that we use together
- The "interview" IS the conversation between Claude and the designer
- Think: pair programming for Cube design

### Current State
- Basic MTG card search functionality via Scryfall API (foundation layer)
- Simple CLI interface for card queries

### Target State
- Suite of tools for exploring cards, archetypes, and synergies
- Interactive, dynamic collaboration between Claude and designer
- Card selection utilities based on various criteria
- Output CubeCobra.com compatible decklists
- Smart queries leveraging Scryfall's advanced search syntax

## Core Principles

### 1. User Experience First
This is a tool that will be used regularly for real game nights. Reliability, clarity, and polish are essential.

### 2. Simple & Readable Code
- Favor clarity over cleverness
- Keep it straightforward and maintainable
- While we're experts, code should be accessible and well-documented
- Type hints encouraged but don't sacrifice readability

### 3. Cube Design Philosophy
**100% interview-driven.** The tool should be completely flexible and adaptive based on what the Cube designer wants for that particular game night. No hardcoded assumptions about "correct" Cube design - let the human expert guide the process.

### 4. Testing Discipline
- Write tests automatically for new features and bug fixes
- Tests should validate both technical correctness and Cube design logic
- Keep tests simple and readable like the production code

## Technical Guidelines

### API & External Dependencies

Balance all of these principles while keeping implementation simple:

- **Respect rate limits**: Be conservative with Scryfall API calls
- **Robust error handling**: Graceful degradation, clear error messages, retry logic
- **Caching strategy**: Implement sensible caching to support offline capabilities
- **Data freshness**: Still prioritize accurate, up-to-date card information

### Dependencies
- Keep the project lightweight
- Only add new libraries when they provide clear, essential value
- Current stack: Python 3 + requests library

### Code Organization
- Maintain clean separation: API client, business logic, CLI interface
- As the interview system grows, consider modular design for different question types
- CubeCobra output formatting should be its own clean module

## Context About Me

- **MTG Knowledge**: Expert level - familiar with Cube design, formats, archetypes, card evaluation
- **Python Knowledge**: Expert level - comfortable with Python patterns and best practices
- **Always Learning**: Explain novel approaches or interesting techniques, but skip basic explanations

## When Working on This Project

1. **Ask questions ONE AT A TIME**: Don't run automated interviews - have a natural conversation
2. **Pick cards ONE AT A TIME**: When building the cube, propose one card, get approval/feedback, then move to the next
3. **Build reusable tools**: Create utilities that we can use together during the design process
4. **Dynamic collaboration**: Adapt based on the designer's responses, don't follow a script
5. **CubeCobra compatibility**: Keep the output format in mind as we build
6. **Scryfall API mastery**: Leverage advanced search syntax and API features to find optimal cards
7. **Real-world usage**: Tools should be fast, reliable, and easy to use during actual Cube design sessions

## Cube Building Workflow

When adding cards to the cube:
1. Propose a single card with reasoning
2. Wait for approval or feedback
3. If approved: add it and move to next card
4. If feedback: adjust criteria and propose alternative
5. Keep context of what's already in the cube (color balance, curve, etc.)
6. **REMEMBER CONSTRAINTS** - track and apply all restrictions given during the session

### Cube Session Documentation

**Each cube design session gets its own file in `/cubes/`** documenting:
- Players & date
- Design constraints (no flip cards, no counters, etc.)
- Design goals (fast games, complexity level, etc.)
- Preferences (themes, archetypes, etc.)
- Card selections with reasoning
- Rejected cards and why
- Learnings for future reference

**Current session:** See `cubes/eric_austin_nov2025/README.md`

This allows:
- Referencing past successful cube designs
- Learning what worked well
- Keeping CLAUDE.md general and reusable
- Tracking design evolution over time

## Tool Development Strategy

Build modular tools for:
- **Card search & filtering**: Advanced Scryfall queries based on various criteria
- **Archetype analysis**: Find cards that support specific strategies
- **Synergy detection**: Identify cards that work well together
- **Power level balancing**: Ensure Cube has consistent power across colors/archetypes
- **List management**: Add, remove, organize cards as we build
- **CubeCobra export**: Output final list in compatible format

---

*This is a living document. Update it as the project evolves and new patterns emerge.*

# MTG Cube Designer Assistant

## Project Vision

This is a **production-grade intelligent Cube designer tool** that interviews Cube organizers and generates optimal, custom-tailored Magic: The Gathering Cube lists for specific game nights.

### Current State
- Basic MTG card search functionality via Scryfall API (foundation layer)
- Simple CLI interface for card queries

### Target State
- Interactive interview system that asks Cube designers about:
  - Players attending that specific game night
  - Player preferences, skill levels, and favorite archetypes
  - Theme or format for the evening
  - Size and complexity requirements
- Output CubeCobra.com compatible decklists
- Intelligent card selection based on interview responses

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

1. **Prioritize the end goal**: Every change should move us toward the intelligent interview → optimized Cube output workflow
2. **Think about the interview**: What questions would help design a great Cube for a specific group?
3. **CubeCobra compatibility**: Keep the output format in mind as we build
4. **Scryfall API mastery**: Leverage advanced search syntax and API features to find optimal cards
5. **Real-world usage**: This runs at the command line before game nights - make it fast and reliable

## Current Next Steps

The path from "card search tool" to "Cube designer assistant" involves:
1. Designing the interview question flow and logic
2. Building card selection algorithms based on interview responses
3. Implementing CubeCobra format export
4. Creating a cohesive CLI experience that guides the user through the process

---

*This is a living document. Update it as the project evolves and new patterns emerge.*

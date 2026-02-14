# TextAdventure

A Python-based text adventure game engine. Build multi-branch narratives, character attribute systems, conditional logic, and multiple endings through nodes and options—no complex coding required.

## Features

- **Visual Story Structure** - Organize plots using Nodes and Options, naturally supporting branching paths
- **Data-Driven System** - Built-in variable system supporting character attributes, items, affinity scores, or any numeric values
- **Conditional Control** - Options can be shown/disabled based on conditions, supporting complex logic (e.g., "requires key AND level ≥ 5")
- **Character Creation** - Built-in input validation system supporting character customization at game start
- **Save & Share** - Games can be exported as single files, easy to share with friends or save progress
- **Secure Execution** - Game logic runs in a restricted environment, no worries about code injection

## Quick Start (1 Minute)

We provide several complete example games, you can directly run them to experience the functionality of the game engine:

- [Hotel Detective](hotel_detective-en.py)
- [Deep Awakening](deep_awaken-en.py)

## Full Documentation

**[View Detailed Creation Guide →](story_doc-en.md)**

Includes:
- Complete API reference
- Variable access rules (important)
- Conditional expression syntax
- Node data execution order
- Common pitfalls and solutions
- Full example code

## Installation

```bash
python game.py                   # Run demo
```

Python version requirement: 3.8+

## Quick Game Creation

1. Create `my_game.py`
2. Import `TextAdventure` module
3. Define nodes and options (refer to example above or detailed docs)
4. Run `python my_game.py`

**Sharing Your Game**:
```python
# Export after creation
game.dump("my_game.pkl")

# Player loads and runs
game = Game.load("my_game.pkl")
game.play()
```

## Project Structure

```
TextAdventure/
├── TextAdventure.py    # Game engine (no modifications needed)
├── consts.py           # Secure execution environment config
├── story_doc.md        # Detailed creation documentation
└── game.py             # Full feature demo
```

## License

MIT License - Free for personal or commercial use.
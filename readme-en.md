# TextAdventure

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A native Python text adventure game engine. No DSL, no visual editor, pure code-driven—write interactive fiction like you write Python.**

Full documentation (teaching you how to write a text adventure game from scratch) -> [story_doc-en.md](./story_doc-en.md)

If you've ever wanted to write complex combat systems in Twine, create pure text terminal games in Ren'Py, or simply want to manage your narrative branches with Git—this is the engine for you.

---

## ✨ Core Features

- **🐍 Pure Python, Zero Learning Curve** - No proprietary scripting language, if you know Python you can write. Directly import any library (numpy, pandas, AI models).
- **📊 Data-Driven Design** - Built-in `init_data`/`set_data` system, full control over RPG stats, inventory, quest states.
- **⚡ Three-Stage Lifecycle** - `on_load` → `on_ready` → `on_move` precise control over execution timing for each node.
- **🔧 Fully Customizable IO** - Through the `IOHandler` interface, the same code can run on terminal, Web, GUI, or API.
- **💾 Native Save System** - Complete state serialization based on pickle, supporting save/load at any time.
- **🌲 Git-Friendly** - All .py files, version control, code review, CI/CD ready out of the box.

[Developer Documentation](./story_doc-en.md)

---

## 🚀 30-Second Quick Start

```bash
git clone https://github.com/zaf-x/TextAdventure.git 
cd TextAdventure
source venv/bin/activate
python3 example.py
```

Then select options and begin your adventure.

---

## 📝 One-Minute Example

```python
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option

# Create game
game = Game(game_name="Dungeon Starter")

# Define node: with state management
entrance = Node(
    game=game,
    node_id="entrance",
    name="Cave Entrance",
    desc="You stand at the dark entrance. Torches remaining: {torches}",
    init_data={"torches": "3", "hp": "100"},
    set_data={"visited": "visited + 1"}
)

# Define option: with conditional judgment
deep_cave = Option(
    game=game,
    option_id="enter",
    name="Enter Deep Cave",
    desc="Enter the darkness...",
    next_node_id="boss_room",
    move_condition="torches > 0",
    cant_move_desc="Too dark, you need a torch!"
)

# Add option and run
entrance.add_option(deep_cave)

if __name__ == "__main__":
    game.play()
```

Don't like how it's written? Click [here](./story_doc.md) to view the full documentation and write your own.

---

## 📚 Documentation

For full documentation (including advanced scripting, IOHandler customization, save system, etc.), please see:

**[📖 story_doc-en.md](./story_doc-en.md)**

Or quick reference:
- **Character Creation** - Use `init_input` to implement opening character creation
- **Complex Logic** - `on_ready`/`on_move` scripts and external .py file separation
- **Custom Interface** - Inherit `IOHandler` to implement Web or GUI versions
- **Debugging Tips** - Common error troubleshooting guide

---

## 🆚 Why Not Twine/Ren'Py?

| Scenario | Recommended Choice |
|----------|-------------------|
| Zero programming foundation, quick branching novel | Twine ✅ |
| Visual novel, needs character art/audio | Ren'Py ✅ |
| **Complex numerical systems (RPG, Roguelike)** | **TextAdventure ✨** |
| **Need version control/unit testing** | **TextAdventure ✨** |
| **Embed into Python projects/data analysis workflows** | **TextAdventure ✨** |
| Pure text terminal games (SSH/MUD) | **TextAdventure ✨** |

---

## 🤝 Contributing

Welcome PRs and Issues! Especially:
- More IOHandler implementations (Web, Discord Bot, TUI)
- Example games (RPG, puzzle, narrative)
- Bug fixes and performance optimizations

---

## 📄 License

MIT License - Free to use, free to modify.
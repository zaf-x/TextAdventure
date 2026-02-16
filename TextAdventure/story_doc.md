# TextAdventure Documentation

## 1. Initialization

### 1.1 Clone the repository

```bash
git clone https://github.com/zaf-x/TextAdventure
cd TextAdventure
source TextAdventure/bin/activate
```

This will clone the repository to your local machine and prepare the engine for you to use.
All the files you create should be in the root directory (`.`) of the engine.

**WARNING:**
<span style="color: orange; font-weight: bold;">
Do NOT create any files in the `./TextAdventure/` directory unless you know what you are doing.
</span>

### 1.2 Create a new story file

Create a Python file with the name of your story in the root directory. For example, `my_story.py`.

The folder structure should look like this:

```
.
├── __pycache__
│   └── ...
├── TextAdventure/
│   ├── pyvenv.cfg
│   ├── readme.md
│   ├── standalone.py
│   ├── standalone_script.md
│   └── story_doc.md
└── my_story.py
```

### 1.3 Imports

Add the following line at the top of your story file:

```python
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option
```

That's it! You can now start writing your story.

## 2. Story Format

### 2.1 Game Structure

The game is composed of nodes. Each node represents a scene in your story.
The game starts from the first node. You can configure the start node ID in the `Game` class.

The default start node ID is `"start"`.

Each node has a unique ID and can contain options to jump to other nodes.

Create a game:

```python
game = Game(
    game_name="My Story",
    start_node_id="start"  # Optional, defaults to "start"
)
```

**Game Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `game_name` | `str` | No | The name of the game. Default: `"TextAdventure"`. |
| `start_node_id` | `str` | No | The ID of the start node. Default: `"start"`. |
| `init_input` | `list[dict]` | No | Initial character creation inputs. See Section 2.8. |
| `io_handler` | `IOHandler` | No | Custom IO handler. See Section 2.9. Default: builtin `IOHandler`. |

### 2.2 Nodes

A node is created using the `Node` class:

```python
node = Node(
    game=game,
    node_id="start",
    name="Start",
    desc="You are at the start of the game."
)
```

**Node Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `game` | `Game` | **Yes** | Game instance this node belongs to. |
| `node_id` | `str` | **Yes** | Unique ID of the node. Must be unique across all nodes. |
| `name` | `str` | No | Name of the node (displayed to player). Default: `""`. |
| `desc` | `str` | No | Description text. Supports `{variable}` formatting. Default: `""`. |
| `end_desc` | `str` | No | If set, this is an ending node. Text shown when game ends. Default: `""`. |
| `options` | `list[Option]` | No | List of options. Can also be added via `add_option()`. Default: `[]`. |
| `init_data` | `dict` | No | Data to set only if variable doesn't exist. Format: `{"var": "expression"}`. Default: `{}`. |
| `set_data` | `dict` | No | Data to set when node is visited. Format: `{"var": "expression"}`. Default: `{}`. |
| `defaults` | `list[dict]` | No | Auto-jump conditions. `[{"condition": "expr", "node_id": "next"}]`. Default: `[]`. |
| `on_load` | `str` | No | Python code executed when node loads (before data change). Default: `""`. |
| `on_ready` | `str` | No | Python code executed when node is ready (after data change). Default: `""`. |
| `on_move` | `str` | No | Python code executed when leaving the node. Default: `""`. |

#### Data System (init_data and set_data)

Both fields accept a Python dictionary where **keys are variable names** and **values are string expressions** that will be evaluated:

```python
node = Node(
    game=game,
    node_id="example",
    name="Example",
    desc="You have {coins} coins.",
    init_data={
        "coins": "100",           # Sets coins to 100 (integer)
        "has_key": "False",       # Sets has_key to False (boolean)
        "player_name": "\"Alex\"" # Sets player_name to "Alex" (string)
    },
    set_data={
        "visited_count": "visited_count + 1"  # Increment counter
    }
)
```

**Important:** Values must be **strings containing valid Python expressions**, not the actual values:
- ✅ Correct: `"100"` (evaluates to integer 100)
- ❌ Wrong: `100` (integer, will cause error)

Available types in expressions: `int`, `float`, `str`, `bool`, `list`, `dict`, `None`, plus math functions like `abs()`, `min()`, `max()`, `len()`, `range()`, etc.

#### Auto-jump (defaults)

Make a node automatically redirect to another node based on conditions:

```python
node = Node(
    game=game,
    node_id="check_health",
    name="Health Check",
    desc="Checking your status...",
    defaults=[
        {
            "condition": "health <= 0",
            "node_id": "game_over"
        },
        {
            "condition": "health > 0 and poisoned",
            "node_id": "poison_effect"
        }
    ]
)
```

Conditions are evaluated in order. The first True condition triggers the jump.

#### Ending Nodes

Create an ending by setting `end_desc`:

```python
ending = Node(
    game=game,
    node_id="victory",
    name="Victory",
    desc="You defeated the final boss!",
    end_desc="Congratulations! You have completed the game.\nThanks for playing!"
)
```

When the player reaches this node, the game displays the end description and terminates.

### 2.3 Options

Options allow players to make choices:

```python
option = Option(
    game=game,
    option_id="go_north",
    name="Go North",
    desc="Travel to the northern cave.",
    next_node_id="cave_entrance"
)

node.add_option(option)
```

**Option Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `game` | `Game` | **Yes** | Game instance this option belongs to. |
| `option_id` | `str` | **Yes** | Unique ID for this option (unique within the node). |
| `name` | `str` | No | Display text for the choice. Default: `""`. |
| `desc` | `str` | No | Additional description shown to player. Default: `""`. |
| `next_node_id` | `str` | No | ID of the node to jump to when selected. Default: `"start"`. |
| `move_condition` | `str` | No | Python expression. If False, option is disabled. Default: `"True"`. |
| `show_condition` | `str` | No | Python expression. If False, option is hidden. Default: `"True"`. |
| `cant_move_desc` | `str` | No | Text shown when option is visible but disabled. Default: `""`. |

#### Conditional Options

```python
locked_door = Option(
    game=game,
    option_id="open_door",
    name="Open the Door",
    desc="Try to open the heavy door.",
    next_node_id="throne_room",
    move_condition="has_key == True",
    cant_move_desc="The door is locked. You need a key.",
    show_condition="True"  # Always show, but sometimes disabled
)
```

### 2.4 Scripting

For complex logic that can't be handled by `init_data`/`set_data`, use the scripting fields: `on_load`, `on_ready`, `on_move`.

**Execution Order:**
1. Node loads
2. `on_load` executes
3. `init_data`/`set_data` are applied
4. `on_ready` executes
5. Node description and options are displayed
6. Player makes a choice
7. `on_move` executes
8. Transition to next node

**Accessing Shared Data:**
- Read: Use variable directly (e.g., `print(f"HP: {player_hp}")`)
- Write: Use `data["var_name"] = value` (⚠️ Never use `var_name = value` - this creates a local variable!)

**Special Variables:**
- `this`: The current Node instance
- `data`: The shared Data instance (also accessible as individual variables)

Example:
```python
complex_node = Node(
    game=game,
    node_id="battle",
    name="Battle",
    desc="A wild beast appears!",
    set_data={"enemy_hp": "50", "player_hp": "100"},
    on_ready="""
        print(f"Enemy HP: {enemy_hp}")
        print("Preparing combat interface...")
        # You can modify data here
        data["combat_started"] = True
    """,
    on_move="""
        if enemy_hp <= 0:
            print("Victory!")
            data["xp"] = xp + 50
    """
)
```

### 2.5 Advanced Scripting

#### Dynamic Option Management

You can add or remove options programmatically in scripts:

```python
on_ready="""
    # Add a dynamic option
    if has_secret_knowledge:
        new_opt = Option(
            game=game,
            option_id="secret_path",
            name="Take Secret Path",
            desc="You know a shortcut.",
            next_node_id="hidden_room"
        )
        this.add_option(new_opt)
    
    # Remove options by ID
    this.del_option_by_id("useless_option")
    
    # Remove by condition
    this.del_option_by_map(lambda opt: "temp_" in opt.option_id)
"""
```

#### Module Import in Scripts

You can import safe modules within a script:

```python
on_ready="""
    import random
    import math
    
    damage = random.randint(10, 20)
    crit_chance = math.sqrt(dexterity) * 0.1
    
    print(f"Damage roll: {damage}")
    
    # To use in other nodes, inject into data:
    data["random"] = random
    data["math"] = math
"""
```

**Allowed modules:** `math`, `random`, `datetime`, `calendar`, `json`, `time`, `numpy`

**Important:** Imports are local to that specific script. To reuse across nodes, store the module in `data` as shown above.

### 2.6 Loading Scripts from Files (Long Script Separation)

For complex logic (10+ lines), write scripts in separate `.py` files and load them:

**File: `scripts/combat_system.py`**
```python
import random

# Access shared data directly
player_hp = data.get("player_hp", 100)
enemy_hp = 50

print(f"Combat started! Enemy HP: {enemy_hp}")

while enemy_hp > 0 and player_hp > 0:
    dmg = random.randint(5, 15)
    enemy_hp -= dmg
    print(f"You deal {dmg} damage!")
    
    if enemy_hp > 0:
        enemy_dmg = random.randint(3, 10)
        player_hp -= enemy_dmg
        print(f"Enemy deals {enemy_dmg} damage!")

data["player_hp"] = player_hp
data["combat_result"] = "victory" if player_hp > 0 else "defeat"
```

**In your story file:**
```python
battle_node = Node(
    game=game,
    node_id="combat",
    name="Combat Encounter",
    desc="A hostile creature attacks!"
)

# Load scripts from files
battle_node.load_onload("scripts/init_combat.py")      # Runs before data change
battle_node.load_onready("scripts/combat_system.py")   # Runs after data change
battle_node.load_onmove("scripts/end_combat.py")       # Runs when leaving
```

**Benefits:**
- Full IDE support (syntax highlighting, linting)
- Easier debugging (error messages show file names)
- Cleaner main story file

### 2.7 Save and Load System

The engine supports saving and loading game state using Python's pickle module.

**Saving:**
```python
# Anywhere in your code, or after game ends
game.dump("save_file.pkl")
```

**Loading:**
```python
# Load a saved game
loaded_game = Game.load("save_file.pkl")
loaded_game.play()  # Continue from where you left off
```

**Usage Example:**
```python
# Add a save option in your game
save_option = Option(
    game=game,
    option_id="save_game",
    name="Save Game",
    desc="Save your progress.",
    next_node_id="current"  # Stay on same node
)

# In the node's on_move or via custom logic, call game.dump()
```

**Note:** Save files store the entire game state including all nodes, shared data, and current position.

### 2.8 Character Creation (init_input)

Configure initial player inputs at game start:

```python
game = Game(
    game_name="Epic Quest",
    start_node_id="start",
    init_input=[
        {
            "prompt": "Enter your name: ",
            "name": "player_name",
            "converter": "str",
            "condition": "3 <= len(val) <= 20",
            "err_desc": "Name must be 3-20 characters."
        },
        {
            "prompt": "Enter your age (10-100): ",
            "name": "player_age",
            "converter": "int",
            "condition": "10 <= val <= 100",
            "err_desc": "Age must be between 10 and 100."
        },
        {
            "prompt": "Choose class (warrior/mage/rogue): ",
            "name": "player_class",
            "converter": "str",
            "condition": "val in ['warrior', 'mage', 'rogue']",
            "err_desc": "Invalid class choice."
        }
    ]
)
```

**Init Input Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `prompt` | `str` | **Yes** | Text shown to player when asking for input. |
| `name` | `str` | **Yes** | Variable name to store the input value in shared data. |
| `converter` | `str` | No | Python expression to convert input. Default: `"str"`. Examples: `"int"`, `"str.lower"`, `"lambda x: x.strip()"`. |
| `condition` | `str` | No | Validation expression (use `val` to reference converted value). Default: `"True"`. |
| `err_desc` | `str` | **Yes** | Error message shown if validation fails. |

### 2.9 Custom IO Handler

For custom interfaces (GUI, Web, etc.), subclass `IOHandler`:

```python
from TextAdventure import IOHandler

class WebIOHandler(IOHandler):
    def show_node(self, node):
        # Custom display logic
        print(f"<h1>{node.name}</h1>")
        print(f"<p>{node.desc}</p>")
    
    def show_options(self, ava_op, dis_op):
        # Return selected option object
        # Implement your own input mechanism
        pass
    
    def get_init_input(self, prompt):
        # Custom input method
        return input(prompt)

# Use custom handler
game = Game(
    game_name="Web Adventure",
    io_handler=WebIOHandler(Data())
)
```

**Methods you can override:**
- `show_node(node)`: Display node content
- `show_options(ava_op, dis_op)`: Display choices, return selected Option
- `show_end(node)`: Display ending
- `get_init_input(prompt)`: Get initial character creation input
- `show_init_input_error(err_desc, user_input)`: Display validation errors

## 3. Appendix

### 3.1 Debug Tips

If you get errors like:
```
[ERROR] 节点 'x' 的 set_data['y'] = 'z' 执行失败: name 'abc' is not defined
```

Check that:
1. Variable expressions in `init_data`/`set_data` are valid Python
2. Variables referenced in expressions exist (set by previous nodes or `init_data`)
3. Strings in expressions are properly quoted: `"\"text\""` not `"text"`

### 3.2 Complete Minimal Example

```python
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option

# Create game
game = Game(game_name="The Cave")

# Create nodes
start = Node(
    game=game,
    node_id="start",
    name="Cave Entrance",
    desc="You stand at the mouth of a dark cave. {torches} torches are lit.",
    init_data={"torches": "2", "has_sword": "False"}
)

cave = Node(
    game=game,
    node_id="cave",
    name="Inside the Cave",
    desc="It's dark and damp.",
    on_ready="""
        if torches <= 0:
            print("It's pitch black! You can't see anything.")
    """
)

# Create options
enter = Option(
    game=game,
    option_id="enter",
    name="Enter Cave",
    desc="Go inside.",
    next_node_id="cave",
    move_condition="torches > 0",
    cant_move_desc="Too dark to enter without light."
)

start.add_option(enter)

# Add return option
back = Option(
    game=game,
    option_id="back",
    name="Go Back",
    desc="Return to entrance.",
    next_node_id="start"
)
cave.add_option(back)

# Run
if __name__ == "__main__":
    game.play()
```
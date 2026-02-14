# TextAdventure Game Script Writing Guide

## 1. File Structure

```python
from TextAdventure import Game, Node, Option

# 1. Create game instance
game = Game(start_node_id="start", game_name="Game Name")

# 2. Define nodes
node = Node(game, node_id="...", name="...", desc="...")

# 3. Define options
option = Option(game, option_id="...", name="...", next_node_id="...")

# 4. Assemble
node.add_option(option)
game.add_node(node)

# 5. Run
game.play()
```

## 2. Data Mechanisms (Critical)

### Execution Order (Important!)
When a node loads, execution follows this sequence:
1. **on_load** script executes
2. **init_data** applies (only if variable doesn't exist)
3. **set_data** applies (overwrites every time)
4. **on_ready** script executes

### Data Definition Methods

| Attribute | Purpose | Execution Timing | Syntax Characteristics |
|-----------|---------|------------------|------------------------|
| `init_data` | Initialize default values | First node entry (only if variable doesn't exist) | `{"hp": "100"}` string expressions |
| `set_data` | Force set/overwrite | Executes every node entry | `{"hp": "hp + 10"}` can use current variables |
| `on_load` | Preparation script | **Before** data application | For initialization checks, **init_data not yet applied** |
| `on_ready` | Ready script | **After** data application | For logic processing, **all data is ready** |

## 3. Variable Access Rules (Core)

### Rule Distinction

**A. Expression Environment (Read-Only)**
- Usage: `set_data` values, `move_condition`, `show_condition`, `defaults` `condition`
- Access: **Direct variable name** (e.g., `hp`, `gold >= 100`, `job == 1`)
- Limitation: Read-only, cannot assign

```python
# Correct
set_data={"gold": "gold + 50", "hp": "min(hp + 10, max_hp)"}
move_condition="level >= 2 and has_key"
show_condition="job == 1"  # Only visible to warriors
```

**B. Script Environment (Read-Write)**
- Usage: `on_load`, `on_ready`, `on_move`
- Reading: **Direct variable name** (e.g., `if hp > max_hp:`)
- Writing: **Must use data object** (e.g., `data['hp'] = 100`)

```python
# Correct
on_ready=""
if hp > max_hp:
    data['hp'] = max_hp  # Write operations must use data[]
print(f"Current HP: {hp}")     # Read operations use direct variable names
""

# Incorrect
on_ready=""
hp = 100          # Wrong! This just creates a local variable
data[hp] = 100    # Wrong! Dictionary key should be string 'hp'
""
```

## 4. Node Parameters Detailed

```python
Node(
    game=game,                    # Game instance (required)
    node_id="start",              # Unique identifier (required)
    name="Start",                 # Display name
    desc="Description text",      # Description (supports {variable} formatting)
    init_data={"hp": "100"},      # Initialize data (first time only)
    set_data={"gold": "50"},      # Force set data (overwrites every time)
    defaults=[                    # Default jump (when no conditional options)
        {"condition": "hp <= 0", "node_id": "game_over"},
        {"condition": "True", "node_id": "next"}  # else branch
    ],
    end_desc="Game over text",    # Ending text (setting this makes it an ending node)
    on_load="...",                # Script on load (before data)
    on_ready="...",               # Script when ready (after data)
    on_move="..."                 # Script when leaving node
)
```

## 5. Option Parameters Detailed

```python
Option(
    game=game,
    option_id="fight",            # Unique identifier
    name="Fight",                 # Display text
    desc="Fight the monster",     # Description
    next_node_id="battle_room",   # Target node ID
    move_condition="hp >= 20",    # Clickable condition (expression, direct variable name)
    show_condition="has_sword",   # Display condition (expression, direct variable name)
    cant_move_desc="Insufficient HP"  # Hint when move_condition not met
)
```

**Notes**:
- `show_condition="False"`: Option completely hidden
- `move_condition="False"`: Option shown but grayed out/unselectable, displays `cant_move_desc`

## 6. Game Instance (Game) Parameters

```python
Game(
    start_node_id="start",        # Starting node ID
    game_name="Game Name",
    init_input=[                  # Character creation input (at game start)
        {
            "prompt": "Enter name:",
            "name": "player_name",      # Variable name
            "converter": "str",         # Conversion function (str/int/float)
            "condition": "len(val) > 0", # Validation condition (val is user input)
            "err_desc": "Cannot be empty"
        },
        {
            "prompt": "Choose class (1-Warrior 2-Mage):",
            "name": "job",
            "converter": "int",
            "condition": "val in [1, 2]", # Validate input value
            "err_desc": "Please enter 1 or 2"
        }
    ]
)
```

## 7. Common Pitfalls and Solutions

### Pitfall 1: init_data not yet applied during on_load
**Symptom**: Accessing `max_hp` in `on_load` raises "name 'max_hp' is not defined"

**Solution**: Need default value check, or use `getattr` for safe access:
```python
on_load=""
# Method 1: Provide default value directly
if 'max_hp' not in dir():  # Or check if already defined
    data['max_hp'] = 100

# Method 2: Use getattr (recommended)
max_hp = getattr(data, 'max_hp', 100)
""
```

### Pitfall 2: Using data['key'] in expressions
**Symptom**: `move_condition="data['hp'] > 0"` raises "name 'data' is not defined"

**Solution**: Expression environment **has no data variable**, use `hp > 0` directly

### Pitfall 3: Script assignment without data[]
**Symptom**: `on_ready="hp = 100"` but HP doesn't change

**Solution**: `hp = 100` just creates a local variable, must use `data['hp'] = 100`

### Pitfall 4: Boolean vs String
**Symptom**: Conditional checks fail

**Solution**: Boolean values in `init_data`/`set_data` must be **strings**:
```python
# Correct
init_data={"has_key": "False", "is_alive": "True"}

# Incorrect (this is Python boolean, will evaluate to True/False literal, may cause type errors)
init_data={"has_key": False}  
```

### Pitfall 5: Node not registered
**Symptom**: `KeyError: 'node_id'`

**Solution**: Don't forget `game.add_node(node)`

## 8. Complete Correct Example

```python
from TextAdventure import Game, Node, Option

game = Game(
    start_node_id="start",
    game_name="Test Game",
    init_input=[
        {"prompt": "Name:", "name": "name", "converter": "str", 
         "condition": "len(val) > 0", "err_desc": "Cannot be empty"}
    ]
)

# Start node
start = Node(
    game=game,
    node_id="start",
    name="Starting Point",
    desc="Welcome, {name}! You have {gold} gold.",
    init_data={"gold": "10", "hp": "100"},
    on_ready="print('Game started!')"
)

# Shop option (requires gold >= 5)
shop_op = Option(
    game=game,
    option_id="shop",
    name="Go to Shop",
    move_condition="gold >= 5",      # Direct variable name
    next_node_id="shop"
)

start.add_option(shop_op)
game.add_node(start)

# Shop node
shop = Node(
    game=game,
    node_id="shop",
    name="Shop",
    desc="Bought something, gold changed from {gold} to {gold}-2",
    set_data={"gold": "gold - 2"},    # Expression uses direct variable name
    defaults=[{"condition": "True", "node_id": "start"}]  # Auto return
)
game.add_node(shop)

game.play()
```

## 9. Debugging Tips

1. **Print variables**: Use `print(f"Debug: hp={hp}, gold={gold}")` in `on_ready`
2. **Check data**: `print(list(data.data.keys()))` to view all available variables
3. **Type check**: `print(type(job))` to ensure class and other variables are expected int/str

---

**Remember the mantra**:
- Expressions (condition/set_data): **Read-only, use direct variable names**
- Scripts (on_load/on_ready): **Read directly, write requires data[]**
- Data order: **on_load → init_data → set_data → on_ready**
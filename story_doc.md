# TextAdventure 文档

## 1. 初始化

### 1.1 克隆仓库

```bash
git clone https://github.com/zaf-x/TextAdventure
cd TextAdventure
source venv/bin/activate
```

这将把仓库克隆到你的本地机器，并为你准备好引擎。
你创建的所有文件都应该在引擎的根目录（`.`）中。

**警告：**
<span style="color: orange; font-weight: bold;">
除非你知道自己在做什么，否则不要在 `./TextAdventure/` 目录中创建任何文件。
</span>

**注意：**
引擎需要 venv，你需要在运行引擎之前激活它。`source venv/bin/activate`

### 1.2 创建新的故事文件

在根目录下创建一个以你的故事名称命名的 Python 文件。例如，`my_story.py`。

文件夹结构应该如下所示：

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

### 1.3 导入

在你的故事文件顶部添加以下行：

```python
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option
```

就是这样！你现在可以开始写你的故事了。

## 2. 故事格式

### 2.1 游戏结构

游戏由节点组成。每个节点代表你故事中的一个场景。
游戏从第一个节点开始。你可以在 `Game` 类中配置起始节点 ID。

默认起始节点 ID 是 `"start"`。

每个节点都有一个唯一的 ID，并且可以包含跳转到其他节点的选项。

创建游戏：

```python
game = Game(
    game_name="My Story",
    start_node_id="start"  # 可选，默认为 "start"
)
```

**游戏字段：**

| 字段 | 类型 | 必需 | 描述 |
|-------|------|----------|-------------|
| `game_name` | `str` | 否 | 游戏名称。默认：`"TextAdventure"`。 |
| `start_node_id` | `str` | 否 | 起始节点的 ID。默认：`"start"`。 |
| `init_input` | `list[dict]` | 否 | 初始角色创建输入。参见第 2.8 节。 |
| `io_handler` | `IOHandler` | 否 | 自定义 IO 处理器。参见第 2.9 节。默认：内置 `IOHandler`。 |

### 2.2 节点

使用 `Node` 类创建一个节点：

```python
node = Node(
    game=game,
    node_id="start",
    name="Start",
    desc="You are at the start of the game."
)
```

**节点字段：**

| 字段 | 类型 | 必需 | 描述 |
|-------|------|----------|-------------|
| `game` | `Game` | **是** | 该节点所属的游戏实例。 |
| `node_id` | `str` | **是** | 节点的唯一 ID。必须在所有节点中唯一。 |
| `name` | `str` | 否 | 节点名称（显示给玩家）。默认：`""`。 |
| `desc` | `str` | 否 | 描述文本。支持 `{variable}` 格式化。默认：`""`。 |
| `end_desc` | `str` | 否 | 如果设置，这是一个结局节点。游戏结束时显示的文本。默认：`""`。 |
| `options` | `list[Option]` | 否 | 选项列表。也可以通过 `add_option()` 添加。默认：`[]`。 |
| `init_data` | `dict` | 否 | 仅在变量不存在时设置的数据。格式：`{"var": "expression"}`。默认：`{}`。 |
| `set_data` | `dict` | 否 | 访问节点时设置的数据。格式：`{"var": "expression"}`。默认：`{}`。 |
| `defaults` | `list[dict]` | 否 | 自动跳转条件。`[{"condition": "expr", "node_id": "next"}]`。默认：`[]`。 |
| `on_load` | `str` | 否 | 节点加载时执行的 Python 代码（数据更改之前）。默认：`""`。 |
| `on_ready` | `str` | 否 | 节点就绪时执行的 Python 代码（数据更改之后）。默认：`""`。 |
| `on_move` | `str` | 否 | 离开节点时执行的 Python 代码。默认：`""`。 |

#### 数据系统（init_data 和 set_data）

两个字段都接受一个 Python 字典，其中**键是变量名**，**值是将被计算的字符串表达式**：

```python
node = Node(
    game=game,
    node_id="example",
    name="Example",
    desc="You have {coins} coins.",
    init_data={
        "coins": "100",           # 设置 coins 为 100（整数）
        "has_key": "False",       # 设置 has_key 为 False（布尔值）
        "player_name": "\"Alex\"" # 设置 player_name 为 "Alex"（字符串）
    },
    set_data={
        "visited_count": "visited_count + 1"  # 递增计数器
    }
)
```

**重要：** 值必须是**包含有效 Python 表达式的字符串**，而不是实际值：
- ✅ 正确：`"100"`（计算为整数 100）
- ❌ 错误：`100`（整数，会导致错误）

Python 中所有可用的类型在数据中也可用。

#### 自动跳转（defaults）

使节点根据条件自动重定向到另一个节点：

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

条件按顺序计算。第一个为 True 的条件触发跳转。

#### 结局节点

通过设置 `end_desc` 创建一个结局：

```python
ending = Node(
    game=game,
    node_id="victory",
    name="Victory",
    desc="You defeated the final boss!",
    end_desc="Congratulations! You have completed the game.\nThanks for playing!"
)
```

当玩家到达此节点时，游戏显示结局描述并终止。

### 2.3 选项

选项允许玩家做出选择：

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

**选项字段：**

| 字段 | 类型 | 必需 | 描述 |
|-------|------|----------|-------------|
| `game` | `Game` | **是** | 该选项所属的游戏实例。 |
| `option_id` | `str` | **是** | 该选项的唯一 ID（在节点内唯一）。 |
| `name` | `str` | 否 | 选择的显示文本。默认：`""`。 |
| `desc` | `str` | 否 | 显示给玩家的额外描述。默认：`""`。 |
| `next_node_id` | `str` | 否 | 选择时跳转到的节点 ID。默认：`"start"`。 |
| `move_condition` | `str` | 否 | Python 表达式。如果为 False，选项被禁用。默认：`"True"`。 |
| `show_condition` | `str` | 否 | Python 表达式。如果为 False，选项被隐藏。默认：`"True"`。 |
| `cant_move_desc` | `str` | 否 | 选项可见但禁用时显示的文本。默认：`""`。 |

#### 条件选项

```python
locked_door = Option(
    game=game,
    option_id="open_door",
    name="Open the Door",
    desc="Try to open the heavy door.",
    next_node_id="throne_room",
    move_condition="has_key == True",
    cant_move_desc="The door is locked. You need a key.",
    show_condition="True"  # 始终显示，但有时禁用
)
```

### 2.4 脚本

对于无法通过 `init_data`/`set_data` 处理的复杂逻辑，使用脚本字段：`on_load`、`on_ready`、`on_move`。

**执行顺序：**
1. 节点加载
2. 执行 `on_load`
3. 应用 `init_data`/`set_data`
4. 执行 `on_ready`
5. 显示节点描述和选项
6. 玩家做出选择
7. 执行 `on_move`
8. 跳转到下一个节点

**访问共享数据：**
- 读取：直接使用变量（例如 `print(f"HP: {player_hp}")`）
- 写入：使用 `data["var_name"] = value`（⚠️ 永远不要使用 `var_name = value` - 这会创建局部变量！）

**特殊变量：**
- `this`：当前的 Node 实例
- `data`：共享的 Data 实例（也可以作为独立变量访问）

**警告：**
<font style="color: orange; font-weight: bold">
永远不要在脚本中编写静态描述。改用 `desc` 字段。
</font>

示例：
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
        # 你可以在这里修改数据
        data["combat_started"] = True
    """,
    on_move="""
        if enemy_hp <= 0:
            print("Victory!")
            data["xp"] = xp + 50
    """
)
```

### 2.5 高级脚本

#### 动态选项管理

你可以在脚本中以编程方式添加或删除选项：

```python
on_ready="""
    # 添加动态选项
    if has_secret_knowledge:
        new_opt = Option(
            game=game,
            option_id="secret_path",
            name="Take Secret Path",
            desc="You know a shortcut.",
            next_node_id="hidden_room"
        )
        this.add_option(new_opt)
    
    # 通过 ID 删除选项
    this.del_option_by_id("useless_option")
    
    # 通过条件删除
    this.del_option_by_map(lambda opt: "temp_" in opt.option_id)
"""
```

#### 脚本中的模块导入

你可以在脚本中导入安全模块：

```python
on_ready="""
    import random
    import math
    
    damage = random.randint(10, 20)
    crit_chance = math.sqrt(dexterity) * 0.1
    
    print(f"Damage roll: {damage}")
    
    # 要在其他节点中使用，注入到 data 中：
    data["random"] = random
    data["math"] = math
"""
```

**允许的模块：** `math`、`random`、`datetime`、`calendar`、`json`、`time`、`numpy`

**重要：** 导入仅限于该特定脚本。要在节点之间重用，请如上所示将模块存储在 `data` 中。

### 2.6 从文件加载脚本（长脚本分离）

对于复杂逻辑（10+ 行），将脚本写在单独的 `.py` 文件中并加载：

**文件：`scripts/combat_system.py`**
```python
import random

# 直接访问共享数据
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

**在你的故事文件中：**
```python
battle_node = Node(
    game=game,
    node_id="combat",
    name="Combat Encounter",
    desc="A hostile creature attacks!"
)

# 从文件加载脚本
battle_node.load_onload("scripts/init_combat.py")      # 在数据更改前运行
battle_node.load_onready("scripts/combat_system.py")   # 在数据更改后运行
battle_node.load_onmove("scripts/end_combat.py")       # 在离开时运行
```

**好处：**
- 完整的 IDE 支持（语法高亮、代码检查）
- 更容易调试（错误消息显示文件名）
- 更干净的主故事文件

### 2.7 存档和读档系统

引擎支持使用 Python 的 pickle 模块进行保存和加载游戏状态。

**保存：**
```python
# 在你的代码中的任何地方，或游戏结束后
game.dump("save_file.pkl")
```

**加载：**
```python
# 加载已保存的游戏
loaded_game = Game.load("save_file.pkl")
loaded_game.play()  # 从上次离开的地方继续
```

**使用示例：**
```python
# 在你的游戏中添加一个保存选项
save_option = Option(
    game=game,
    option_id="save_game",
    name="Save Game",
    desc="Save your progress.",
    next_node_id="current"  # 停留在同一节点
)

# 在节点的 on_move 中或通过自定义逻辑，调用 game.dump()
```

**注意：** 存档文件存储整个游戏状态，包括所有节点、共享数据和当前位置。

### 2.8 角色创建（init_input）

在游戏开始时配置初始玩家输入：

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

**初始输入字段：**

| 字段 | 类型 | 必需 | 描述 |
|-------|------|----------|-------------|
| `prompt` | `str` | **是** | 请求输入时显示给玩家的文本。 |
| `name` | `str` | **是** | 存储输入值的共享数据中的变量名。 |
| `converter` | `str` | 否 | 转换输入的 Python 表达式。默认：`"str"`。示例：`"int"`、`"str.lower"`、`"lambda x: x.strip()"`。 |
| `condition` | `str` | 否 | 验证表达式（使用 `val` 引用转换后的值）。默认：`"True"`。 |
| `err_desc` | `str` | **是** | 验证失败时显示的错误消息。 |

### 2.9 自定义 IO 处理器

对于自定义界面（GUI、Web 等），继承 `IOHandler`：

```python
from TextAdventure import IOHandler

class WebIOHandler(IOHandler):
    def show_node(self, node):
        # 自定义显示逻辑
        print(f"<h1>{node.name}</h1>")
        print(f"<p>{node.desc}</p>")
    
    def show_options(self, ava_op, dis_op):
        # 返回选中的选项对象
        # 实现你自己的输入机制
        pass
    
    def get_init_input(self, prompt):
        # 自定义输入方法
        return input(prompt)

# 使用自定义处理器
game = Game(
    game_name="Web Adventure",
    io_handler=WebIOHandler(Data())
)
```

**你可以覆盖的方法：**
- `show_node(node)`：显示节点内容
- `show_options(ava_op, dis_op)`：显示选择，返回选中的 Option
- `show_end(node)`：显示结局
- `get_init_input(prompt)`：获取初始角色创建输入
- `show_init_input_error(err_desc, user_input)`：显示验证错误

## 3. 附录

### 3.1 调试技巧

如果你遇到如下错误：
```
[ERROR] 节点 'x' 的 set_data['y'] = 'z' 执行失败: name 'abc' is not defined
```

检查：
1. `init_data`/`set_data` 中的变量表达式是有效的 Python
2. 表达式中引用的变量存在（由前面的节点或 `init_data` 设置）
3. 表达式中的字符串正确引号：`"\"text\""` 而不是 `"text"`

### 3.2 完整最小示例

```python
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option

# 创建游戏
game = Game(game_name="The Cave")

# 创建节点
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

# 创建选项
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

# 添加返回选项
back = Option(
    game=game,
    option_id="back",
    name="Go Back",
    desc="Return to entrance.",
    next_node_id="start"
)
cave.add_option(back)

# 运行
if __name__ == "__main__":
    game.play()
```
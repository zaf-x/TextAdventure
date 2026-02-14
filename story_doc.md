# TextAdventure 游戏脚本编写指南

## 1. 文件结构

```python
from TextAdventure import Game, Node, Option

# 1. 创建游戏实例
game = Game(start_node_id="start", game_name="游戏名")

# 2. 定义节点
node = Node(game, node_id="...", name="...", desc="...")

# 3. 定义选项
option = Option(game, option_id="...", name="...", next_node_id="...")

# 4. 组装
node.add_option(option)
game.add_node(node)

# 5. 运行
game.play()
```

## 2. 数据机制（关键）

### 执行顺序（重要！）
节点加载时的执行顺序：
1. **on_load** 脚本执行
2. **init_data** 应用（仅当变量不存在时）
3. **set_data** 应用（每次都覆盖）
4. **on_ready** 脚本执行

### 数据定义方式

| 属性 | 作用 | 执行时机 | 语法特点 |
|------|------|----------|----------|
| `init_data` | 初始化默认值 | 首次进入节点（仅当变量不存在） | `{"hp": "100"}` 字符串表达式 |
| `set_data` | 强制设置/覆盖 | 每次进入节点都执行 | `{"hp": "hp + 10"}` 可使用当前变量 |
| `on_load` | 准备脚本 | 数据应用**前**执行 | 用于初始化检查，**此时 init_data 还未应用** |
| `on_ready` | 就绪脚本 | 数据应用**后**执行 | 用于逻辑处理，**此时所有数据已就绪** |

## 3. 变量访问规则（核心）

### 规则区分

**A. 表达式环境（只读）**
- 使用场景：`set_data` 的值、`move_condition`、`show_condition`、`defaults` 的 `condition`
- 访问方式：**直接变量名**（如 `hp`, `gold >= 100`, `job == 1`）
- 限制：只读，不能赋值

```python
# 正确
set_data={"gold": "gold + 50", "hp": "min(hp + 10, max_hp)"}
move_condition="level >= 2 and has_key"
show_condition="job == 1"  # 只有战士可见
```

**B. 脚本环境（读写）**
- 使用场景：`on_load`, `on_ready`, `on_move`
- 读取：**直接变量名**（如 `if hp > max_hp:`）
- 写入：**必须通过 data 对象**（如 `data['hp'] = 100`）

```python
# 正确
on_ready=""
if hp > max_hp:
    data['hp'] = max_hp  # 写操作必须带 data[]
print(f"当前HP: {hp}")     # 读操作直接用变量名
""

# 错误
on_ready=""
hp = 100          # 错误！这只是创建局部变量
data[hp] = 100    # 错误！字典key应该是字符串 'hp'
""
```

## 4. 节点（Node）参数详解

```python
Node(
    game=game,                    # 游戏实例（必须）
    node_id="start",              # 唯一标识（必须）
    name="开始",                  # 显示名称
    desc="描述文本",              # 描述（支持 {变量} 格式化）
    init_data={"hp": "100"},      # 初始化数据（首次有效）
    set_data={"gold": "50"},      # 强制设置数据（每次覆盖）
    defaults=[                    # 默认跳转（无条件选项时）
        {"condition": "hp <= 0", "node_id": "game_over"},
        {"condition": "True", "node_id": "next"}  # else 分支
    ],
    end_desc="游戏结束文本",      # 结局文本（设置此字段则为结局节点）
    on_load="...",                # 加载时脚本（数据前）
    on_ready="...",               # 就绪时脚本（数据后）
    on_move="..."                 # 离开节点时脚本
)
```

## 5. 选项（Option）参数详解

```python
Option(
    game=game,
    option_id="fight",            # 唯一标识
    name="战斗",                  # 显示文本
    desc="与怪物战斗",            # 描述
    next_node_id="battle_room",   # 目标节点ID
    move_condition="hp >= 20",    # 可点击条件（表达式，直接变量名）
    show_condition="has_sword",   # 显示条件（表达式，直接变量名）
    cant_move_desc="HP不足"       # 不满足 move_condition 时的提示
)
```

**注意**：
- `show_condition="False"`：选项完全隐藏
- `move_condition="False"`：选项显示但灰色/不可选，显示 `cant_move_desc`

## 6. 游戏实例（Game）参数

```python
Game(
    start_node_id="start",        # 起始节点ID
    game_name="游戏名",
    init_input=[                  # 角色创建输入（游戏开始时）
        {
            "prompt": "请输入姓名：",
            "name": "player_name",      # 变量名
            "converter": "str",         # 转换函数（str/int/float）
            "condition": "len(val) > 0", # 验证条件（val 是用户输入）
            "err_desc": "不能为空"
        },
        {
            "prompt": "选择职业(1-战士 2-法师)：",
            "name": "job",
            "converter": "int",
            "condition": "val in [1, 2]", # 验证输入值
            "err_desc": "请输入1或2"
        }
    ]
)
```

## 7. 常见陷阱与解决

### 陷阱1：on_load 时 init_data 还未应用
**现象**：`on_load` 中访问 `max_hp` 报错 "name 'max_hp' is not defined"

**解决**：需要默认值检查，或用 `getattr` 安全访问：
```python
on_load=""
# 方法1：直接提供默认值
if 'max_hp' not in dir():  # 或检查是否已定义
    data['max_hp'] = 100

# 方法2：使用 getattr（推荐）
max_hp = getattr(data, 'max_hp', 100)
""
```

### 陷阱2：表达式中用了 data['key']
**现象**：`move_condition="data['hp'] > 0"` 报错 "name 'data' is not defined"

**解决**：表达式环境**没有 data 变量**，直接用 `hp > 0`

### 陷阱3：脚本中赋值未用 data[]
**现象**：`on_ready="hp = 100"` 后 HP 没变

**解决**：`hp = 100` 只是创建局部变量，必须用 `data['hp'] = 100`

### 陷阱4：布尔值 vs 字符串
**现象**：条件判断失效

**解决**：`init_data`/`set_data` 中的布尔值必须是**字符串**：
```python
# 正确
init_data={"has_key": "False", "is_alive": "True"}

# 错误（这是Python布尔值，会被求值为True/False字面量，可能导致类型错误）
init_data={"has_key": False}  
```

### 陷阱5：节点未注册
**现象**：`KeyError: 'node_id'`

**解决**：别忘了 `game.add_node(node)`

## 8. 完整正确示例

```python
from TextAdventure import Game, Node, Option

game = Game(
    start_node_id="start",
    game_name="测试游戏",
    init_input=[
        {"prompt": "姓名：", "name": "name", "converter": "str", 
         "condition": "len(val) > 0", "err_desc": "不能为空"}
    ]
)

# 开始节点
start = Node(
    game=game,
    node_id="start",
    name="起点",
    desc="欢迎，{name}！你有 {gold} 金币。",
    init_data={"gold": "10", "hp": "100"},
    on_ready="print('游戏开始！')"
)

# 商店选项（需要金币>=5）
shop_op = Option(
    game=game,
    option_id="shop",
    name="去商店",
    move_condition="gold >= 5",      # 直接变量名
    next_node_id="shop"
)

start.add_option(shop_op)
game.add_node(start)

# 商店节点
shop = Node(
    game=game,
    node_id="shop",
    name="商店",
    desc="买了东西，金币从 {gold} 变成 {gold}-2",
    set_data={"gold": "gold - 2"},    # 表达式用直接变量名
    defaults=[{"condition": "True", "node_id": "start"}]  # 自动返回
)
game.add_node(shop)

game.play()
```

## 9. 调试技巧

1. **打印变量**：在 `on_ready` 中使用 `print(f"调试: hp={hp}, gold={gold}")`
2. **检查数据**：`print(list(data.data.keys()))` 查看所有可用变量
3. **类型检查**：`print(type(job))` 确保职业等变量是预期的 int/str

---

**记住口诀**：
- 表达式（condition/set_data）：**只读，直接用变量名**
- 脚本（on_load/on_ready）：**读直接用，写要加 data[]**
- 数据顺序：**on_load → init_data → set_data → on_ready**
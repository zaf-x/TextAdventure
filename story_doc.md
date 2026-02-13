
# TextAdventure 剧本格式说明

## 概述

本引擎使用 JSON 格式定义文字冒险游戏剧本，支持变量系统、条件分支、Python 脚本、初始化输入等高级功能。

---

## 根级结构

```json
{
    "name": "游戏名称",
    "start_node": "起始节点ID",
    "shared_data": {
        "全局变量名": "初始值"
    },
    "init_inputs": {
        "变量名": {
            "desc": "提示文本",
            "converter": "类型转换函数",
            "condition": "验证条件表达式",
            "condition_desc": "验证失败提示"
        }
    },
    "onready_script": "游戏开始时执行的Python脚本",
    "nodes": {
        "节点ID": { ...节点定义... }
    }
}
```

---

## 字段详解

### 1. 基本信息

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `name` | string | 是 | 游戏名称 |
| `start_node` | string | 是 | 起始节点的ID，对应`nodes`中的键 |
| `shared_data` | dict | 否 | 全局共享变量，所有节点可读写 |
| `init_inputs` | dict | 否 | 游戏开始时的玩家输入配置 |
| `onready_script` | string | 否 | 准备阶段执行的Python脚本 |
| `nodes` | dict | 是 | 所有节点的定义 |

---

### 2. 初始化输入 (init_inputs)

用于游戏开始时收集玩家信息（如角色名、属性点分配等）。

```json
"init_inputs": {
    "player_name": {
        "desc": "请输入你的角色名: ",
        "converter": "str",
        "condition": "len(val) > 0 and len(val) <= 10",
        "condition_desc": "角色名长度必须在1-10个字符之间"
    },
    "player_age": {
        "desc": "请输入你的年龄: ",
        "converter": "int",
        "condition": "val >= 18 and val <= 60",
        "condition_desc": "年龄必须在18-60岁之间"
    }
}
```

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `desc` | string | 是 | 输入提示语 |
| `converter` | string | 否 | 类型转换函数，默认为`str`，支持`int`/`float`/`bool`等 |
| `condition` | string | 否 | 验证表达式，`val`为转换后的值 |
| `condition_desc` | string | 否 | 验证失败时的错误提示 |

---

### 3. 节点定义 (nodes)

每个节点是游戏的一个场景。

```json
"节点ID": {
    "name": "场景名称",
    "description": "场景描述，支持{变量名}插值",
    
    "set_d": {
        "变量名": "表达式"
    },
    "init_d": {
        "变量名": "表达式"
    },
    
    "python_script": "进入节点时执行的脚本",
    "onmove_script": "选择选项后执行的脚本",
    
    "force_select": [
        {
            "condition": "条件表达式",
            "next_node": "目标节点ID"
        }
    ],
    
    "options": {
        "选项名称": {
            "desc": "选项描述",
            "next_node": "目标节点ID",
            "show_condition": "显示条件",
            "move_condition": "可选条件",
            "cant_move_desc": "不可选时的提示"
        }
    },
    
    "end": false,
    "end_description": "结局描述"
}
```

#### 节点字段详解

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `name` | string | 是 | 场景标题 |
| `description` | string | 是 | 场景描述文本，支持`{变量}`插值和`{表达式}`计算 |
| `set_d` | dict | 否 | 每次进入节点都执行的变量赋值 |
| `init_d` | dict | 否 | 仅在变量不存在时执行的初始化赋值 |
| `python_script` | string | 否 | 进入节点时执行的Python代码 |
| `onmove_script` | string | 否 | 选择选项后、跳转前执行的Python代码 |
| `force_select` | array | 否 | 强制跳转规则（按顺序匹配第一个满足条件的）|
| `options` | dict | 否 | 玩家可选择的选项 |
| `end` | bool | 否 | 是否为结局节点 |
| `end_description` | string | 否 | 结局描述文本 |

#### 选项字段详解

| 字段 | 类型 | 必填 | 说明 |
|:---|:---|:---|:---|
| `desc` | string | 是 | 选项描述 |
| `next_node` | string | 是 | 目标节点ID |
| `show_condition` | string | 否 | 显示条件，默认为`"True"` |
| `move_condition` | string | 否 | 可选条件，默认为`"True"` |
| `cant_move_desc` | string | 否 | 不可选时的灰色提示文本 |

---

## 表达式与脚本

### 可用变量

- `shared_data`中定义的所有变量（仅针对表达式，例如condition字段，脚本访问共享数据见下文）
- 节点`set_d`/`init_d`中定义的变量
- 初始化输入收集的变量

### 安全内置函数

```
int, float, str, bool, list, dict, tuple, set
abs, min, max, sum, round, pow, divmod
len, range, enumerate, zip, map, filter, sorted, reversed
all, any, id, hex, oct, bin, print, input
```

### 可用模块

`math`, `random`, `datetime`, `calendar`, `json`, `time`, `numpy`

### 特殊API

在Python脚本中可使用以下函数操作共享数据：

```python
write_data(key, value)  # 写入数据
read_data(key)          # 读取数据
exist_data(key)         # 检查是否存在
```

---

## 完整示例剧本

```json
{
    "name": "古堡探险",
    "start_node": "entrance",
    "shared_data": {
        "hp": 100,
        "gold": 0,
        "has_key": false,
        "torch_count": 0
    },
    "init_inputs": {
        "player_name": {
            "desc": "请输入冒险者姓名: ",
            "converter": "str",
            "condition": "len(val) > 0",
            "condition_desc": "姓名不能为空"
        }
    },
    "onready_script": "import random\nwrite_data('luck', random.randint(1, 100))\nprint(f'欢迎,{read_data(\"player_name\")}! 你的幸运值是:{read_data(\"luck\")}')",
    "nodes": {
        "entrance": {
            "name": "古堡大门",
            "description": "你站在一座阴森的古堡前，大门虚掩着。你身上带着{gold}枚金币，{torch_count}个火把。\n生命值: {hp}/100",
            "set_d": {
                "visit_entrance": "visit_entrance + 1 if exist_data('visit_entrance') else 1"
            },
            "options": {
                "进入大门": {
                    "desc": "推开沉重的铁门",
                    "next_node": "hall",
                    "move_condition": "hp > 0",
                    "cant_move_desc": "你已经没有力气了"
                },
                "检查口袋": {
                    "desc": "看看还有什么物资",
                    "next_node": "check_inventory"
                },
                "离开": {
                    "desc": "这地方太诡异了，回家吧",
                    "next_node": "give_up",
                    "show_condition": "visit_entrance >= 2"
                }
            }
        },
        "hall": {
            "name": "大厅",
            "description": "昏暗的大厅里只有几缕月光。你听到楼上传来奇怪的声音。",
            "python_script": "if read_data('torch_count') == 0:\n    print('太黑了，你需要一个火把！')",
            "force_select": [
                {
                    "condition": "torch_count == 0",
                    "next_node": "dark_death"
                }
            ],
            "options": {
                "上楼": {
                    "desc": "去二楼查看",
                    "next_node": "second_floor"
                },
                "搜索大厅": {
                    "desc": "找找有用的东西",
                    "next_node": "search_hall"
                },
                "返回": {
                    "desc": "回到大门",
                    "next_node": "entrance"
                }
            }
        },
        "search_hall": {
            "name": "搜索大厅",
            "description": "你在角落里发现了一个火把！",
            "set_d": {
                "torch_count": "torch_count + 1"
            },
            "options": {
                "继续": {
                    "desc": "返回大厅",
                    "next_node": "hall"
                }
            }
        },
        "second_floor": {
            "name": "二楼走廊",
            "description": "走廊尽头有一扇上锁的门。你{ '有' if has_key else '没有' }钥匙。",
            "options": {
                "开门": {
                    "desc": "尝试打开房门",
                    "next_node": "treasure_room",
                    "move_condition": "has_key",
                    "cant_move_desc": "需要钥匙"
                },
                "返回大厅": {
                    "desc": "下楼",
                    "next_node": "hall"
                }
            }
        },
        "treasure_room": {
            "name": "藏宝室",
            "description": "你找到了传说中的宝藏！金币闪闪发光。",
            "set_d": {
                "gold": "gold + 1000"
            },
            "end": true,
            "end_description": "恭喜你，{player_name}！你带着{gold}枚金币成为了传奇冒险者！"
        },
        "dark_death": {
            "name": "黑暗中的悲剧",
            "description": "你在黑暗中迷失了方向...",
            "end": true,
            "end_description": "你没能走出古堡。{player_name}的名字被刻在了失踪者名单上。"
        },
        "give_up": {
            "name": "放弃",
            "description": "你决定不再冒险。",
            "end": true,
            "end_description": "有时候，活着回来就是最好的结局。你带着{gold}枚金币回家了。"
        }
    }
}
```

---

## 高级技巧

### 1. 动态描述

描述文本支持两种插值方式：

- **简单变量**: `{player_name}`, `{hp}`
- **表达式计算**: `{gold * 2}`, `{'有' if has_key else '没有'}`

### 2. 条件显示与可用

```json
"选项名": {
    "show_condition": "quest_completed == true",
    "move_condition": "level >= 10",
    "cant_move_desc": "需要等级10"
}
```

- `show_condition`为`false`时选项完全隐藏
- `show_condition`为`true`但`move_condition`为`false`时显示为灰色不可选

### 3. 强制跳转

用于剧情杀、自动触发等场景：

```json
"force_select": [
    {"condition": "hp <= 0", "next_node": "game_over"},
    {"condition": "has_item('诅咒')", "next_node": "cursed_ending"}
]
```

### 4. 变量初始化策略

| 指令 | 执行时机 | 用途 |
|:---|:---|:---|
| `set_d` | 每次进入节点 | 计数器、状态更新 |
| `init_d` | 仅变量不存在时 | 一次性初始化、默认值 |

---

## 注意事项

1. **JSON格式**: 确保JSON语法正确，字符串中的引号需转义
2. **Python脚本**: 使用4空格缩进，注意换行符在JSON中的处理
3. **安全性**: 脚本在受限环境中运行，无法访问文件系统或网络
4. **节点ID**: 建议使用有意义的英文标识符，避免空格和特殊字符
5. **循环检测**: 引擎不自动检测节点循环，请自行避免无限循环
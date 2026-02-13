TextAdventure

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

一个基于 Python 的文字冒险游戏引擎，使用 JSON 定义剧本，支持变量系统、条件分支、Python 脚本和初始化输入。

[English](#english) | [中文](#中文)

---

## 中文

### 特性

- 🎮 **纯文本驱动** - 使用 JSON 编写游戏剧本，无需编程基础
- 🧮 **变量系统** - 支持全局变量、条件判断和动态计算
- 🐍 **Python 脚本** - 可在节点中执行 Python 代码（安全沙箱）
- 🎯 **条件分支** - 选项可根据条件显示或禁用
- 💾 **存档系统** - 支持 pickle 序列化保存进度
- 🎨 **文本渲染** - 支持变量插值和表达式计算

### 快速开始

```bash
# 克隆仓库
git clone https://github.com/BaoShuWen/TextAdventure.git
cd TextAdventure

# 运行示例
python TextAdventure.py
```

### 项目结构

```
TextAdventure/
├── TextAdventure.py      # 主程序
├── consts.py             # 常量配置（安全内置函数、消息模板）
├── stories/              # 游戏剧本目录
│   └── test.json         # 示例剧本
├── saves/                # 存档目录（自动生成）
└── README.md             # 本文件
```

### 示例剧本

```json
{
  "name": "古堡探险",
  "start_node": "entrance",
  "shared_data": {
    "hp": 100,
    "gold": 0
  },
  "nodes": {
    "entrance": {
      "name": "古堡大门",
      "description": "你站在一座阴森的古堡前，生命值: {hp}",
      "options": {
        "进入大门": {
          "desc": "推开沉重的铁门",
          "next_node": "hall",
          "move_condition": "hp > 0"
        }
      }
    }
  }
}
```

### 完整文档

详见 [story_doc.md](./story_doc.md)

---

## English

### Features

- 🎮 **Text-Driven** - Write game scripts in JSON, no programming required
- 🧮 **Variable System** - Global variables, conditions and dynamic calculations
- 🐍 **Python Scripts** - Execute Python code in nodes (safe sandbox)
- 🎯 **Conditional Branching** - Show/disable options based on conditions
- 💾 **Save System** - Pickle serialization for progress saving
- 🎨 **Text Rendering** - Variable interpolation and expression evaluation

### Quick Start

```bash
git clone https://github.com/BaoShuWen/TextAdventure.git
cd TextAdventure
python TextAdventure.py
```

### Documentation

See [story_doc.md](./story_doc.md) for full documentation (Chinese only for now).

---

## 技术细节 / Technical Details

### 安全机制

- Python 脚本运行在受限环境中
- 仅允许白名单内置函数和模块（`math`, `random`, `datetime` 等）
- 文件系统访问被隔离

### 依赖

- Python 3.8+
- 无第三方依赖（标准库 only）

---

## 贡献 / Contributing

欢迎 Issue 和 PR！

## 许可证 / License

[MIT](./LICENSE)

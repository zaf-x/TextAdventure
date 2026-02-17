# TextAdventure -- Text Adventure Engine
## For english version -> [Here](./readme-en.md)

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Python 原生的文本冒险游戏引擎。没有 DSL，没有可视化编辑器，纯代码驱动——像写 Python 一样写互动小说。**

完整文档（从头开始教你如何写一个文本冒险游戏）-> [story_doc.md](./story_doc.md)

如果你曾想在 Twine 里写复杂战斗系统、在 Ren'Py 里做纯文本终端游戏，或者单纯想用 Git 管理你的叙事分支——这就是你要的引擎。

---

## ✨ 核心特性

- **🐍 纯 Python，零学习成本** - 没有专属脚本语言，会 Python 就会写。直接 import 任意库（numpy, pandas, AI 模型）。
- **📊 数据驱动设计** - 内置 `init_data`/`set_data` 系统，RPG 数值、物品栏、任务状态一手掌控。
- **⚡ 三阶段生命周期** - `on_load` → `on_ready` → `on_move` 精确控制每个节点的执行时机。
- **🔧 完全可定制的 IO** - 通过 `IOHandler` 接口，同一套代码可运行在终端、Web、GUI 或 API 上。
- **💾 原生存档系统** - 基于 pickle 的完整状态序列化，支持随时保存/加载。
- **🌲 Git 友好** - 全是 .py 文件，版本控制、代码审查、CI/CD 开箱即用。

[开发者文档](./story_doc.md)

---

## 🚀 30 秒上手

Linux:
````bash
git clone https://github.com/zaf-x/TextAdventure.git 
cd TextAdventure
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 example.py
````

Windows:
````bash
git clone https://github.com/zaf-x/TextAdventure.git 
cd TextAdventure
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python example.py
````

然后选择选项，开始你的冒险。

---

## 📝 一分钟示例

````
#!/usr/bin/env python3
from TextAdventure import Game, Node, Option

# 创建游戏
game = Game(game_name="地下城入门")

# 定义节点：带有状态管理
entrance = Node(
    game=game,
    node_id="entrance",
    name="洞穴入口",
    desc="你站在黑暗的入口。火把剩余: {torches}",
    init_data={"torches": "3", "hp": "100"},
    set_data={"visited": "visited + 1"}
)

# 定义选项：带条件判断
deep_cave = Option(
    game=game,
    option_id="enter",
    name="深入洞穴",
    desc="进入黑暗...",
    next_node_id="boss_room",
    move_condition="torches > 0",
    cant_move_desc="太黑了，你需要火把！"
)

# 添加选项并运行
entrance.add_option(deep_cave)

if __name__ == "__main__":
    game.play()
````

觉得写的不好？点击[这里](./story_doc.md)查看完整文档，自己写一个。

---

## 📚 文档

完整文档（包含高级脚本、IOHandler 定制、存档系统等）请查看：

**[📖 story_doc.md](./story_doc.md)**

或快速查阅：
- **创建角色** - 使用 `init_input` 实现开局角色创建
- **复杂逻辑** - `on_ready`/`on_move` 脚本与外部 .py 文件分离
- **自定义界面** - 继承 `IOHandler` 实现 Web 或 GUI 版本
- **调试技巧** - 常见错误排查指南

---

## 🆚 为什么不用 Twine/Ren'Py？

| 场景 | 推荐选择 |
|------|---------|
| 零编程基础，快速做分支小说 | Twine ✅ |
| 视觉小说，需要立绘/音效 | Ren'Py ✅ |
| **复杂数值系统（RPG、Roguelike）** | **TextAdventure ✨** |
| **需要版本控制/单元测试** | **TextAdventure ✨** |
| **嵌入到 Python 项目/数据分析流程** | **TextAdventure ✨** |
| 纯文本终端游戏（SSH/MUD） | **TextAdventure ✨** |

---

## 🤝 贡献

欢迎 PR 和 Issue！特别是：
- 更多 IOHandler 实现（Web、Discord Bot、TUI）
- 示例游戏（RPG、解谜、叙事）
- Bug 修复和性能优化

---

## 📄 许可证

MIT License - 自由使用，自由修改。
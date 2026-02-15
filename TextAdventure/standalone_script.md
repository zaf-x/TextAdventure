# Standalone Script Creator 使用说明

将 TextAdventure 游戏打包为独立可执行脚本，分发时无需携带引擎库文件。

---

## 功能简介

该工具将：
1. 解析你的游戏脚本（如 `hotel_detective.py`）
2. 合并 TextAdventure 引擎核心代码
3. 序列化游戏数据（节点、选项、变量等）
4. 生成单个 Python 文件（`standalone.py`）

生成的文件可在**未安装 TextAdventure 的纯净环境**中直接运行。

---

## 前置要求

- Python 3.8+
- 游戏脚本必须导出一个名为 `game` 的 `Game` 实例
- 游戏脚本的 `game.play()` 必须在 `if __name__ == "__main__":` 中，否则在解析脚本阶段会出现不被定义的行为。
- 确保 `TextAdventure.py` 和 `consts.py` 在指定路径存在

错误的实例：
```python
# 其它节点和选项的定义
my_game = Game(...) # 错！必须导出名为 game 的 Game 实例，否则会报错
```

正确的实例：
```python
# 其它节点和选项的定义
game = Game(...) # 对！导出名为 game 的 Game 实例
```

---

## 基本用法

### 1. 快速打包（默认配置）

```bash
python standalone_script_creator.py hotel_detective.py
```

生成 `dist/script.py`，双击或在终端运行：
```bash
python dist/script.py
```

### 2. 指定输出文件名

```bash
python standalone_script_creator.py hotel_detective.py --out_path 雨夜旅馆.py
```

### 3. 自定义依赖路径（非标准目录结构时使用）

```bash
python standalone_script_creator.py \
    mygame/story.py \
    --talib_path libs/TextAdventure.py \
    --consts libs/consts.py \
    --out_path releases/我的游戏_v1.0.py
```

### 4. PyInstaller 打包

为了生成独立的可执行文件，推荐使用 [PyInstaller](https://pyinstaller.org/en/stable/)：

```bash
pip install pyinstaller
pyinstaller --onefile dist/script.py
```

这将在 `dist/` 目录下生成 `script.exe`（Windows）或 `script`（Linux/macOS）。

---

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `script_path` | ✓ | - | 游戏脚本路径，必须包含 `game = Game(...)` 对象 |
| `--talib_path` | ✗ | `TextAdventure.py` | TextAdventure 引擎文件路径 |
| `--consts` | ✗ | `consts.py` | 常量配置文件路径 |
| `--out_path` | ✗ | `standalone.py` | 生成的独立脚本输出路径 |

---

## 工作流程详解

### 准备阶段
确保你的游戏脚本结构如下：

```python
# hotel_detective.py
from TextAdventure import Game, Node, Option

game = Game(start_node_id="start", game_name="雨夜旅馆")
# ... 配置节点、选项 ...

if __name__ == "__main__":
    game.play()
```

**关键**：脚本中必须存在名为 `game` 的 `Game` 实例。

### 打包阶段
工具执行以下操作：
1. **动态导入**：加载 `script_path` 作为模块，提取 `game` 对象
2. **序列化**：使用 `pickle` 将游戏状态转为 base64 编码
3. **合并代码**：将 `consts.py` + `TextAdventure` + 序列化数据写入新文件
4. **生成启动器**：添加独立运行所需的引导代码

### 运行阶段
生成的 `dist/script.py` 包含完整运行环境：
- 内嵌引擎源码（无需外部 `TextAdventure` 库）
- 内嵌游戏数据（节点、选项、变量初始值）
- 自动反序列化并启动游戏

---

## 注意事项

### 路径问题
- 游戏脚本中使用的**相对路径**（如加载外部文本、图片）在打包后可能失效，建议使用绝对路径或内嵌资源
- 生成的独立脚本与原始脚本**不在同一目录**时，注意资源文件路径

### 数据固化
- 打包时**固化**了当前的 `game` 对象状态
- 若修改了游戏源码，必须**重新打包**才能生效

### 兼容性
- 生成的脚本依赖生成时使用的 Python 版本
- 建议在与目标运行环境相同的 Python 版本下打包

### 安全性
- 生成的脚本包含 base64 编码的 pickle 数据，**不可信来源的独立脚本可能存在安全风险**
- 分发时建议同时提供源码供用户自行打包

---

## 完整示例

假设项目结构：
```
my_game/
├── TextAdventure.py
├── consts.py
├── standalone_script_creator.py
└── story/
    ├── main.py
    └── assets/
```

打包命令：
```bash
cd my_game
python standalone_script_creator.py story/main.py --out_path dist/冒险游戏.py
```

分发时只需发送 `dist/冒险游戏.py`，接收方直接运行：
```bash
python 冒险游戏.py
```

无需安装任何依赖，无需原始引擎文件。
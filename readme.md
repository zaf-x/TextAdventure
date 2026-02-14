# TextAdventure

## For english version, see [readme-en.md](readme-en.md)

基于 Python 的文本冒险游戏引擎。不用关心输入输出等复杂逻辑，通过节点和选项即可构建多分支剧情、角色属性系统、条件判断和多重结局。

## 功能特性

- **可视化剧情结构** - 使用 Node（节点）和 Option（选项）组织剧情，天然支持多分支
- **数据驱动系统** - 内置变量系统，支持角色属性、物品、好感度等任意数值
- **条件控制** - 选项可根据条件显示/禁用，支持复杂逻辑（如"需要钥匙且等级≥5"）
- **角色创建** - 内置输入验证系统，支持游戏开始时的角色定制
- **存档分享** - 游戏可导出为单文件，方便分享给朋友或保存进度
- **安全执行** - 游戏逻辑在受限环境中运行，无需担心代码注入

## 一分钟上手

我们为您准备了几个个完整的示例游戏，您可以直接运行它们来体验游戏引擎的功能：

- [旅馆侦探](hotel_detective.py)
- [深空觉醒](deep_awaken.py)


## 完整文档

**[查看详细制作指南 →](story_doc.md)**

包含：
- 完整的 API 参考
- 变量访问规则（重要）
- 条件表达式写法
- 节点数据执行顺序
- 常见陷阱与解决方案
- 完整示例代码

## 安装

```bash
git clone https://github.com/baosh/TextAdventure.git
# 您可以直接运行示例游戏
cd TextAdventure
python hotel_detective.py
python deep_awaken.py
```

Python 版本要求：3.8+

## 快速制作游戏

1. 创建 `my_game.py`
2. 导入 `TextAdventure` 模块
3. 定义节点和选项（参考上方示例或详细文档）
4. 运行 `python my_game.py`

**分享游戏**：
```python
# 制作完成后导出
game.dump("my_game.pkl")

# 玩家加载运行
game = Game.load("my_game.pkl")
game.play()
```

## 项目结构

```
TextAdventure/
├── TextAdventure.py    # 游戏引擎（无需修改）
├── consts.py           # 安全执行环境配置
├── story_doc.md        # 详细制作文档
└── game.py             # 完整功能演示
```

## License

MIT License - 可自由用于个人或商业项目。

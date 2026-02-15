SAFE_BUILTINS = {
    "__builtins__": {
    # 类型转换
    "int": int,
    "float": float,
    "str": str,
    "bool": bool,
    "list": list,
    "dict": dict,
    "tuple": tuple,
    "set": set,
    
    # 数学运算
    "abs": abs,
    "min": min,
    "max": max,
    "sum": sum,
    "round": round,
    "pow": pow,
    "divmod": divmod,
    
    # 字符串处理
    "len": len,
    "range": range,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "sorted": sorted,
    "reversed": reversed,
    
    # 逻辑判断
    "all": all,
    "any": any,

    # 其他常用函数
    "id": id,
    "hex": hex,
    "oct": oct,
    "bin": bin,
    "print": print,
    "input": input,
    
    # 数学模块（可选）
    "__import__": None,  # 需要限制，见下方
}}

SAFE_MODULES = [
    "math",
    "random",
    "datetime",
    "calendar",
    "json",
    "time",
    "numpy",
]


def import_safe(name, globals=None, locals=None, fromlist=(), level=0):
    '''安全导入模块，仅允许导入白名单中的模块'''
    if name in SAFE_MODULES:
        return __import__(name, globals, locals, fromlist, level)
    else:
        print(f"警告：尝试导入不安全模块，已终止剧本 {name}")
        exit(1)
    
SAFE_BUILTINS["__builtins__"]["__import__"] = import_safe

STANDALONE_SCRIPT_MOD = """
'''
WARNING: This script is created by standalone_script_creator.py.
Do not modify this file manually.
modifications may cause unexpected behavior.
'''

import base64
import os
import types
import sys

TextAdventure = types.ModuleType("TextAdventure")
sys.modules["TextAdventure"] = TextAdventure

{consts}

{lib_cont}

TextAdventure.Game = Game
TextAdventure.Node = Node
TextAdventure.Option = Option
TextAdventure.Data = Data
TextAdventure.IOHandler = IOHandler
TextAdventure.SAFE_BUILTINS = SAFE_BUILTINS

_GAME_DATA = {gamedata}

try:
    with open("tmp.game", "wb") as f:
        f.write(base64.b64decode(_GAME_DATA))

    game = Game.load("tmp.game")
    game.play()
except Exception as e:
    print(f"[ERROR] Failed to play game: {{e}}")
    print("Abort")
    exit(1)
finally:
    os.remove("tmp.game")
"""
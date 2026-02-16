
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

import json
import pickle
from typing import Any, Callable, TYPE_CHECKING

if TYPE_CHECKING or "SAFE_BUILTINS" not in globals():
    from .consts import SAFE_BUILTINS

class Node:
    def __init__(self, game: 'Game', node_id: str = "", name: str = "", 
                 desc: str = "", options: list['Option'] | None = None, 
                 set_data: dict | None = None,
                 init_data: dict | None = None, defaults: list[dict[str, Any]] | None = None,
                 end_desc: str = "", on_load: str = "", on_ready: str = "", on_move: str = ""):
        
        '''初始化节点
        Args:
            game: 游戏实例
            node_id: 节点ID
            name: 节点名称
            desc: 节点描述
            options: 选项列表
            init_data: 初始化数据
            defaults: 默认选项
            end_desc: 结局描述
            on_load: 加载时执行的脚本
            on_ready: 就绪时执行的脚本
            on_move: 移动时执行的脚本
        '''

        self.game = game
        self.shared_data: 'Data' = self.game.shared_data

        self.node_id = node_id
        self.name = name
        self.desc = desc
        self.set_data = set_data or {}
        self.options = options or []
        self.init_data = init_data or {}
        self.end_desc = end_desc
        self.defaults = defaults or []
        self.on_load = on_load
        self.on_ready = on_ready
        self.on_move = on_move
        
        self.game.add_node(self)
    
    # 选项操作
    def add_option(self, option: 'Option'):
        '''添加选项
        Args:
            option: 选项实例
        '''
        self.options.append(option)
    
    def get_option_by_id(self, option_id: str) -> 'Option | None':
        '''根据ID获取选项
        Args:
            option_id: 选项ID
        Returns:
            选项实例
        '''
        for option in self.options:
            if option.option_id == option_id:
                return option
        return None

    def del_option(self, option: 'Option'):
        '''删除选项
        Args:
            option: 选项实例
        '''
        self.options.remove(option)
    
    def del_option_by_id(self, option_id: str):
        '''删除选项
        Args:
            option_id: 选项ID
        '''
        self.options = [option for option in self.options if option.option_id != option_id]
    
    def del_option_by_name(self, option_name: str):
        '''删除选项
        Args:
            option_name: 选项名称
        '''
        self.options = [option for option in self.options if option.name != option_name]
    
    def del_option_by_map(self, omap: Callable):
        '''删除选项

        Args:
            omap: 选项映射函数，返回True则删除
        '''
        self.options = [option for option in self.options if not omap(option)]
    
    def add_set_data(self, var, expr: str):
        '''添加或设置数据
        Args:
            var: 变量名
            expr: 变量值表达式
        '''
        self.set_data[var] = expr
    
    def del_set_data(self, var):
        '''删除数据
        Args:
            var: 变量名
        '''
        del self.set_data[var]
    
    def add_init_data(self, var, expr: str):
        '''添加或设置初始化数据
        Args:
            var: 变量名
            expr: 变量值表达式
        '''
        self.init_data[var] = expr
    
    def del_init_data(self, var):
        '''删除初始化数据
        Args:
            var: 变量名
        '''
        del self.init_data[var]
    
    def add_default(self, condition: str, node_id: str):
        '''添加默认选项
        Args:
            condition: 条件表达式，返回True则跳转到默认选项
            node_id: 下一个节点ID
        '''
        self.defaults.append({'condition': condition, 'node_id': node_id})
    
    def apply_data_change(self):
        '''应用数据变更
        '''
        for var, value in self.init_data.items():
            if var not in self.shared_data.data:
                try:
                    self.shared_data.data[var] = eval(value, SAFE_BUILTINS, self.shared_data.run_env())
                except Exception as e:
                    print(f"\n[ERROR] 节点 '{self.node_id}' 的 init_data['{var}'] = '{value}' 执行失败: {e}")
                    print(f"当前可用变量: {list(self.shared_data.data.keys())}")
                    raise
        
        for var, value in self.set_data.items():
            try:
                self.shared_data.data[var] = eval(value, SAFE_BUILTINS, self.shared_data.run_env())
            except Exception as e:
                print(f"\n[ERROR] 节点 '{self.node_id}' 的 set_data['{var}'] = '{value}' 执行失败: {e}")
                print(f"当前可用变量: {list(self.shared_data.data.keys())}")
                raise
    
    def run_default(self):
        for default in self.defaults:
            try:
                if eval(default['condition'], SAFE_BUILTINS, self.shared_data.run_env()):
                    return default['node_id']
            except Exception as e:
                print(f"\n[ERROR] 节点 '{self.node_id}' 的 defaults condition '{default['condition']}' 执行失败: {e}")
                print(f"当前可用变量: {list(self.shared_data.data.keys())}")
                raise
        return None
    
    def load_onload(self, filename: str):
        '''加载时执行的脚本
        Args:
            filename: 脚本文件名
        '''
        with open(filename, 'r') as f:
            self.on_load = f.read()
    
    def load_onready(self, filename: str):
        '''加载就绪时执行的脚本
        Args:
            filename: 脚本文件名
        '''
        with open(filename, 'r') as f:
            self.on_ready = f.read()
    
    def load_onmove(self, filename: str):
        '''移动时执行的脚本
        Args:
            filename: 脚本文件名
        '''
        with open(filename, 'r') as f:
            self.on_move = f.read()
    
    def load(self):
        try:
            exec(self.on_load, self.shared_data.run_env(this=self, data=self.shared_data))
        except Exception as e:
            print(f"\n[ERROR] 节点 '{self.node_id}' 的 on_load 脚本执行失败: {e}")
            raise
        self.apply_data_change()
        try:
            exec(self.on_ready, self.shared_data.run_env(this=self, data=self.shared_data))
        except Exception as e:
            print(f"\n[ERROR] 节点 '{self.node_id}' 的 on_ready 脚本执行失败: {e}")
            raise
    
    def run_onmove(self):
        try:
            exec(self.on_move, self.shared_data.run_env(this=self, data=self.shared_data))
        except Exception as e:
            print(f"\n[ERROR] 节点 '{self.node_id}' 的 on_move 脚本执行失败: {e}")
            raise
    
    def available_options(self):
        '''获取可移动且可显示的选项
        Returns:
            可移动且可显示的选项列表
        '''
        return [option for option in self.options if option.can_move() and option.can_show()]

    def can_move_options(self):
        '''获取可移动的选项
        Returns:
            可移动的选项列表
        '''
        return [option for option in self.options if option.can_move()]

    def can_show_options(self):
        '''获取可显示的选项
        Returns:
            可显示的选项列表
        '''
        return [option for option in self.options if option.can_show()]
    
    def disabled_options(self):
        return [x for x in self.can_show_options() if not x.can_move()]
    
    def move(self, option_id: str):
        '''移动到下一个节点
        Args:
            option_id: 选项ID
        '''

        self.run_onmove()
        for option in self.options:
            if option.option_id == option_id:
                if option.can_move():
                    return option.move()
        return None
    
    def is_end(self):
        '''判断是否为结局节点
        Returns:
            是否为结局节点
        '''
        return bool(self.end_desc)

class Option:
    def __init__(self, game: 'Game', option_id: str = "", name: str = "", 
                 desc: str = "", move_condition: str = "True", 
                 show_condition: str = "True", next_node_id: str = "start",
                 cant_move_desc: str = ""):
        
        '''初始化选项
        Args:
            game: 游戏实例
            option_id: 选项ID
            name: 选项名称
            desc: 选项描述
            condition: 可移动的条件表达式，返回True则可移动
            show_condition: 显示条件表达式，返回True则显示选项
            next_node_id: 下一个节点ID
        '''

        self.game = game
        self.nodes = game.nodes
        self.shared_data: Data = game.shared_data
        self.cant_move_desc = cant_move_desc

        self.option_id = option_id
        self.name = name
        self.desc = desc
        self.move_condition = move_condition
        self.show_condition = show_condition
        self.next_node_id = next_node_id
    
    def can_move(self):
        '''判断是否可移动
        Returns:
            是否可移动
        '''
        try:
            return eval(self.move_condition, SAFE_BUILTINS, self.shared_data.run_env())
        except Exception as e:
            print(f"\n[ERROR] 选项 '{self.option_id}' (name: '{self.name}') 的 move_condition 执行失败")
            print(f"条件表达式: {self.move_condition}")
            print(f"当前可用变量: {list(self.shared_data.data.keys())}")
            print(f"错误类型: {type(e).__name__}: {e}")
            raise
    
    def can_show(self):
        '''判断是否可显示
        Returns:
            是否可显示
        '''
        try:
            return eval(self.show_condition, SAFE_BUILTINS, self.shared_data.run_env())
        except Exception as e:
            print(f"\n[ERROR] 选项 '{self.option_id}' (name: '{self.name}') 的 show_condition 执行失败")
            print(f"条件表达式: {self.show_condition}")
            print(f"当前可用变量: {list(self.shared_data.data.keys())}")
            print(f"错误类型: {type(e).__name__}: {e}")
            raise
    
    def move(self):
        '''移动到下一个节点
        Returns:
            下一个节点实例
        '''
        return self.nodes[self.next_node_id]

class Data:
    def __init__(self):
        self.data = {}
    
    def run_env(self, **kwargs):
        '''运行环境
        Args:
            kwargs: 环境变量
        '''
        return {**self.data, **kwargs, "Node": Node, "Option": Option, "Game": Game}
    
    def format_string(self, s: str, **kwargs):
        '''格式化字符串
        Args:
            s: 字符串
            kwargs: 格式化变量
        Returns:
            格式化后的字符串
        '''
        return s.format(**self.run_env(**kwargs))

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
    
    def get_attr(self, name):
        '''获取属性
        Args:
            name: 属性名
        Returns:
            属性值
        '''
        return self.data.get(name, None)

    def __getattribute__(self, name):
        if name == "data":
            return super().__getattribute__(name)
        # Safely check if data attribute exists before accessing it
        try:
            data_dict = super().__getattribute__("data")
            if isinstance(data_dict, dict) and name in data_dict:
                return data_dict[name]
        except AttributeError:
            pass
        return super().__getattribute__(name)
    
    def __contains__(self, key):
        return key in self.data
    
    def __setattr__(self, name, value):
        # Check if data attribute exists before trying to access it
        try:
            if hasattr(self, 'data') and isinstance(self.data, dict) and name in self.data:
                self.data[name] = value
            else:
                super().__setattr__(name, value)
        except AttributeError:
            super().__setattr__(name, value)

class IOHandler:
    def __init__(self, shared_data: 'Data'):
        self.shared_data = shared_data
    
    def show_end(self, node: 'Node'):
        '''显示结局节点
        Args:
            node: 节点实例
        '''
        print(f"{self.shared_data.format_string(node.desc)}")
        print(f"{self.shared_data.format_string(node.name)}\n\n{self.shared_data.format_string(node.end_desc)}")
    
    def show_node(self, node: 'Node'):
        '''显示节点
        Args:
            node: 节点实例
        '''
        print(f"{self.shared_data.format_string(node.name)}\n\n{self.shared_data.format_string(node.desc)}")
    
    def show_options(self, ava_op: list['Option'], dis_op: list['Option']):
        '''显示选项
        Args:
            ava_op: 可移动选项列表
            dis_op: 不可移动选项列表
        '''
        print("可移动选项：")
        for i, option in enumerate(ava_op):
            print(f"{i}: {self.shared_data.format_string(option.name)} ({self.shared_data.format_string(option.desc)})")

        if dis_op:
            print("\n不可移动选项：")
            for i, option in enumerate(dis_op):
                print(f"X {i}: {self.shared_data.format_string(option.name)} ({self.shared_data.format_string(option.desc)}) | {self.shared_data.format_string(option.cant_move_desc)}")

        choice = input("> ")

        while not choice.isdigit() or int(choice) < 0 or int(choice) >= len(ava_op):
            print("输入错误，请重新输入")
            choice = input("> ")
        
        return ava_op[int(choice)]
    
    def get_init_input_start(self):
        print("#" * 20, "角色创建", "#" * 20)
    
    def init_input_boundary(self):
        print()
    
    def get_init_input_end(self):
        print("#" * 20, "角色创建完成", "#" * 20)
    
    def get_init_input(self, prompt: str):
        '''获取初始化输入
        Args:
            prompt: 提示信息
        Returns:
            输入值
        '''
        return input(self.shared_data.format_string(prompt))
    
    def show_init_input_error(self, err_desc: str, user_input: str):
        '''显示初始化输入错误
        Args:
            err_desc: 错误描述
            user_input: 用户输入值
        '''
        print(f"输入错误：{self.shared_data.format_string(err_desc)}，请重新输入")
    
    def node_boundary(self):
        print("\n")
    
class Game:
    def __init__(self, start_node_id: str = "start", game_name: str = "TextAdventure", init_input: list[dict] | None = None, io_handler: 'IOHandler | None' = None):
        self.shared_data = Data()
        self.io_handler = io_handler if io_handler else IOHandler(self.shared_data)
        self.start_node_id = start_node_id
        self.game_name = game_name
        self.nodes: dict[str, 'Node'] = {}

        self.current_node: 'Node | None' = None

        self.init_input = init_input or []
    
    def add_node(self, node: 'Node'):
        '''添加节点
        Args:
            node: 节点实例
        '''
        self.nodes[node.node_id] = node
    
    def remove_node(self, node: 'Node'):
        '''移除节点
        Args:
            node: 节点实例
        '''
        del self.nodes[node.node_id]
    
    def remove_node_by_id(self, node_id: str):
        '''移除节点
        Args:
            node_id: 节点ID
        '''
        del self.nodes[node_id]
    
    def add_init_input(self, prompt: str, name: str, converter: str, condition: str, err_desc: str):
        '''添加初始化输入
        Args:
            prompt: 提示信息
            name: 变量名
            converter: 转换函数名
            condition: 条件表达式
            err_desc: 错误描述
        '''
        self.init_input.append({"prompt": prompt, "name": name, "converter": converter, "condition": condition, "err_desc": err_desc})
    
    def remove_init_input_by_name(self, name: str):
        '''移除初始化输入
        Args:
            name: 变量名
        '''
        for init_input in self.init_input:
            if init_input["name"] == name:
                self.init_input.remove(init_input)
                break
    
    def get_init_inputs(self):
        '''获取初始化输入
        '''
        for init_input in self.init_input:
            prompt = init_input["prompt"]
            name = init_input["name"]
            converter = init_input["converter"]
            callable_converter = eval(converter, SAFE_BUILTINS, self.shared_data.run_env())
            condition = init_input["condition"]
            err_desc = init_input["err_desc"]

            while True:
                user_input = self.io_handler.get_init_input(prompt)
                try:
                    val = callable_converter(user_input)
                except ValueError:
                    self.io_handler.show_init_input_error(err_desc, user_input)
                    continue
                
                if not eval(condition, SAFE_BUILTINS, {"val": val}):
                    self.io_handler.show_init_input_error(err_desc, user_input)
                    continue
                
                self.shared_data[name] = val
                break
    
    def play(self):
        self.io_handler.get_init_input_start()
        self.get_init_inputs()
        self.io_handler.get_init_input_end()

        self.current_node = self.nodes[self.start_node_id]

        while not self.current_node.is_end():
            self.current_node.load()
            self.io_handler.show_node(self.current_node)
            default = self.current_node.run_default()

            if default:
                self.current_node = self.nodes[default]
                continue

            ava_op = self.current_node.available_options()
            dis_op = self.current_node.disabled_options()

            option = self.io_handler.show_options(ava_op, dis_op)

            if option:
                self.current_node = self.nodes[option.next_node_id]
            else:
                print("选项不存在")
            
            self.io_handler.node_boundary()
        
        self.current_node.load()
        self.io_handler.show_end(self.current_node)
    
    def dump(self, file: str):
        '''导出数据
        '''
        with open(file, "wb") as f:
            pickle.dump(self, f)
    
    @classmethod
    def load(cls, file: str):
        '''导入数据
        '''
        with open(file, "rb") as f:
            game = pickle.load(f)
            return game

TextAdventure.Game = Game
TextAdventure.Node = Node
TextAdventure.Option = Option
TextAdventure.Data = Data
TextAdventure.IOHandler = IOHandler
TextAdventure.SAFE_BUILTINS = SAFE_BUILTINS

_GAME_DATA = b'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juayieeahOWXoem4o+WjsOOAgieUc2hNaCxoTl2UKH2UKGiZaikBAABoHGoqAQAAdX2UKGiZaEloHIwNaW5uZXJfc2FuY3R1bZR1ZWhQaCxoUWgsaFNoLHViajABAABoGCmBlH2UKGgbaANoBWgIaBxqMAEAAGgdjAzop4Llr5/nn7Ppl6iUaB+Mc+S9oOS7lOe7huinguWvn+efs+mXqOS4iueahOespuaWh++8jOWPkeeOsOS6humakOiXj+eahOaWh+Wtl++8mgoKIuWUr+acieaZuuiAhe+8jOaWueiDveW+l+ingeecn+ebuOOAgiIKCnttYXBfaGludH2UaCF9lGglXZRoNn2UjAhtYXBfaGludJSMAicnlHNoTWgsaE5dlH2UKGiZaDJoHGjBdWFoUGgsaFGM8gpwcmludCgn5L2g6K6w5LiL5LqG6Zeo5LiK55qE6ZOt5paH44CCJykKaWYgaGFzX21hcDoKICAgIGRhdGFbJ21hcF9oaW50J10gPSAn5L2g56qB54S25oOz6LW36LSt5Lmw55qE5Y+k6ICB5Zyw5Zu+77yM6IOM6Z2i5YaZ552A77yaIuetlOahiOaYry4uLuWcsOWbvuacrOi6q++8gSInCmVsc2U6CiAgICBkYXRhWydtYXBfaGludCddID0gJ+i/meS8vOS5juaYr+afkOenjeaPkOekuu+8jOS9huS9oOavq+aXoOWktOe7quOAgicKlGhTaCx1YmoqAQAAaBgpgZR9lChoG2gDaAVoCGgcaioBAABoHYwM56ym5paH5a+G5a6klGgfWCIBAADkvaDnlKjpkqXljJnmiZPlvIDkuobnn7Ppl6jjgILpl6jlkI7mmK/kuIDkuKrlnIblvaLmiL/pl7TvvIzlopnlo4HkuIrmvILmta7nnYDlj5HlhYnnmoTnrKbmlofjgIIKCuaIv+mXtOS4reWkruacieS4gOS4quefs+WPsO+8jOS4iumdouWIu+edgOiwnOmimO+8mgoKIuaIkeacieWfjuW4guS9huayoeacieaIv+Wxi++8jOacieWxseiEieS9huayoeacieagkeacqO+8jOacieawtOS9huayoeaciemxvO+8jOaciemBk+i3r+S9huayoeaciei9pui+huOAguaIkeaYr+S7gOS5iO+8nyIKCntwdXp6bGVfc3Rh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'

try:
    with open("tmp.game", "wb") as f:
        f.write(base64.b64decode(_GAME_DATA))

    game = Game.load("tmp.game")
    game.play()
except Exception as e:
    print(f"[ERROR] Failed to play game: {e}")
    print("Abort")
    exit(1)
finally:
    os.remove("tmp.game")

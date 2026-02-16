
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
        return {**self.data, **kwargs}
    
    def format_string(self, s: str, **kwargs):
        '''格式化字符串
        Args:
            s: 字符串
            kwargs: 格式化变量
        Returns:
            格式化后的字符串
        '''
        return s.format(**self.data, **kwargs)

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

_GAME_DATA = b'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nKjmraPmmK/mraPljYjvvIzlhYnmn7HnhaflsITlnKjmiL/pl7TkuK3lpK7nmoTnn7Plj7DkuIrjgIIKCuefs+WPsOS4iuaRhuaUvuedgOS4gOS4quawtOaZtuWktOmqqO+8jOS4jeaYr+aBkOaAluaVheS6i+mHjOmCo+enje+8jOiAjOaYr+eyvuWvhueahOWFieWtpuS7quWZqO+8jOWwhumYs+WFieaKmOWwhOaIkOS4g+W9qeWFieiwse+8jOaKleWwhOWcqOWbm+WRqOWimeWjgeS4iuOAgumCo+S6m+WFieiwseeFp+S6rueahOWjgeeUu+iusui/sOS6hum7hOmHkeWfjueahOecn+ebuO+8mgoK6L+Z5LiN5piv5LiA5bqn5Z+O5biC77yM6ICM5piv5LiA5Liq5paH5piO55qE55+l6K+G5bqT44CC5Y+k5Lq65bCG5LuW5Lus55qE5pm65oWn44CB5Y6G5Y+y44CB5aSp5paH5a2m5ZKM5Yy75a2m55+l6K+G57yW56CB5Zyo6buE6YeR5Yi25ZOB5Lit77yM5L2/55So5p+Q56eN6YeP5a2Q6K6w5b+G5oqA5pyv44CC6Kem56Kw6buE6YeR77yM5bCx6IO96I635Y+W55+l6K+G77yM5L2G5Luj5Lu35piv5oSP6K+G5Lya6KKr6YOo5YiG5aSN5Yi25Yiw6buE6YeR5Lit44CCCgrlopnlo4HkuIrmnInkuInkuKrpgJrpgZPvvJoKLSDlt6bkvqfvvJrpgJrlvoAi6buE6YeR5LmL5a6kIu+8jOWghua7oemHkeWZqOeahOWvhuWupAotIOWPs+S+p++8mumAmuW+gCLop4LmmJ/lj7Ai77yM6K6w6L295aSp5paH55+l6K+G55qE5oi/6Ze0Ci0g5Lit5aSu77ya6YCa5b6AIuelreelgOS6lSLvvIzmt7HkuI3op4HlupXnmoTnq5bkupXvvIzmja7or7TpgJrlvoDlnLDkuIvmsrMKCuawtOaZtuWktOmqqOeqgeeEtuWPkeWHuuWXoem4o++8jOS8vOS5juWcqOitpuWRiuS9oOS7gOS5iOOAgpRoIX2UaFdoMHNoI12UKGgmKYGUfZQoaBtoA2gVaBZoBWgIaCloKmgrjA9vcHRfZ29fdHJlYXN1cnmUaB2MEui/m+WFpem7hOmH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5Y2V55qE5aSp5paH5Y+w77yM6ICM5piv5LiA5Liq5L+h5oGv6Kej56CB5Lit5b+D44CCCgrlopnlo4HkuIrliLvmu6Hkuobnsr7noa7nmoTmmJ/lm77vvIzorrDlvZXkuobkuInljYPlubTliY3nmoTmmJ/nqbrjgILkuK3lpK7mmK/kuIDkuKrlpI3mnYLnmoTpvb/ova7oo4Xnva7vvIznlLHpnZLpk5zlkozpu4Tph5HliLbmiJDvvIzmmK/kuIDlj7Dlj6Tku6PorqHnrpfmnLrvvIznlKjkuo7pooTmtYvml6Xpo5/lkozooYzmmJ/ovajov7njgIIKCuS9oOWPkeeOsOS6hue+iuearue6uOWcsOWbvueahOWujOaVtOeJiOacrOKAlOKAlOWOn+adpeS9oOaJi+S4reeahOWPquaYr+S4ieWIhuS5i+S4gOOAguWujOaVtOeahOWcsOWbvuaYvuekuu+8jOelnuW6meS4jeaYr+e7iOeCue+8jOiAjOaYr+S4rei9rOermeOAguecn+ato+eahCLpu4Tph5Hln44i5piv55+l6K+G5pys6Lqr77yM5a2Y5YKo5Zyo5YWo55CD5Y2B5LqM5aSE57G75Ly855qE56We5bqZ5Lit77yM57uE5oiQ5LiA5Liq572R57uc44CCCgrmm7Tph43opoHnmoTmmK/vvIzkvaDmib7liLDkuoYi56a75byA55qE5pa55rOVIuOAguinguaYn+WPsOeahOijhee9ruWPr+S7peaJk+W8gOS4gOadoeenmOWvhumAmumBk++8jOebtOaOpemAmuW+gOWxseS4i++8jOmBv+W8gOaJgOacieWNsemZqeOAguS9huWQr+WKqOijhee9rumcgOimgei+k+WFpeato+ehrueahOaYn+WbvuWvhueggeOAggoK5aKZ5LiK5Yi7552A5o+Q56S677yaIuW9k+eMjuaIt+W6p+iFsOW4puS4ieaYn+S4jumHkeWtl+WhlOWvuem9kOaXtu+8jOecn+eQhuS5i+mXqOW8gOWQr+OAgiIKCuS9oOi/mOmcgOimgeaUtumbhui2s+Wkn+eahOe6v+e0ouaJjeiDveino+iwnO+8iOiHs+WwkemcgOimgTPngrnmmbrmhafmiJbmi6XmnInnrJTorrDmnKzvvInjgIKUaCF9lCho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6KOF572u77yM6L6T5YWl5LqG5q2j56Gu55qE5pif5Zu+5Z2Q5qCH44CC5aKZ5aOB56e75Yqo77yM6Zyy5Ye65LiA5Liq5a+G5a6k4oCU4oCU5LiN5piv6buE6YeR77yM6ICM5piv5Zu+5Lmm6aaG77yM55So5LiN54Gt55qE5p2Q5paZ5Yi25oiQ55qE5Lmm57GN77yM6K6w5b2V552A5LiA5YiH44CCCgrkvYbkvaDlj6/ku6XpgInmi6nvvJrluKbotbDov5nkupvnn6Xor4blm57liLDnjrDku6PkuJbnlYzvvIzmiJbogIXnlZnlnKjov5nph4zmiJDkuLrlrojmiqTogIXvvIznu7TmiqTov5nkuKrnn6Xor4blupPvvIznrYnlvoXkuIvkuIDkuKogd29ydGh5IOeahOS6uuOAggoK5L2g55yL552A5omL5Lit55qE55u45py677yI5aaC5p6c5L2g5pyJ55u45py677yJ5oiW56yU6K6w5pys77yM5oOz5Yiw5LqG546w5Luj5LiW55WM55qE5oiY5LqJ44CB5rGh5p+T44CB6LSq5amq44CC55+l6K+G5Lya6KKr5rul55So44CCCgrkvaDpgInmi6nkuobnlZnkuIvjgIIKCuS9oOWWneS4i+S6huelreWPsOS4iueahOiNieiNr+iMtu+8jOmCo+aYr+W7tumVv+eUn+WRveeahOenmOiNr+OAguS9oOWwhuaIkOS4uuaWsOeahOelnuW6meWuiOaKpOiAhe+8jOWDj+S8oOivtOS4reeahOe7v+iDoeWtkOmakOWjq+S4gOagt++8jOWcqOS4m+ael+S4reeUn+a0u+aVsOeZvuW5tO+8jOWBtuWwlOW4ruWKqei/t+i3r+eahOaXheS6uu+8jOWBtuWwlOmpsemAkOi0quWpqueahOebl+WuneiAheOAggoK5L2g6LWw5Ye65LqG56We5bqZ77yM56uZ5Zyo6YeR5a2X5aGU6aG256uv77yM55yL552A5peg6L655peg6ZmF55qE6Zuo5p6X44CC5LiA5Y+q6KeS6ZuV6aOe5p2l77yM5YGc5Zyo5L2g6Lqr5peB77yM5o6l5Y+X5LqG5L2g55qE5oqa5pG444CCCgrkvaDmib7liLDkuobmr5Tpu4Tph5Hmm7Tnj43otLXnmoTkuJzopb/vvJrnm67nmoTjgIKUaCF9lGpFAQAAjAonZ3VhcmRpYW4nlHNoI12UaEJ9lGhbWAsCAADjgJDlrojmiqTogIXnu5PlsYDjgJEKCuS9oOaIkOS4uuS6huS6mumprOmAiueahOS8oOivtOOAggoK5pyq5p2l55qE5o6i6Zmp6ICF5YG25bCU5Lya5oql5ZGK77yM5Zyo5Lib5p6X5rex5aSE6YGH5Yiw5LiA5L2N55+l5pmT5LiA5YiH55qE6ZW/6ICF77yM5LuWL+WlueS8muaPkOS+m+awtOOAgemjn+eJqeWSjOitpuWRiu+8jOeEtuWQjua2iOWkseWcqOe7v+iJsuS4reOAggoK5L2g5rS75LqG5Lik55m+5bm077yM5a6I5oqk552A5Lq657G75aSx6JC955qE55+l6K+G77yM55u05Yiw5LiL5LiA5LiqIHdvcnRoeSDnmoTnu6fmib/ogIXlh7rnjrDjgIIKCuW9k+S9oOacgOe7iOemu+S4luaXtu+8jOS9oOeahOi6q+S9k+WMluS4uumHkeiJsueahOWFie+8jOiejeWFpeS6huelnuW6meeahOWimeWjge+8jOaIkOS4uuS6huawuOaBkueahOS4gOmDqOWIhuOAggoK6L+Z5piv5pyA5aW955qE57uT5bGA77ya55+l6K+G5b6X5Yiw5LqG5L+d5oqk77yM5L2g5Lmf6I635b6X5LqG6LaF6LaK5Yeh5Lq655qE55Sf5ZG95oSP5LmJ44CClGhcXZRoXmgqaF9oKmhgaCp1YmoWAQAAaBgpgZR9lChoG2gDaAVoCGgcahYBAABoHYwS57uT5bGA77ya55Sf6L+Y6ICFlGgfWFcDAADkvaDmi5Lnu53kuobor7Hmg5HjgIIKCuayoeacieeisOm7hOmHke+8jOayoeaciei3s+WFpea3seS6le+8jOS9oOaJvuWIsOS6huenmOWvhumAmumBk++8jOWcqOacuuWFs+WQr+WKqOWQjumAg+emu+S6huelnuW6meOAggoK5b2T5L2g6LWw5Ye65bGx5rSe77yM5ZG85ZC45Yiw5aSW55WM5r2u5rm/5L2G5riF5paw55qE56m65rCU5pe277yM5aSq6Ziz5q2j5Zyo6JC95bGx77yM5Lib5p6X6KKr5p+T5oiQ6YeR6Imy4oCU4oCU5q+U5Lu75L2V6buE6YeR6YO9576O5Li955qE6aKc6Imy44CCCgrkvaDlm57liLDkuobmlofmmI7kuJbnlYzvvIzluKbnnYDnhafniYfvvIjlpoLmnpzkvaDmnInnm7jmnLrvvInlkoznrJTorrDvvIzku6Xlj4rkuIDkuKrlhbPkuo7lj6Tku6PmmbrmhafnmoTmlYXkuovjgILmsqHmnInkurrnm7jkv6HkvaDlhbPkuo4i5rS7552A55qE6buE6YeRIueahOaPj+i/sO+8jOiupOS4uumCo+aYr+S4m+ael+eDreeXheS6p+eUn+eahOW5u+inieOAggoK5L2G5L2g5LiN5Zyo5LmO44CCCgrkvaDlu7rnq4vkuobkuIDkuKrkv53miqTln7rph5HvvIzkubDkuIvkuobnpZ7lupnlkajlm7TnmoTlnJ/lnLDvvIzpmLvmraLkuobnm5flrp3ogIXnmoTli5jmjqLjgILkvaDlhpnpgZPvvJoi5pyJ5Lqb5a6d6JeP5LiN5bqU6K+l6KKr5omT5omw44CCIgoK5aSa5bm05ZCO77yM5L2g5oiQ5Li65LqG5LiA5ZCN5pmu6YCa55qE5pWZ5o6I5oiW5ZCR5a+877yM5YG25bCU5Zyo5rex5aSc55yL552A5Lqa6ams6YCK55qE5pa55ZCR77yM55+l6YGT6YKj6YeM5pyJ5LiA5Liq56eY5a+G77yM5Y+q5pyJ5L2g55+l6YGT55yf55u444CCCgrkvaDlpLHljrvkuobotKLlr4zvvIzkvYbkv53kvY/kuobngbXprYLjgIKUaCF9lGpFAQAAjAonc3Vydml2b3InlHNoI12UaEJ9lGhbWLYBAADjgJDnlJ/ov5jogIXnu5PlsYDjgJEKCuS9oOW4puedgOeUn+WRveWSjOeQhuaZuuWbnuWIsOS6huWutuOAggoK6Jm954S25a2m5pyv55WM5Ziy56yR5L2g55qEIuWlh+W5u+aVheS6iyLvvIzkvYbkvaDmi43mkYTnmoTmmJ/lm77lkozlu7rnrZHnhafniYfmiJDkuLrkuobph43opoHnmoTogIPlj6TotYTmlpnjgIIKCuacgOmHjeimgeeahOaYr++8jOS9oOmYu+atouS6hui0quWpquWvueelnuW6meeahOegtOWdj+OAguWcqOS9oOatu+WQju+8jOS9oOea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r+ibh+avku+8jOS5n+iuuOaYr+WdoOiQve+8jOS5n+iuuOaYr+mlpemlv++8jOS9oOWAkuWcqOS6huemu+elnuW6meWPquacieS4gOatpeS5i+mBpeeahOWcsOaWueOAguinhumHjuaooeeziu+8jOWRvOWQuOayiemHje+8jOS9oOaEn+inieWIsOeUn+WRveWcqOa1gemAneOAggoK5L2G5aWH5oCq55qE5piv77yM5L2g5LiN5oSf5Yiw5oGQ5oOn44CCCgrkuJvmnpfmsqHmnInmg6nnvZrkvaDvvIzlroPlj6rmmK/lnKjlgZrlroPkuIDnm7TlgZrnmoTkuovigJTigJTlvqrnjq/nlJ/lkb3jgILkvaDnmoTouqvkvZPlsIbmiJDkuLrmoJHmnKjnmoTlhbvliIbvvIzkvaDnmoTmlYXkuovlsIbmiJDkuLrkvKDor7TvvIzkvaDnmoTlhpLpmannsr7npZ7lsIbmv4DlirHlkI7mnaXnmoTmjqLpmanogIXjgIIKCuacgOWQjueci+WIsOeahOaZr+ixoeaYr+S4gOWPquiTneiJsiBNb3JwaG8g6J206J2277yM5YGc5Zyo5L2g6by75bCW77yM57+F6IaA5Y+N5bCE552A5aSp56m655qE6aKc6Imy44CCCgrnhLblkI7vvIzlroHpnZnjgIKUaCF9lChqRQEAAIwHJ2RlYXRoJ5RoRmhadWgjXZRoQn2UaFtYwAEAAOOAkOWbnuW9kuiHqueEtue7k+WxgOOAkQoK5L2g55qE6YGX5L2T5LuO5pyq6KKr5om+5Yiw44CCCgrkvYbkuInlubTlkI7vvIzkuIDkvY3lvZPlnLDlkJHlr7zlnKjkuJvmnpfkuK3lj5HnjrDkuobkuIDmo7XlvILluLjlt6jlpKfnmoTlj6TmoJHvvIzmoJHmoLnnvKDnu5XnnYDkuIDmnKzmub/pgI/nmoTnrJTorrDmnKzigJTigJTkvaDnmoTnrJTorrDjgIIKCuagkeWRqOWbtOW8gOa7oeS6hue9leingeeahOiKseacte+8jOWKqOeJqeS7rOiBmumbhuWcqOmCo+mHjO+8jOS7v+S9m+Wco+WcsOOAggoK5L2g55qE5YaS6Zmp57uT5p2f5LqG77yM5L2G5L2g55qE55Sf5ZG95Lul5Y+m5LiA56eN5b2i5byP5bu257ut44CC6L+Z5bCx5piv5Lqa6ams6YCK55qE5pa55byP77ya5q275Lqh5LiN5piv57uI54K577yM6ICM5piv6L2s5o2i44CCCgpSZXN0IGluIG5hdHVyZSwge3BsYXllcl9uYW1lfS6UaFxdlGheaCpoX2gqaGBoKnVidYwMY3VycmVudF9ub2RllE6MCmluaXRfaW5wdXSUXZQofZQojAZwcm9tcHSUjEfpgInmi6nkvaDnmoTouqvku70gWzFd6ICD5Y+k5a2m5a62IFsyXeaOoumZqeWQkeWvvCBbM13ph47lpJbmkYTlvbHluIg6IJRoHYwMcGxheWVyX2NsYXNzlIwJY29udmVydGVylIwDaW50lIwJY29uZGl0aW9ulIwQdmFsIGluIFsxLCAyLCAzXZSMCGVycl9kZXNjlIwS6K+36L6T5YWlMeOAgTLmiJYzlHV9lChqdwEAAIwO5L2g55qE5ZCN5a2XOiCUaB2MC3BsYXllcl9uYW1llGp6AQAAjANzdHKUanwBAACMEzIgPD0gbGVuKHZhbCkgPD0gMjCUan4BAACMGeWQjeWtl+mVv+W6pjItMjDkuKrlrZfnrKaUdWV1Yi4='

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

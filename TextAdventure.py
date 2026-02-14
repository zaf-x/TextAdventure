import json
import pickle
from consts import SAFE_BUILTINS

class Node:
    def __init__(self, game: 'Game', node_id: str = "", name: str = "", 
                 desc: str = "", options: list['Option'] | None = None, 
                 set_data: dict | None = None,
                 init_data: dict | None = None, defaults: list[dict[str, any]] | None = None,
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
    
    # 选项操作
    def add_option(self, option: 'Option'):
        '''添加选项
        Args:
            option: 选项实例
        '''
        self.options.append(option)
    
    def get_option_by_id(self, option_id: str) -> 'Option':
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
    
    def del_option_by_map(self, omap: callable):
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
                self.shared_data.data[var] = eval(value, SAFE_BUILTINS, self.shared_data.run_env())
        
        for var, value in self.set_data.items():
            self.shared_data.data[var] = eval(value, SAFE_BUILTINS, self.shared_data.run_env())
    
    def run_default(self):
        for default in self.defaults:
            if eval(default['condition'], SAFE_BUILTINS, self.shared_data.run_env()):
                return default['node_id']
        return None
    
    def load_onready(self, filename: str):
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
        exec(self.on_load, self.shared_data.run_env(this=self, data=self.shared_data))
        self.apply_data_change()
        exec(self.on_ready, self.shared_data.run_env(this=self, data=self.shared_data))
    
    def run_onmove(self):
        exec(self.on_move, self.shared_data.run_env(this=self, data=self.shared_data))
    
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
        return eval(self.move_condition, SAFE_BUILTINS, self.shared_data.run_env())

    def can_show(self):
        '''判断是否可显示
        Returns:
            是否可显示
        '''
        return eval(self.show_condition, SAFE_BUILTINS, self.shared_data.run_env())
    
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
    
class Game:
    def __init__(self, start_node_id: str = "start", game_name: str = "TextAdventure", init_input: list[dict] | None = None, io_handler: 'IOHandler' = None):
        self.shared_data = Data()
        self.io_handler = io_handler if io_handler else IOHandler(self.shared_data)
        self.start_node_id = start_node_id
        self.game_name = game_name
        self.nodes: dict[str, 'Node'] = {}

        self.current_node: 'Node' | None = None

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

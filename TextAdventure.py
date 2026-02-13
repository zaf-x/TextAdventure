import json
from consts import SAFE_BUILTINS

class Node:
    def __init__(self, game: 'TextAdventure', node_id: str, name: str, desc: str, end_desc: str = '', set_sd: dict = None, init_sd: dict = None, options: list['Option'] = None, force_move: list[dict] = [], on_load: str = '', on_ready: str = '', on_move: str = ''):
        self.game = game
        self.shared_data: SharedData = self.game.shared_data
        
        self.node_id = node_id
        self.name = name
        self.desc = desc
        self.end_desc = end_desc
        self.options = options or []
        self.on_load = on_load
        self.on_ready = on_ready
        self.on_move = on_move
        self.force_move = force_move

        self.set_sd = set_sd or {}
        self.init_sd = init_sd or {}
    
    def get_option_list(self):
        return [option.to_json_schema() for option in self.options]
    
    def get_force_move(self):
        for move in self.force_move:
            condition = move.get("condition", "True")
            if self.shared_data.expr(condition):
                return self.game.get_node(move["node_id"])
        return None

    def set_shared_data(self):
        for key, value in self.set_sd.items():
            self.shared_data.write(key, self.shared_data.expr(value))
    
    def init_shared_data(self):
        for key, value in self.init_sd.items():
            if key not in self.shared_data:
                self.shared_data.write(key, self.shared_data.expr(value))
    
    def options_can_show(self):
        return [option for option in self.options if option.can_show()]

    def options_can_move(self):
        return [option for option in self.options if option.can_move()]
    
    def options_available(self):
        return [option for option in self.options_can_show() if option.can_move()]
    
    def options_disable(self):
        return [option for option in self.options_can_show() if not option.can_move()]

    def prepare(self):
        self.game.shared_data.script(self.on_load)
        self.init_shared_data()
        self.set_shared_data()
        self.game.shared_data.script(self.on_ready)
    
    def to_json_schema(self):
        return {
            self.node_id: {
                "name": self.name,
                "desc": self.desc,
                "end_desc": self.end_desc,
                "set_sd": self.set_sd,
                "init_sd": self.init_sd,
                "options": self.get_option_list(),
                "on_load": self.on_load,
                "on_ready": self.on_ready,
                "on_move": self.on_move,
                "force_move": self.force_move,
            }
        }

    def __rshift__(self, option: 'Option'):
        return option.move()
    
    def __invert__(self):
        return self.end_desc
    
class SharedData:
    def __init__(self, data: dict = None):
        self.data = data or {}
    
    def write(self, key: str, value):
        self.data[key] = value
    
    def read(self, key: str):
        return self.data.get(key, None)
    
    def get(self, key: str, default=None):
        return self.data.get(key, default)

    def get_script_run_env(self, addition: dict = {}):
        return {
            "globals": {
                "__builtins__": SAFE_BUILTINS,
                "shared_data": self,
                **addition,
            }, 
            "locals": {},
        }

    def expr(self, expr: str, **addition):
        renv = self.get_script_run_env(addition)
        return eval(expr, renv["globals"], renv["locals"])

    def script(self, script: str, **addition):
        renv = self.get_script_run_env(addition)
        exec(script, renv["globals"], renv["locals"])
    
    def format_string(self, s: str, **addition):
        return s.format(**self.data, **addition)
    
    def __getitem__(self, key: str):
        return self.read(key)
    
    def __setitem__(self, key: str, value):
        self.write(key, value)
    
    def __contains__(self, key: str):
        return key in self.data

class Option:
    def __init__(self, game: 'TextAdventure', option_id: str, show_name: str, desc: str, next_node: 'Node', show_condition: str = 'True', move_condition: str = 'True', cant_move_desc: str = "（无法移动）"):
        self.game = game
        self.shared_data: SharedData = self.game.shared_data
        self.option_id = option_id
        self.show_name = show_name
        self.desc = desc
        self.next_node = next_node
        self.show_condition = show_condition
        self.move_condition = move_condition

        self.cant_move_desc = cant_move_desc
    
    def to_json_schema(self):
        return {
            self.option_id: {
                "show_name": self.show_name,
                "desc": self.desc,
                "next_node": self.next_node.node_id,
                "show_condition": self.show_condition,
                "move_condition": self.move_condition,
                "cant_move_desc": self.cant_move_desc,
            }
        }
    
    @classmethod
    def from_json_schema(cls, data: dict, game: 'TextAdventure'):
        option_id = list(data.keys())[0]
        option_data = data[option_id]

        return Option(
            game=game,
            option_id=option_id,
            show_name=option_data["show_name"],
            desc=option_data["desc"],
            next_node=game.nodes[option_data["next_node"]],
            show_condition=option_data["show_condition"],
            move_condition=option_data["move_condition"],
            cant_move_desc=option_data["cant_move_desc"],
        )
    
    def can_show(self):
        return self.shared_data.expr(self.show_condition)
    
    def can_move(self):
        return self.shared_data.expr(self.move_condition)
    
    def move(self):
        if self.can_move():
            return self.next_node
        else:
            return None
    
    def __bool__(self):
        return self.can_move()

class TextAdventure:
    def __init__(self, game_name: str, start_node_id: str, init_inputs: dict = None, nodes: dict[str, Node] = None, on_load: str = '', on_ready: str = '', on_move: str = ''):
        self.game_name = game_name
        self.nodes = nodes or {}
        self.init_inputs = init_inputs or {}
        self.start_node_id = start_node_id
        self.shared_data = SharedData()

        self.on_load = on_load
        self.on_ready = on_ready
        self.on_move = on_move

        self.current_node: Node = self.nodes[self.start_node_id]
    
    @classmethod
    def from_json_schema(cls, data: dict):
        game = cls.__new__(cls)
        game.shared_data = SharedData()
        game.nodes = {}
        
        # ========== 阶段 1：创建所有裸 Node ==========
        for node_id in data["nodes"].keys():
            game.nodes[node_id] = Node.__new__(Node)
        
        # ========== 阶段 2：初始化所有 Node（填充 options）==========
        for node_id, node_obj in game.nodes.items():
            node_data = data["nodes"][node_id]
            
            # 先收集 options 数据，但不创建 Option（需要所有 Node 就绪）
            options_data = node_data.get("options", [])
            
            # 初始化 Node（除了 options）
            node_obj.game = game
            node_obj.shared_data = game.shared_data
            node_obj.node_id = node_id
            node_obj.name = node_data["name"]
            node_obj.desc = node_data["desc"]
            node_obj.end_desc = node_data.get("end_desc", "")
            node_obj.set_sd = node_data.get("set_sd", {})
            node_obj.init_sd = node_data.get("init_sd", {})
            node_obj.force_move = node_data.get("force_move", [])
            node_obj.on_load = node_data.get("on_load", "")
            node_obj.on_ready = node_data.get("on_ready", "")
            node_obj.on_move = node_data.get("on_move", "")
            node_obj.options = []  # 先空着
        
        # ========== 阶段 3：创建所有 Option（现在所有 Node 都已就绪）==========
        for node_id, node_obj in game.nodes.items():
            node_data = data["nodes"][node_id]
            options_data = node_data.get("options", [])
            
            for opt_data in options_data:
                opt_id = list(opt_data.keys())[0]
                opt_info = opt_data[opt_id]
                
                option = Option(
                    game=game,
                    option_id=opt_id,
                    show_name=opt_info["show_name"],
                    desc=opt_info["desc"],
                    next_node=game.nodes[opt_info["next_node"]],
                    show_condition=opt_info.get("show_condition", "True"),
                    move_condition=opt_info.get("move_condition", "True"),
                    cant_move_desc=opt_info.get("cant_move_desc", "（无法移动）"),
                )
                node_obj.options.append(option)
        
        # ========== 阶段 4：初始化 Game ==========
        game.game_name = data["game_name"]
        game.start_node_id = data["start_node_id"]
        game.init_inputs = data.get("init_inputs", {})
        game.on_load = data.get("on_load", "")
        game.on_ready = data.get("on_ready", "")
        game.on_move = data.get("on_move", "")
        game.current_node = game.nodes[game.start_node_id]
        
        return game
    
    def get_init_inputs(self):
        for key, data in self.init_inputs.items():
            prompt = data.get("prompt", f"请输入 {key}：")

            converter = data.get("converter", 'str')
            condition = data.get("condition", 'True')
            condition_desc = data.get("condition_desc", f"输入值不符合要求 {condition}")

            while True:
                user_input = input(prompt)
                value = self.shared_data.expr(f'converter(user_input)', user_input=user_input, converter=self.shared_data.expr(converter))

                if self.shared_data.expr(condition, value=value):
                    break
                else:
                    print(condition_desc.format(condition=condition))
            
            self.shared_data.write(key, value)
    
    def get_node(self, node_id: str):
        return self.nodes.get(node_id, None)
    
    def prepare(self):
        self.shared_data.script(self.on_load)
        self.get_init_inputs()
        self.shared_data.script(self.on_ready)
    
    def play(self):
        self.prepare()
        while not ~self.current_node:
            self.current_node.prepare()
            print(self.current_node.desc)

            force_move = self.current_node.get_force_move()

            if force_move:
                self.current_node = force_move
                self.shared_data.script(self.on_move)
                continue

            available_options = self.current_node.options_available()
            disabled_options = self.current_node.options_disable()

            for i, option in enumerate(available_options):
                print(f"{i+1} -> {self.shared_data.format_string(option.show_name)} ({self.shared_data.format_string(option.desc)})")
            
            for i, option in enumerate(disabled_options):
                print(f"X -> {self.shared_data.format_string(option.show_name)} ({self.shared_data.format_string(option.desc)}) | {self.shared_data.format_string(option.cant_move_desc)}")
            
            while True:
                next_move_input = input(">>> ")
                if not next_move_input.isdigit():
                    print("请输入数字")
                    continue

                next_move_index = int(next_move_input) - 1
                if next_move_index < 0 or next_move_index >= len(available_options):
                    print("请输入正确的数字")
                    continue

                break

            next_move_option = available_options[next_move_index]
            self.current_node = self.current_node >> next_move_option
            self.shared_data.script(self.on_move)
            
            print('\n')
        
        end = ~self.current_node
        print(self.shared_data.format_string(end))

if __name__ == "__main__":
    with open("game.json", "r") as f:
        data = json.load(f)
        game = TextAdventure.from_json_schema(data)
        game.play()

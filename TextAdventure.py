import json
import readline
import copy
import os
from datetime import datetime
import pickle

from consts import MESSAGE_IDS, SAFE_BUILTINS

class Node:
    def __init__(self, data: dict, nodes: dict, shared_data: dict, node_id: str, text_adv: 'TextAdventure'):
        self.data = data
        self.nodes = nodes
        self.node_id = node_id
        self.text_adv = text_adv

        self.name = data.get('name', '')
        self.description = data.get('description', '')

        self.options = data.get('options', {})
        self.force_select = data.get('force_select', [])

        self.set_d = data.get('set_d', {})
        self.init_d = data.get('init_d', {})

        self.end = data.get('end', False)
        self.end_description = data.get('end_description', '')

        self.python_script = data.get('python_script', '')
        self.onmove_script = data.get('onmove_script', '')

        self.shared_data = shared_data
    
    def full_init(self):
        self.update_shared_datas()
        self.run_script()

    def get_formula_result(self, formula: str):
        return self.text_adv.get_formula_result(formula)
    
    def can_show(self, option_dat: dict):
        '''Check if the option can be shown.'''
        show_condition = option_dat.get("show_condition", "True")
        return self.get_formula_result(show_condition)
    
    def can_move(self, option_dat: dict):
        '''Check if the option can be moved.'''
        move_condition = option_dat.get("move_condition", "True")
        return self.get_formula_result(move_condition)
    
    def options_can_show(self):
        '''Check if the options can be shown.'''
        options_can_show = {}

        for option_name, option_dat in self.options.items():
            if self.can_show(option_dat):
                options_can_show[option_name] = copy.deepcopy(option_dat)

        return copy.deepcopy(options_can_show)
    
    def options_can_move(self):
        '''Check if the options can be moved.'''
        options_can_move = {}

        for option_name, option_dat in self.options.items():
            if self.can_move(option_dat):
                options_can_move[option_name] = copy.deepcopy(option_dat)

        return copy.deepcopy(options_can_move)
    
    
    def show_no_move_options(self):
        '''Show the options that can be shown but cannot be moved.'''
        can_move = self.options_can_move()
        no_move = {}

        for option_name, option_dat in self.options.items():
            if option_name not in can_move.keys() and self.can_show(option_dat):
                no_move[option_name] = copy.deepcopy(option_dat)

        return copy.deepcopy(no_move)
    
    def show_and_move_options(self):
        '''Show the options that can be shown and moved.'''
        can_move = self.options_can_move()
        options_can_show = self.options_can_show()
        
        return {
            name: copy.deepcopy(dat) 
            for name, dat in can_move.items() 
            if name in options_can_show
        }

    def update_shared_datas(self):
        '''Update the shared datas of the current node.'''
        for key in self.set_d.keys():
            self.shared_data[key] = self.get_formula_result(self.set_d[key])

        for key in self.init_d.keys():
            if key not in self.shared_data.keys():
                self.shared_data[key] = self.get_formula_result(self.init_d[key])

    def force_move(self):
        '''Force move to the next node.'''
        if not self.force_select:
            return None

        for force in self.force_select:
            condition = force.get('condition', 'True')
            if self.get_formula_result(condition):
                data = self.nodes[force["next_node"]]
                return Node(data, self.nodes, self.shared_data, force["next_node"], self.text_adv)
        else:
            return None
    def run_script(self, script: str = None):
        '''Run the python script of the current node.'''
        if script is not None:
            try:
                self.text_adv.run_script(script)
            except Exception as e:
                self.text_adv.log_handler.log("ERR_SCRIPT_ERROR", e=f"{e.__class__.__name__}: {e}; on line {e.__traceback__.tb_lineno} in {e.__traceback__.tb_frame.f_code.co_name}", script_desc=self.python_script.splitlines()[e.__traceback__.tb_lineno-1])
        else:
            self.run_script(self.python_script)

    def move(self, option: str):
        '''Move to the next node.'''
        if option in self.options.keys():
            self.run_script(self.onmove_script)
            next_node_name = self.options[option].get('next_node', '')

            if next_node_name in self.nodes.keys():
                new_data = copy.deepcopy(self.nodes[next_node_name])
                new_node = Node(new_data, self.nodes, self.shared_data, next_node_name, self.text_adv)
            return new_node
        else:
            return None
    
    # 在 Node 类中添加方法
    def render_description(self, text):
        '''渲染描述文本，支持变量和简单表达式'''
        try:
            # 先尝试普通format
            return text.format(**self.shared_data)
        except KeyError as e:
            # 如果失败，尝试用eval计算表达式
            import re
            pattern = r'\{([^}]+)\}'
            def replace_expr(match):
                expr = match.group(1)
                try:
                    # 尝试作为表达式计算
                    result = eval(expr, {"__builtins__": SAFE_BUILTINS}, self.shared_data)
                    return str(result)
                except:
                    # 计算失败，保持原样
                    return match.group(0)
            return re.sub(pattern, replace_expr, text)

class LogHandler:
    def log(self, message_id: str, end: str = '\n', **kwargs):
        '''Log the message.'''
        print(MESSAGE_IDS[message_id].format(**kwargs), end=end)
    
    def input(self, message_id: str, **kwargs):
        '''Log the message and return the input.'''
        return input(MESSAGE_IDS[message_id].format(**kwargs))

DEFAULT_LOG_HANDLER = LogHandler()

class TextAdventure:
    def __init__(self, story_data: dict, log_handler: LogHandler = DEFAULT_LOG_HANDLER):
        self.name = story_data.get('name', '')
        self.start_node_name = story_data.get('start_node', '')
        self.nodes = story_data.get('nodes', {})
        self.init_inputs = story_data.get('init_inputs', {})

        self.shared_data = story_data.get('shared_data', {})
        self.onready_script = story_data.get('onready_script', '')

        self.script_run_globals = {
            "__builtins__": SAFE_BUILTINS,            
            "write_data": self.write_data, 
            "read_data": self.read_data, 
            "exist_data": self.exist_data
            }

        self.current_node = Node(self.nodes[self.start_node_name], self.nodes, self.shared_data, self.start_node_name, self)
        self.log_handler = log_handler
        
    def write_data(self, key: str, value):
        '''Write the data to the shared data.'''
        self.shared_data[key] = value
    
    def read_data(self, key: str):
        '''Read the data from the shared data.'''
        return self.shared_data[key]
    
    def exist_data(self, key: str):
        '''Check if the data exists in the shared data.'''
        return key in self.shared_data.keys()

    def dump(self, filename: str):
        '''Dump the current node.'''
        with open(filename, "wb") as f:
            pickle.dump(self.current_node, f)

        self.log_handler.log("DUMP_CURRENT_NODE", filename=filename)
    
    def get_formula_result(self, formula: str, **additions):
        '''Get the result of the formula.'''
        return eval(formula, self.script_run_globals, {**self.shared_data, **additions})
    
    def run_script(self, script: str):
        '''Run the python script.'''
        try:
            exec(script, self.script_run_globals)
            return True
        except Exception as e:
            lineno = e.__traceback__.tb_lineno
            self.log_handler.log("ERR_SCRIPT_ERROR", e=f"{e.__class__.__name__}: {e}; on line {lineno} in {e.__traceback__.tb_frame.f_code.co_name}", script_desc=script.splitlines()[lineno-1])
            return False
        
    @classmethod
    def from_json(cls, filename: str, log_handler: LogHandler = DEFAULT_LOG_HANDLER):
        '''Load the current node.'''
        with open(filename, "r") as f:
            data = json.load(f)

        return cls(data, log_handler)
    
    @classmethod
    def load(cls, filename: str, log_handler: LogHandler = DEFAULT_LOG_HANDLER):
        '''Load the current node.'''
        with open(filename, "rb") as f:
            current_node = pickle.load(f)

        return cls(current_node, log_handler)
    
    def get_one_init_input(self, init_input_dat: dict):
        '''Get the input for one init data.'''
        desc = init_input_dat.get('desc', '')
        converter = init_input_dat.get('converter', 'str')
        condition = init_input_dat.get('condition', 'True')
        condition_desc = init_input_dat.get('condition_desc', '')

        value = self.log_handler.input("INPUT", prompt=desc)
        final_val = self.get_formula_result(f"{converter}({repr(value)})", value=value)

        while not self.get_formula_result(condition, val = final_val):
            self.log_handler.log("ERR_INVALID_INPUT", condition_desc=condition_desc)
            value = self.log_handler.input("INPUT", prompt=desc)
            final_val = self.get_formula_result(f"{converter}({repr(value)})", value=value)
        
        return final_val
    
    def get_init_inputs(self):
        '''Get the init inputs.'''
        self.log_handler.log("INPUT_INIT_BEGIN")
        for init_input_name, init_input_dat in self.init_inputs.items():
            self.shared_data[init_input_name] = self.get_one_init_input(init_input_dat)
            self.log_handler.log("INPUT_INIT_BOUNDARY")

        self.log_handler.log("INPUT_INIT_END")
    
    def prepare(self):
        '''Prepare the game.'''
        self.get_init_inputs()
        success = self.run_script(self.onready_script)
        if not success:
            exit(1)
    
    def play(self):
        '''Play the game.'''
        while True:
            self.current_node.full_init()

            end = self.current_node.end
            name = self.current_node.name
            desc = self.current_node.render_description(self.current_node.description)
            self.log_handler.log("SHOW_NODE", name=name, desc=desc)
            if end:
                break
        
            options_show_move = self.current_node.show_and_move_options()
            options_no_move = self.current_node.show_no_move_options()
            force_move = self.current_node.force_move()

            if force_move:
                self.current_node = force_move
                continue
            
            i = 0
            for option_name, option_dat in options_show_move.items():
                option_desc = option_dat.get('desc', '')

                rendered_option_name = self.current_node.render_description(option_name)
                rendered_option_desc = self.current_node.render_description(option_desc)

                self.log_handler.log("SHOW_OPTION", i=i, option_name=rendered_option_name, option_desc=rendered_option_desc)
                i += 1
            
            for option_name, option_dat in options_no_move.items():
                option_desc = option_dat.get('desc', '')
                cant_move_desc = option_dat.get('cant_move_desc', '')

                rendered_option_name = self.current_node.render_description(option_name)
                rendered_option_desc = self.current_node.render_description(option_desc)
                rendered_cant_move_desc = self.current_node.render_description(cant_move_desc)

                self.log_handler.log("SHOW_NO_MOVE_OPTION", option_name=rendered_option_name, option_desc=rendered_option_desc, cant_move_desc=rendered_cant_move_desc)
        
            player_move = self.log_handler.input("NEXT_MOVE_INPUT")
            if not player_move.isdigit():
                self.log_handler.log("ERR_INVALID_INPUT", condition_desc="请输入数字")
                continue

            player_move = int(player_move)
            if player_move < 0 or player_move >= i:
                self.log_handler.log("ERR_INVALID_INPUT", condition_desc="请输入正确的数字")
                continue

            move_option_name = list(options_show_move.keys())[player_move]
            self.current_node = self.current_node.move(move_option_name)

            self.log_handler.log("NODE_BOUNDARY")

        self.log_handler.log("END_DESC", end_desc=self.current_node.render_description(self.current_node.end_description))

if __name__ == "__main__":
    files = os.listdir("stories")
    games = {}
    for file in files:
        if file.endswith(".json"):
            with open(f"stories/{file}", "r") as f:
                data = json.load(f)
                game_name = data.get("name", file[:-5])
                games[game_name] = f"stories/{file}"
    
    print("------ 游戏列表 ------")
    for i, game_name in enumerate(games.keys()):
        print(f"{i}. {game_name}")
    print("----------------------")

    game_index = int(input("请选择游戏序号: "))
    if game_index < 0 or game_index >= len(games):
        print("无效的游戏序号")
        exit(1)
    
    game_file = games[list(games.keys())[game_index]]
    game = TextAdventure.from_json(game_file)
    game.prepare()
    game.play()
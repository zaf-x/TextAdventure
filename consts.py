SAFE_BUILTINS = {
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
}

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
    
SAFE_BUILTINS["__import__"] = import_safe

MESSAGE_IDS = {
    "ERR_INVALID_INPUT": "[错误: 输入值不符合要求 {condition_desc}]",
    "ERR_SCRIPT_ERROR": "[错误: 执行剧本脚本时出错 {e} {script_desc}]",
    "ERR_INVALID_NODE": "[错误: 节点 {node_id} 不存在]",
    "ERR_INVALID_CONDITION": "[错误: 条件表达式 {condition} 无效]",
    "ERR_NAME": "[错误: 变量名 {name} 无效或不存在]",
    "ERR_INVALID_IMPORT": "[错误: 导入模块 {module_name} 无效]",
    "DUMP_CURRENT_NODE": "[信息: 当前节点已转储到 {filename}]",
    "INPUT": "{prompt}",
    "INPUT_INIT_BEGIN": "[信息: 初始化输入开始]",
    "INPUT_INIT_BOUNDARY": "\n",
    "INPUT_INIT_END": "[信息: 初始化输入结束]",
    "SHOW_OPTION": "{i}. {option_name} ({option_desc})",
    "SHOW_NO_MOVE_OPTION": "X {option_name} ({option_desc}) | {cant_move_desc}",
    "NEXT_MOVE_INPUT": "请选择 > ",
    "SHOW_NODE": "【{name}】\n\n{desc}",
    "END_DESC": "结局：\n {end_desc}",
    "NODE_BOUNDARY": "\n\n"
}
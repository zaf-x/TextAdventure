from TextAdventure import Game, Node, Option

# 创建游戏实例
game = Game(
    start_node_id="start",
    game_name="完整功能测试游戏",
    init_input=[
        {"prompt": "请输入角色姓名：", "name": "player_name", "converter": "str", "condition": "len(val) > 0", "err_desc": "姓名不能为空"},
        {"prompt": "请输入年龄(1-150)：", "name": "age", "converter": "int", "condition": "1 <= val <= 150", "err_desc": "年龄必须在1-150之间"},
        {"prompt": "选择职业(1-战士 2-法师 3-盗贼)：", "name": "job", "converter": "int", "condition": "val in [1, 2, 3]", "err_desc": "请输入1、2或3"}
    ]
)

# ========== 节点1：开始节点 ==========
start = Node(
    game=game,
    node_id="start",
    name="冒险者公会",
    desc="""欢迎，{player_name}！
你是一名{job_name}，等级{level}。
生命值: {hp}/{max_hp} | 魔法值: {mp}/{max_mp} | 金币: {gold}

你站在冒险者公会的大厅里，前方有两扇门。""",
    init_data={
        "level": "1",
        "max_hp": "100",
        "max_mp": "100",
        "has_key": "False",
        "monster_defeated": "False"
    },
    set_data={
        "gold": "50"
    },
    on_load="""
# 根据职业设置属性
jobs = {1: "战士", 2: "法师", 3: "盗贼"}
hp_map = {1: 100, 2: 60, 3: 80}
mp_map = {1: 20, 2: 100, 3: 40}

# 安全获取 job（确保是整数）
try:
    job_id = int(job)
    if job_id not in jobs:
        job_id = 1
except:
    job_id = 1

# 直接赋值给共享数据（通过 data 对象）
data['job'] = job_id
data['job_name'] = jobs[job_id]
data['hp'] = hp_map[job_id]
data['mp'] = mp_map[job_id]
""",
    on_ready="""
# HP/MP上限检查
if hp > max_hp:
    data['hp'] = max_hp
if mp > max_mp:
    data['mp'] = max_mp
print(f'[系统] {player_name}（{job_name}）进入了游戏')
"""
)

# 左门选项（通往战斗）
left_op = Option(
    game=game,
    option_id="left_door",
    name="进入左门（战斗挑战）",
    desc="门后传来野兽的咆哮声",
    next_node_id="battle_room"
)

# 右门选项（通往解谜）
right_op = Option(
    game=game,
    option_id="right_door",
    name="进入右门（解谜挑战）",
    desc="门后一片寂静，似乎有宝藏的气息",
    next_node_id="puzzle_room"
)

# 商店选项（需要等级>=2或金币>=100）- 使用直接变量名
shop_op = Option(
    game=game,
    option_id="shop",
    name="前往商店",
    desc="购买装备和药水",
    move_condition="level >= 2 or gold >= 100",
    show_condition="True",
    next_node_id="shop",
    cant_move_desc="需要等级≥2或金币≥100才能进入高级商店"
)

# 结局选项（需要击败怪物且有钥匙）- 使用直接变量名
end_op = Option(
    game=game,
    option_id="go_end",
    name="前往最终之门",
    desc="结束冒险",
    move_condition="monster_defeated and has_key",
    show_condition="True",
    next_node_id="good_end",
    cant_move_desc="需要击败怪物并获得钥匙"
)

start.add_option(left_op)
start.add_option(right_op)
start.add_option(shop_op)
start.add_option(end_op)

# ========== 节点2：战斗房间 ==========
battle = Node(
    game=game,
    node_id="battle_room",
    name="战斗房间",
    desc="""一只凶猛的史莱姆王出现在你面前！
你的状态：HP {hp}/{max_hp} | MP {mp}/{max_mp}

史莱姆王咆哮着冲向你！""",
    on_load="""
if not in_battle:
    data['enemy_hp'] = 50
    data['in_battle'] = True
    print("[战斗开始] 史莱姆王 HP:", enemy_hp)
"""
)

# 攻击选项 - 使用直接变量名
attack_op = Option(
    game=game,
    option_id="attack",
    name="攻击",
    desc="造成10-20点伤害，消耗5MP",
    move_condition="mp >= 5",
    next_node_id="battle_room",
    cant_move_desc="魔法值不足"
)

# 强力攻击（战士专属）- 使用直接变量名
power_attack_op = Option(
    game=game,
    option_id="power_attack",
    name="强力斩击",
    desc="造成25-35点伤害，消耗15MP",
    move_condition="job == 1 and mp >= 15",
    show_condition="job == 1",
    next_node_id="battle_room"
)

# 火球术（法师专属）- 使用直接变量名
fireball_op = Option(
    game=game,
    option_id="fireball",
    name="火球术",
    desc="造成30-40点伤害，消耗20MP",
    move_condition="mp >= 20",
    show_condition="job == 2",
    next_node_id="battle_room"
)

# 逃跑选项
flee_op = Option(
    game=game,
    option_id="flee",
    name="逃跑",
    desc="返回公会（战斗重置）",
    next_node_id="start"
)

battle.add_option(attack_op)
battle.add_option(power_attack_op)
battle.add_option(fireball_op)
battle.add_option(flee_op)

# 战斗胜利节点 - set_data 使用直接变量名
battle_win = Node(
    game=game,
    node_id="battle_win",
    name="战斗胜利！",
    desc="你击败了史莱姆王！获得50金币和经验值！",
    set_data={
        "gold": "gold + 50",
        "level": "level + 1",
        "monster_defeated": "True",
        "in_battle": "False"
    },
    defaults=[
        {"condition": "True", "node_id": "start"}
    ]
)

# ========== 节点3：解谜房间 ==========
# ========== 节点3：解谜房间 ==========
puzzle = Node(
    game=game,
    node_id="puzzle_room",
    name="谜题房间",
    desc="""你进入一个充满古代符文的房间。
墙上刻着："只有智者才能获得宝藏。
2 + 2 × 2 = ?"

地上有三个石板，分别写着：8、6、4""",
    init_data={
        "puzzle_solved": "False"
    }
)

# 答案选项（正确答案是6）
answer_8 = Option(
    game=game,
    option_id="ans_8",
    name="选择 8",
    desc="点击写着8的石板",
    next_node_id="puzzle_wrong"
)

answer_6 = Option(
    game=game,
    option_id="ans_6",
    name="选择 6",
    desc="点击写着6的石板（根据运算法则，先乘除后加减：2×2=4，2+4=6）",
    next_node_id="puzzle_correct"
)

answer_4 = Option(
    game=game,
    option_id="ans_4",
    name="选择 4",
    desc="点击写着4的石板",
    next_node_id="puzzle_wrong"
)

puzzle.add_option(answer_8)
puzzle.add_option(answer_6)
puzzle.add_option(answer_4)

# 答错节点 - set_data 使用直接变量名
puzzle_wrong = Node(
    game=game,
    node_id="puzzle_wrong",
    name="回答错误",
    desc="石板发出红光，你感到一阵眩晕，失去了10点HP...",
    set_data={
        "hp": "max(1, hp - 10)"
    },
    defaults=[
        {"condition": "True", "node_id": "puzzle_room"}
    ]
)

# 答对节点 - set_data 使用直接变量名
puzzle_correct = Node(
    game=game,
    node_id="puzzle_correct",
    name="回答正确！",
    desc="""石板发出金光，一个宝箱缓缓升起！
你获得了：神秘钥匙 + 30金币""",
    set_data={
        "has_key": "True",
        "gold": "gold + 30",
        "puzzle_solved": "True"
    },
    defaults=[
        {"condition": "True", "node_id": "start"}
    ]
)

# ========== 节点4：商店 ==========
shop = Node(
    game=game,
    node_id="shop",
    name="神秘商店",
    desc="""商人："欢迎光临！想要点什么？"
你的金币：{gold}

1. 生命药水（恢复30HP）- 20金币
2. 魔法药水（恢复30MP）- 20金币  
3. 升级护符（等级+1）- 100金币
4. 离开商店""",
    on_ready="print('[商店] 欢迎光临！')"
)

# 购买生命药水 - 使用直接变量名
buy_hp = Option(
    game=game,
    option_id="buy_hp",
    name="购买生命药水",
    desc="花费20金币恢复30HP",
    move_condition="gold >= 20",
    next_node_id="shop",
    cant_move_desc="金币不足"
)

# 购买魔法药水 - 使用直接变量名
buy_mp = Option(
    game=game,
    option_id="buy_mp",
    name="购买魔法药水",
    desc="花费20金币恢复30MP",
    move_condition="gold >= 20",
    next_node_id="shop",
    cant_move_desc="金币不足"
)

# 购买升级护符 - 使用直接变量名
buy_level = Option(
    game=game,
    option_id="buy_level",
    name="购买升级护符",
    desc="花费100金币提升等级",
    move_condition="gold >= 100",
    next_node_id="shop",
    cant_move_desc="金币不足（需要100）"
)

# 离开商店
leave_shop = Option(
    game=game,
    option_id="leave_shop",
    name="离开商店",
    desc="返回公会",
    next_node_id="start"
)

shop.add_option(buy_hp)
shop.add_option(buy_mp)
shop.add_option(buy_level)
shop.add_option(leave_shop)

# ========== 节点5：结局 ==========
good_end = Node(
    game=game,
    node_id="good_end",
    name="完美结局：传奇冒险者",
    desc="""你使用钥匙打开了最终之门，里面是无尽的宝藏和荣耀！

【最终统计】
姓名：{player_name}
职业：{job_name}
等级：{level}
金币：{gold}

你成为了传说中的冒险者！""",
    end_desc="""感谢游玩完整功能测试游戏！
你体验了：角色创建、条件选项、战斗系统、解谜系统、商店系统、多结局"""
)

# 注册所有节点
game.add_node(start)
game.add_node(battle)
game.add_node(battle_win)
game.add_node(puzzle)
game.add_node(puzzle_wrong)
game.add_node(puzzle_correct)
game.add_node(shop)
game.add_node(good_end)

# 运行游戏
if __name__ == "__main__":
    game.play()
    game.dump("game.pkl")
    print("游戏已导出到 game.pkl")
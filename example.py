#!/usr/bin/env python3
from TextAdventure import Game, Node, Option

# ==================== 游戏初始化 ====================
game = Game(
    game_name="遗忘之城 - The Forgotten City",
    start_node_id="intro",
    init_input=[
        {
            "prompt": "请输入冒险者的名字: ",
            "name": "player_name",
            "converter": "str.strip",
            "condition": "2 <= len(val) <= 20",
            "err_desc": "名字长度需要在2-20个字符之间。"
        },
        {
            "prompt": "选择你的职业：\n1. 战士 (高生命/高防御)\n2. 法师 (高攻击/低生命)\n3. 盗贼 (高敏捷)\n请输入数字 (1-3): ",
            "name": "player_class",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "请输入 1、2 或 3。"
        }
    ]
)

# ==================== 数据初始化节点 ====================
intro = Node(
    game=game,
    node_id="intro",
    name="序章：启程",
    desc="""欢迎，{player_name}。

你是一位年轻的{player_class_name}，听闻北方山脉中出现了古老的遗迹——"遗忘之城"。
传说那里藏有能让人获得永恒力量的秘宝，但也充满了致命的危险。

你站在村庄的出口处，背包里装着仅有的补给。
阳光洒在你的脸上，微风带来远方的气息。

你的冒险，现在开始。""",
    init_data={
        "hp": "120 if player_class == 1 else (80 if player_class == 2 else 100)",
        "max_hp": "120 if player_class == 1 else (80 if player_class == 2 else 100)",
        "attack": "15 if player_class == 1 else (20 if player_class == 2 else 12)",
        "defense": "10 if player_class == 1 else (4 if player_class == 2 else 8)",
        "agility": "6 if player_class == 1 else (7 if player_class == 2 else 15)",
        "gold": "50",
        "potions": "3",
        "has_map": "False",
        "has_key": "False",
        "defeated_goblin": "False",
        "solved_riddle": "False",
        "turns": "0",
        "player_class_name": "'战士'"
    },
    set_data={"turns": "turns + 1"},
    on_ready="""
# 根据选择的数字设置职业名称
class_names = {1: '战士', 2: '法师', 3: '盗贼'}
data['player_class_name'] = class_names.get(player_class, '冒险者')
print(f'欢迎，{player_name} the {player_class_name}！')
"""
)

# ==================== 村庄节点 ====================
village = Node(
    game=game,
    node_id="village",
    name="青石村",
    desc="""你回到了青石村，这是一个宁静的小村庄。

村子里有简陋的商店和疲惫的守卫。村民们用好奇的眼神打量着你。

【状态】生命值: {hp}/{max_hp} | 金币: {gold} | 药水: {potions}瓶
【装备】攻击力: {attack} | 防御力: {defense} | 敏捷: {agility}

{player_name}，你要做什么？""",
    set_data={"turns": "turns + 1"},
    on_ready="""
# 恢复生命值（在村庄休息）
if hp < max_hp:
    data['hp'] = min(hp + 10, max_hp)
    print('在村庄休息，恢复了10点生命值。')
"""
)

shop = Node(
    game=game,
    node_id="shop",
    name="杂货店",
    desc="""你走进了村里的杂货店。店主是一位满脸皱纹的老人。

"年轻人，需要点什么？"店主问道。

货架上摆放着：
- 生命药水 (30金币) - 恢复30点生命
- 古老地图 (50金币) - 标记了通往遗忘之城的秘密通道

你目前拥有 {gold} 枚金币。""",
    set_data={"turns": "turns + 1"}
)

# 购买处理节点
buy_potion_process = Node(
    game=game,
    node_id="buy_potion_process",
    name="购买中...",
    desc="你付给店主30金币，拿到了一瓶生命药水。",
    set_data={"gold": "gold - 30", "potions": "potions + 1", "turns": "turns + 1"},
    defaults=[{"condition": "True", "node_id": "shop"}]
)

buy_map_process = Node(
    game=game,
    node_id="buy_map_process",
    name="购买中...",
    desc="你付给店主50金币，获得了一张泛黄的古老地图。地图上标记着通往遗忘之城的秘密路径。",
    set_data={"gold": "gold - 50", "has_map": "True", "turns": "turns + 1"},
    defaults=[{"condition": "True", "node_id": "shop"}]
)

rest_process = Node(
    game=game,
    node_id="rest_process",
    name="休息中...",
    desc="你在旅馆中度过了一晚。柔软的床铺让你彻底放松了身心。",
    set_data={"gold": "gold - 10", "hp": "max_hp", "turns": "turns + 1"},
    on_ready="""print('生命值已完全恢复！')""",
    defaults=[{"condition": "True", "node_id": "village"}]
)

# ==================== 森林节点 ====================
forest = Node(
    game=game,
    node_id="forest",
    name="迷雾森林",
    desc="""你进入了迷雾森林。高大的树木遮蔽了天空，雾气在林间缭绕。

树叶沙沙作响，似乎有什么东西在暗处窥视着你。

{combat_status}""",
    init_data={"combat_status": "'你小心翼翼地前进...'"},
    set_data={"turns": "turns + 1"},
    on_ready="""
if not defeated_goblin:
    data['combat_status'] = '突然，一只哥布林从灌木丛中跳了出来！它挥舞着生锈的短刀，发出刺耳的嘶吼。'
    data['enemy_hp'] = 40
    data['enemy_name'] = '森林哥布林'
    data['enemy_attack'] = 8
    data['in_combat'] = True
    data['combat_log'] = '战斗开始了！'
else:
    data['combat_status'] = '森林很安静，哥布林的尸体已经消失。道路现在安全了。'
    data['in_combat'] = False
"""
)

# ==================== 战斗节点系统 ====================
goblin_combat = Node(
    game=game,
    node_id="goblin_combat",
    name="战斗：森林哥布林",
    desc="""{combat_log}

【战斗状态】
{player_name}: {hp}/{max_hp} HP
{enemy_name}: {enemy_hp} HP

你要如何行动？""",
    set_data={"turns": "turns + 1"},
    on_ready="""
import random
# 预计算伤害值（显示在选项描述中）
data['player_dmg'] = max(1, attack + random.randint(-3, 5))
# 先用局部变量计算，再存入data
enemy_dmg_raw_val = max(1, enemy_attack + random.randint(-2, 2))
data['enemy_dmg'] = max(0, enemy_dmg_raw_val - defense // 3)
"""
)

# 战斗处理节点
goblin_attack_process = Node(
    game=game,
    node_id="goblin_attack_process",
    name="攻击中...",
    desc="你挥舞武器攻击哥布林！",
    set_data={
        "enemy_hp": "enemy_hp - player_dmg",
        "hp": "hp - enemy_dmg",
        # 使用 f-string 来插入变量值
        "combat_log": "f'你造成了{player_dmg}点伤害，但受到了{enemy_dmg}点反击！'"
    },
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "enemy_hp <= 0", "node_id": "victory_goblin"},
        {"condition": "True", "node_id": "goblin_combat"}
    ]
)

goblin_defend_process = Node(
    game=game,
    node_id="goblin_defend_process",
    name="防御中...",
    desc="你举起盾牌/武器采取防御姿态。",
    set_data={
        "hp": "hp - max(0, enemy_dmg // 2)",
        "combat_log": "'你采取防御姿态，减少了受到的伤害！'"
    },
    on_ready="""
import random
# 防御时有机会反击造成少量伤害
if random.random() < 0.3:
    data['enemy_hp'] = enemy_hp - attack // 2
    data['combat_log'] = '你成功格挡并反击，造成了少量伤害！'
""",
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "enemy_hp <= 0", "node_id": "victory_goblin"},
        {"condition": "True", "node_id": "goblin_combat"}
    ]
)

goblin_potion_process = Node(
    game=game,
    node_id="goblin_potion_process",
    name="使用药水...",
    desc="你迅速喝下一瓶生命药水，甜美的液体流淌过喉咙。",
    set_data={
        "potions": "potions - 1",
        "hp": "min(max_hp, hp + 30)",
        "combat_log": "'你恢复了生命值，精神一振！'"
    },
    defaults=[{"condition": "True", "node_id": "goblin_combat"}]
)

# ==================== 洞穴入口 ====================
cave_entrance = Node(
    game=game,
    node_id="cave_entrance",
    name="遗忘之城入口",
    desc="""你来到了山脉深处，面前是一座巨大的石门，上面刻满了古老的符文。

石门紧闭，似乎需要某种方式才能打开。

{entrance_desc}""",
    init_data={"entrance_desc": "'门缝中透出微弱的光芒和低沉的嗡鸣声。'"},
    set_data={"turns": "turns + 1"},
    defaults=[
        {
            "condition": "has_key and not solved_riddle",
            "node_id": "riddle_room"
        },
        {
            "condition": "solved_riddle",
            "node_id": "inner_sanctum"
        }
    ]
)

# 检查石门处理节点
examine_door_process = Node(
    game=game,
    node_id="examine_door_process",
    name="观察石门",
    desc="""你仔细观察石门上的符文，发现了隐藏的文字：

"唯有智者，方能得见真相。"

{map_hint}""",
    init_data={"map_hint": "''"},
    on_ready="""
print('你记下了门上的铭文。')
if has_map:
    data['map_hint'] = '你突然想起购买的古老地图，背面写着："答案是...地图本身！"'
else:
    data['map_hint'] = '这似乎是某种提示，但你毫无头绪。'
""",
    defaults=[{"condition": "True", "node_id": "cave_entrance"}]
)

riddle_room = Node(
    game=game,
    node_id="riddle_room",
    name="符文密室",
    desc="""你用钥匙打开了石门。门后是一个圆形房间，墙壁上漂浮着发光的符文。

房间中央有一个石台，上面刻着谜题：

"我有城市但没有房屋，有山脉但没有树木，有水但没有鱼，有道路但没有车辆。我是什么？"

{puzzle_status}""",
    init_data={"puzzle_status": "'你需要回答这个谜题才能继续前进。'", "attempts": "3"},
    set_data={"turns": "turns + 1"}
)

# 解答谜题处理节点
solve_riddle_process = Node(
    game=game,
    node_id="solve_riddle_process",
    name="解答谜题",
    desc="""你自信地回答："是地图。"

符文瞬间亮起耀眼的绿光，古老的魔法认可了你的智慧。石门缓缓向两侧滑开，露出通往核心圣所的阶梯。

你深吸一口气，准备迎接最后的挑战。""",
    set_data={"solved_riddle": "True", "turns": "turns + 1"},
    defaults=[{"condition": "True", "node_id": "inner_sanctum"}]
)

riddle_wrong_process = Node(
    game=game,
    node_id="riddle_wrong_process",
    name="回答错误",
    desc="符文闪烁着刺眼的红色光芒！",
    set_data={"attempts": "attempts - 1", "hp": "hp - 10"},
    on_ready="""
if attempts <= 1:
    print('错误次数太多！魔法能量反噬了你。')
else:
    print('答案错误，再试一次。（剩余尝试次数：', attempts-1, '）')
print(f'你受到了10点伤害！剩余生命值：{hp-10}')
""",
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "True", "node_id": "riddle_room"}
    ]
)

# ==================== 最终战斗 ====================
# ==================== 最终战斗 ====================
inner_sanctum = Node(
    game=game,
    node_id="inner_sanctum",
    name="核心圣所",
    desc="""你终于进入了遗忘之城的核心。这是一个巨大的穹顶大厅，中央悬浮着一颗散发着紫色光芒的水晶——"永恒之源"。

然而，一个身影挡住了你的去路。那是守护水晶的古代魔像，它的身体由黑曜石构成，双眼燃烧着红色的火焰。

"凡人，你不该来此。"魔像的声音如同滚雷，"证明你的价值，或者死在这里。"

魔像向你冲来！这是最后的战斗！""",
    set_data={
        "turns": "turns + 1",
        "enemy_hp": "100",
        "enemy_name": "'古代魔像'",
        "enemy_attack": "18",
        "in_combat": "True",
        "final_boss": "True",
        "combat_log": "'战斗开始！古代魔像散发着恐怖的威压...'"
    }
)

boss_combat = Node(
    game=game,
    node_id="boss_combat",
    name="决战：古代魔像",
    desc="""{combat_log}

【最终决战】
{player_name}: {hp}/{max_hp} HP | 药水: {potions}瓶
{enemy_name}: {enemy_hp}/100 HP

圣所中的能量在激荡，决定命运的瞬间到了！""",
    set_data={"turns": "turns + 1"},
    on_ready="""
import random
# Boss战伤害计算
data['player_dmg'] = attack + random.randint(0, 8)
# Boss攻击有概率暴击
crit = random.random() < 0.3
base_dmg = enemy_attack + random.randint(0, 5)
data['enemy_dmg'] = base_dmg * 2 if crit else base_dmg
data['crit_happened'] = crit
"""
)

boss_attack_process = Node(
    game=game,
    node_id="boss_attack_process",
    name="全力攻击",
    desc="你发动猛烈攻击！",
    set_data={
        "enemy_hp": "enemy_hp - player_dmg",
        "hp": "hp - enemy_dmg",
        "combat_log": "f'你全力一击造成{player_dmg}点伤害！古代魔像反击造成{enemy_dmg}点伤害！'"
    },
    on_ready="""
if crit_happened:
    print('>>> 古代魔像发动了毁灭性暴击！')
""",
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "enemy_hp <= 0", "node_id": "true_ending"},
        {"condition": "True", "node_id": "boss_combat"}
    ]
)

boss_defend_process = Node(
    game=game,
    node_id="boss_defend_process",
    name="坚守防御",
    desc="你采取稳固的防守姿态。",
    set_data={
        "hp": "hp - max(0, enemy_dmg // 2 - defense // 4)",
        "enemy_hp": "enemy_hp - player_dmg // 2",
        "combat_log": "f'你稳固防守，只受到少量伤害，并反击造成{player_dmg // 2}点伤害！'"
    },
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "enemy_hp <= 0", "node_id": "true_ending"},
        {"condition": "True", "node_id": "boss_combat"}
    ]
)

boss_potion_process = Node(
    game=game,
    node_id="boss_potion_process",
    name="使用药水",
    desc="你喝下药水恢复生命，但魔像趁机攻击！",
    set_data={
        "potions": "potions - 1",
        # 伤害减半计算，稍微吃点防御减免
        "hp": "min(max_hp, hp + 30) - max(0, enemy_dmg // 2 - defense // 5)",
        "combat_log": "f'你迅速喝下药水恢复30生命，魔像趁机攻击造成{max(0, enemy_dmg // 2 - defense // 5)}点伤害！'"
    },
    defaults=[
        {"condition": "hp <= 0", "node_id": "game_over_dead"},
        {"condition": "enemy_hp <= 0", "node_id": "true_ending"},
        {"condition": "True", "node_id": "boss_combat"}
    ]
)

# ==================== 结局节点 ====================
victory_goblin = Node(
    game=game,
    node_id="victory_goblin",
    name="胜利",
    desc="""哥布林发出一声惨叫，倒在地上化为灰烬。

你搜查了它的巢穴，发现了一些金币和一瓶药水。

获得战利品：
- 30金币
- 1瓶生命药水
- 哥布林的钥匙（看起来能打开某扇门）

森林的道路现在已经安全，你可以继续向山脉深处前进。""",
    set_data={
        "defeated_goblin": "True",
        "gold": "gold + 30",
        "potions": "potions + 1",
        "has_key": "True",
        "in_combat": "False"
    }
)

true_ending = Node(
    game=game,
    node_id="true_ending",
    name="结局：永恒之光",
    desc="""随着最后一击，古代魔像轰然倒塌，化为碎石。

你走向"永恒之源"，水晶的光芒温柔地包裹着你。这不是邪恶的力量，而是古老文明留下的知识之光。

你选择了接受这份力量，承诺用它来守护世界的平衡。

你在第 {turns} 回合完成了冒险。
谢谢你游玩《遗忘之城》！""",
    end_desc="""【游戏通关 - 完美结局】

{player_name}成为了新的守护者，遗忘之城的秘密得以保存。
你的名字将被载入传说，直到时间的尽头...""",
    set_data={"in_combat": "False"}
)

game_over_dead = Node(
    game=game,
    node_id="game_over_dead",
    name="你死了",
    desc="""黑暗吞噬了你的视野...

你的冒险在这里结束了。

统计：
- 存活回合数: {turns}
- 职业: {player_class_name}
- 获得金币: {gold}""",
    end_desc="""【游戏结束】

{player_name}的故事成为了另一个传说。
也许下一位冒险者会完成你未竟的事业...""",
    set_data={"in_combat": "False"}
)

escaped = Node(
    game=game,
    node_id="escaped",
    name="撤退",
    desc="""你选择了撤退，保存实力。

虽然活了下来，但遗忘之城的秘密依然无人知晓...""",
    end_desc="【游戏结束 - 生还者结局】\n\n有时候，活着本身就是最大的胜利。",
    set_data={"in_combat": "False"}
)

# ==================== 选项配置 ====================

# 从intro到village
intro.add_option(Option(
    game=game,
    option_id="go_village",
    name="进入村庄",
    desc="前往青石村准备装备",
    next_node_id="village"
))

# 村庄选项
village.add_option(Option(
    game=game,
    option_id="go_shop",
    name="去杂货店",
    desc="购买补给",
    next_node_id="shop"
))

village.add_option(Option(
    game=game,
    option_id="go_forest",
    name="前往迷雾森林",
    desc="踏上寻找遗忘之城的旅程",
    next_node_id="forest"
))

village.add_option(Option(
    game=game,
    option_id="rest",
    name="在旅馆休息",
    desc="完全恢复生命值（花费10金币）",
    next_node_id="rest_process",
    move_condition="gold >= 10 and hp < max_hp",
    cant_move_desc="金币不足或生命值已满"
))

# 商店选项
shop.add_option(Option(
    game=game,
    option_id="buy_potion",
    name="购买生命药水 (30金币)",
    desc="恢复30点生命值的药水",
    next_node_id="buy_potion_process",
    move_condition="gold >= 30",
    cant_move_desc="金币不足"
))

shop.add_option(Option(
    game=game,
    option_id="buy_map",
    name="购买古老地图 (50金币)",
    desc="标记秘密通道的地图",
    next_node_id="buy_map_process",
    move_condition="gold >= 50 and not has_map",
    cant_move_desc="金币不足或已经拥有地图"
))

shop.add_option(Option(
    game=game,
    option_id="leave_shop",
    name="离开商店",
    desc="返回村庄广场",
    next_node_id="village"
))

# 森林选项
forest.add_option(Option(
    game=game,
    option_id="fight_goblin",
    name="准备战斗",
    desc="迎战哥布林",
    next_node_id="goblin_combat",
    move_condition="not defeated_goblin",
    show_condition="not defeated_goblin"
))

forest.add_option(Option(
    game=game,
    option_id="to_cave",
    name="前往山脉深处",
    desc="继续前进到遗忘之城",
    next_node_id="cave_entrance",
    move_condition="defeated_goblin",
    cant_move_desc="你需要先击败哥布林才能安全通过森林"
))

forest.add_option(Option(
    game=game,
    option_id="back_to_village",
    name="返回村庄",
    desc="撤退并恢复状态",
    next_node_id="village"
))

# 战斗系统选项 - 跳转到处理节点
goblin_combat.add_option(Option(
    game=game,
    option_id="attack",
    name="攻击",
    desc="发动攻击（预计伤害：{player_dmg}）",
    next_node_id="goblin_attack_process"
))

goblin_combat.add_option(Option(
    game=game,
    option_id="defend",
    name="防御",
    desc="减少受到的伤害并有机会反击",
    next_node_id="goblin_defend_process"
))

goblin_combat.add_option(Option(
    game=game,
    option_id="use_potion",
    name="使用药水",
    desc="恢复30点生命值（剩余{potions}瓶）",
    next_node_id="goblin_potion_process",
    move_condition="potions > 0 and hp < max_hp",
    cant_move_desc="没有药水或生命值已满"
))

goblin_combat.add_option(Option(
    game=game,
    option_id="flee",
    name="逃跑",
    desc="尝试逃离战斗",
    next_node_id="forest",
    move_condition="agility > 10",
    cant_move_desc="你的敏捷不够，无法逃跑！"
))

# 从胜利到洞穴
victory_goblin.add_option(Option(
    game=game,
    option_id="continue_journey",
    name="继续前进",
    desc="前往遗忘之城",
    next_node_id="cave_entrance"
))

victory_goblin.add_option(Option(
    game=game,
    option_id="back_village_after_win",
    name="先回村补给",
    desc="带着战利品回青石村休息整顿（推荐，可以买药休息）",
    next_node_id="village"
))

# 洞穴入口选项
cave_entrance.add_option(Option(
    game=game,
    option_id="use_key",
    name="使用钥匙",
    desc="用哥布林的钥匙打开石门",
    next_node_id="riddle_room",
    move_condition="has_key",
    show_condition="has_key and not solved_riddle",
    cant_move_desc="你没有钥匙"
))

cave_entrance.add_option(Option(
    game=game,
    option_id="examine",
    name="检查石门",
    desc="仔细观察符文",
    next_node_id="examine_door_process"
))

cave_entrance.add_option(Option(
    game=game,
    option_id="back_forest",
    name="返回森林",
    desc="暂时撤退",
    next_node_id="forest"
))

# 谜题房间选项
riddle_room.add_option(Option(
    game=game,
    option_id="answer_map",
    name="回答：地图",
    desc="说出你的答案",
    next_node_id="solve_riddle_process"
))

riddle_room.add_option(Option(
    game=game,
    option_id="answer_other",
    name="回答其他答案",
    desc="尝试猜测",
    next_node_id="riddle_wrong_process"
))

riddle_room.add_option(Option(
    game=game,
    option_id="retreat_riddle",
    name="撤退",
    desc="离开密室",
    next_node_id="cave_entrance"
))

# Boss战选项
inner_sanctum.add_option(Option(
    game=game,
    option_id="engage_boss",
    name="迎战魔像",
    desc="开始最终战斗",
    next_node_id="boss_combat"
))

inner_sanctum.add_option(Option(
    game=game,
    option_id="flee_final",
    name="逃离圣所",
    desc="放弃挑战",
    next_node_id="escaped"
))

boss_combat.add_option(Option(
    game=game,
    option_id="boss_attack",
    name="全力攻击",
    desc="造成{player_dmg}点伤害",
    next_node_id="boss_attack_process"
))

boss_combat.add_option(Option(
    game=game,
    option_id="boss_defend",
    name="坚守防御",
    desc="采取守势并反击",
    next_node_id="boss_defend_process"
))

boss_combat.add_option(Option(
    game=game,
    option_id="boss_potion",
    name="使用药水",
    desc="恢复生命（剩余{potions}瓶）",
    next_node_id="boss_potion_process",
    move_condition="potions > 0"
))

# ==================== 启动游戏 ====================
if __name__ == "__main__":
    game.play()
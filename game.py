from TextAdventure import Game, Node, Option

# ==================== 游戏配置 ====================

game = Game(
    start_node_id="start",
    game_name="雨夜旅馆",
    init_input=[
        {
            "prompt": "请输入你的名字：",
            "name": "player_name",
            "converter": "str",
            "condition": "len(val) > 0",
            "err_desc": "名字不能为空"
        },
        {
            "prompt": "选择你的职业（1-侦探 2-医生）：",
            "name": "job",
            "converter": "int",
            "condition": "val in [1, 2]",
            "err_desc": "请输入 1 或 2"
        }
    ]
)

# ==================== 变量初始化 ====================
# 使用init_data设置所有默认值，避免在desc中使用表达式

start = Node(
    game=game,
    node_id="start",
    name="暴风雨夜",
    desc="""
外面雷雨交加，你的车在山路上抛锚了。
前方有一家老旧旅馆——"安心旅馆"。

你浑身湿透地走进大厅，柜台后站着一个面色苍白的男人。
"欢迎，今晚只有您一位客人。"他微笑着，但眼神飘忽。

欢迎，{player_name}。你的职业是：{job_name}。

{profession_hint}

【系统】线索收集: {clue_count} | 信任度: {trust_owner}
    """.strip(),
    init_data={
        "clue_count": "0",
        "trust_owner": "50",
        "has_key": "False",
        "know_secret": "False",
        "investigated_room": "False",
        "checked_basement": "False",
        "job_name": "'职业未设置'",
        "profession_hint": "'请先设置职业'",
        "ending_rating": "'未评价'"
    },
    # on_load在init_data之前执行，用于设置依赖job的初始值
    on_load="""
if job == 1:
    data['job_name'] = '侦探'
    data['profession_hint'] = '【侦探直觉】你觉得这个老板有些可疑...'
else:
    data['job_name'] = '医生'
    data['profession_hint'] = '【医生观察】你注意到老板左手有新鲜的绷带...'
    """
)

# ==================== 大厅选项 ====================

opt_room = Option(
    game=game,
    option_id="go_room",
    name="去房间休息",
    desc="你累了，想先休息一下",
    next_node_id="room"
)

opt_talk = Option(
    game=game,
    option_id="talk_owner",
    name="与老板交谈",
    desc="试图了解更多信息",
    next_node_id="talk"
)

opt_leave = Option(
    game=game,
    option_id="try_leave",
    name="尝试离开",
    desc="这地方感觉不太对，想冒雨离开",
    next_node_id="leave_attempt",
    move_condition="trust_owner < 30",
    cant_move_desc="这个老板应该没什么问题，或许该再跟他说说话。"
)

start.add_option(opt_room)
start.add_option(opt_talk)
start.add_option(opt_leave)
game.add_node(start)

# ==================== 与老板交谈 ====================

talk = Node(
    game=game,
    node_id="talk",
    name="诡异的对谈",
    desc="""
"这旅馆开了多久了？"你问道。

"二十年了。"老板擦拭着杯子，"以前很热闹，自从...那场事故后，客人就少了。"

他顿了顿："您相信这世上有无法解释的事吗？"

他的目光越过你，看向走廊深处的一扇紧闭的门。

{system_hint}
    """,
    init_data={"system_hint": "' '"},
    set_data={"trust_owner": "trust_owner - 10"},
    # 使用set_data覆盖system_hint，在desc中展示
    on_load="data['system_hint'] = '【系统】信任度下降，你感到一丝不安'"
)

opt_ask_accident = Option(
    game=game,
    option_id="ask_accident",
    name="询问事故详情",
    desc="追问二十年前发生了什么",
    next_node_id="accident_story"
)

opt_ask_door = Option(
    game=game,
    option_id="ask_door",
    name="询问那扇门",
    desc="问走廊深处的门通向哪里",
    next_node_id="door_story"
)

opt_back_start = Option(
    game=game,
    option_id="back_start",
    name="结束对话，回到大厅",
    desc="不再追问",
    next_node_id="start"
)

talk.add_option(opt_ask_accident)
talk.add_option(opt_ask_door)
talk.add_option(opt_back_start)
game.add_node(talk)

# ==================== 事故故事 ====================

accident = Node(
    game=game,
    node_id="accident_story",
    name="二十年前的阴影",
    desc="""
老板的表情变得阴沉。

"一场火灾...死了三个人。我的妻子和女儿..."他的声音颤抖，"警方说是意外，但我知道不是。"

他突然抓住你的手："如果您能帮我查明真相，我重重有谢！"

你注意到他说"三个人"，但只提到了妻子和女儿。

{clue_hint}
    """,
    init_data={"clue_hint": "' '"},
    set_data={
        "clue_count": "clue_count + 1",
        "know_secret": "True"
    },
    on_load="data['clue_hint'] = '【线索 +1】火灾死亡人数疑点'"
)

back_opt = Option(game, option_id="back_from_accident", name="继续交谈", next_node_id="talk")
accident.add_option(back_opt)
game.add_node(accident)

# ==================== 门的故事 ====================

door = Node(
    game=game,
    node_id="door_story",
    name="地下室",
    desc="""
"那是地下室，存放旧物的地方。"老板的眼神闪烁，"门锁坏了，不建议下去。"

他说不建议，但没有说不能。

你注意到他腰间的钥匙串上有一把生锈的铜钥匙。

{clue_hint}
    """,
    init_data={"clue_hint": "' '"},
    set_data={"clue_count": "clue_count + 1"},
    on_load="data['clue_hint'] = '【线索 +1】地下室可能藏着什么'"
)

door.add_option(back_opt)
game.add_node(door)

# ==================== 尝试离开 ====================

leave = Node(
    game=game,
    node_id="leave_attempt",
    name="暴雨中的抉择",
    desc="""
你推开大门，狂风暴雨瞬间打湿了全身。

但就在这一瞬间，你借着闪电的光，看到停车棚里有一辆车的轮廓——车牌被拆了，但车型和老板描述"二十年前烧毁的车"完全不同。

更可怕的是，你看到自己的车旁边，站着一个人影，正在往你的油箱里倒着什么...

你迅速退回室内，心脏狂跳。

{clue_hint}

{system_hint}
    """,
    init_data={
        "clue_hint": "' '",
        "system_hint": "' '"
    },
    set_data={
        "trust_owner": "trust_owner - 30",
        "clue_count": "clue_count + 2"
    },
    on_load="""
data['clue_hint'] = '【线索 +2】车辆疑点 & 破坏行为'
data['system_hint'] = '【系统】信任度暴跌，你意识到危险真实存在'
    """
)

leave.add_option(Option(game, option_id="rush_room", name="悄悄回房间锁门", next_node_id="room"))
leave.add_option(Option(game, option_id="confront", name="质问老板", next_node_id="confront"))
game.add_node(leave)

# ==================== 房间 ====================

room = Node(
    game=game,
    node_id="room",
    name="客房 204",
    desc="""
房间陈设老旧但整洁。你锁上门，开始思考。

窗外雨声轰鸣，但你隐约听到楼下有声音——像是重物拖动的声音。

你的职业本能告诉你应该仔细调查这个房间。

{room_status}
    """,
    init_data={"room_status": "'【系统】房间尚未调查'"},
    on_load="""
if investigated_room:
    data['room_status'] = '【系统】你已经搜查过这里'
    """
)

opt_search = Option(
    game=game,
    option_id="search_room",
    name="搜查房间",
    desc="仔细检查每个角落",
    next_node_id="room_search",
    show_condition="not investigated_room"
)

opt_sleep = Option(
    game=game,
    option_id="sleep",
    name="尝试睡觉",
    desc="也许只是自己太紧张了",
    next_node_id="sleep_ending"
)

opt_go_down = Option(
    game=game,
    option_id="go_down",
    name="下楼探查",
    desc="去查看那个拖动声音",
    next_node_id="downstairs"
)

room.add_option(opt_search)
room.add_option(opt_sleep)
room.add_option(opt_go_down)
game.add_node(room)

# ==================== 房间搜查 ====================

room_search = Node(
    game=game,
    node_id="room_search",
    name="惊人发现",
    desc="""
你在床垫下发现了一本日记，最后一页写着：

"他要杀我，就像杀之前那些人一样。地下室有证据，但我拿不到钥匙。如果我死了，请找到地下室里的..."

字迹到此中断。

你还发现床底下有一部老式手机，还有电，但无信号——相册里存着几张照片：老板和不同客人的合影，但那些客人的脸都被红笔划掉了。

{clue_hint}

{system_hint}
    """,
    init_data={
        "clue_hint": "' '",
        "system_hint": "' '"
    },
    set_data={
        "clue_count": "clue_count + 2",
        "investigated_room": "True",
        "trust_owner": "trust_owner - 20"
    },
    on_load="""
data['clue_hint'] = '【线索 +2】日记 & 受害者照片'
data['system_hint'] = '【系统】你意识到自己是下一个目标'
    """
)

room_search.add_option(opt_go_down)
room_search.add_option(Option(game, option_id="plan", name="制定逃生计划", next_node_id="plan_escape"))
game.add_node(room_search)

# ==================== 制定计划 ====================

plan = Node(
    game=game,
    node_id="plan_escape",
    name="冷静分析",
    desc="""
你深吸一口气，开始整理思路。

{analysis_text}

你需要做出选择：冒险去地下室找证据，还是直接逃跑？

【系统】当前线索: {clue_count}
    """,
    init_data={"analysis_text": "' '"},
    on_load="""
if clue_count >= 4:
    if job == 1:
        data['analysis_text'] = '【分析】他是连环杀手，地下室有决定性证据\\n【侦探直觉】需要确凿证据才能定罪，地下室必须去'
    else:
        data['analysis_text'] = '【分析】他是连环杀手，地下室有决定性证据\\n【医生观察】他的绷带是伪造的——没有渗血，包扎方式也不对'
else:
    if job == 1:
        data['analysis_text'] = '【分析】他很可疑，但证据还不足\\n【侦探直觉】需要更多线索才能确定'
    else:
        data['analysis_text'] = '【分析】他很可疑，但证据还不足\\n【医生观察】他的行为可疑，但需要更多证据'
    """
)

opt_basement = Option(
    game=game,
    option_id="to_basement",
    name="去地下室",
    desc="寻找决定性证据",
    next_node_id="basement",
    move_condition="clue_count >= 3",
    cant_move_desc="证据不足，贸然去地下室太危险。需要更多线索。"
)

opt_run = Option(
    game=game,
    option_id="run_away",
    name="趁夜逃跑",
    desc="从窗户离开，放弃调查",
    next_node_id="escape_ending"
)

plan.add_option(opt_basement)
plan.add_option(opt_run)
game.add_node(plan)

# ==================== 地下室 ====================

basement = Node(
    game=game,
    node_id="basement",
    name="地狱之门",
    desc="""
你撬开地下室的门，霉味和福尔马林的气味扑面而来。

墙上贴满了剪报——"山区连环失踪案，已发现7具尸体"。
桌上放着一本名册，记录了近二十年的"客人"信息。

突然，灯光大亮。老板站在楼梯口，手里拿着刀。

"我通常不会这么快动手的，"他叹气，"但您太聪明了。"

【系统】最终对决！线索数：{clue_count}，职业：{job_name}
    """,
    set_data={"checked_basement": "True"},
    defaults=[
        {"condition": "job == 1 and clue_count >= 5", "node_id": "detective_win"},
        {"condition": "job == 2", "node_id": "doctor_win"},
        {"condition": "True", "node_id": "bad_ending"}
    ]
)

game.add_node(basement)

# ==================== 侦探胜利 ====================

detective_win = Node(
    game=game,
    node_id="detective_win",
    name="正义执行",
    desc="""
你冷静地举起手机——刚才你一直在直播。

"李警官，都录下来了吗？"你对着手机说。

老板脸色大变，转身想逃，却被埋伏在门口的特警按倒。你早就联系了警方，这一切都是陷阱——为了抓住这个潜逃二十年的恶魔。

"谢谢你，侦探。"一个苍老的声音从阴影中走出，是当年火灾的真正幸存者，"我终于可以为女儿报仇了。"

【真结局：侦探的正义】
你不仅救了自己，还揭开了二十年前的真相。老板就是当年纵火杀人的凶手，而"安心旅馆"是他继续犯罪的猎场。
    """,
    end_desc="结局：正义执行 | 完美侦探 | 你展现了卓越的推理能力和勇气。"
)
game.add_node(detective_win)

# ==================== 医生胜利 ====================

doctor_win = Node(
    game=game,
    node_id="doctor_win",
    name="医者仁心",
    desc="""
你没有后退，反而向前走了一步。

"你的左手，不是烧伤，是化学腐蚀伤，对吗？"你平静地说，"二十年前你试图销毁证据时受的伤。它一直在溃烂，因为你不敢看医生。"

老板愣住了，刀微微颤抖。

"我可以帮你治疗，"你伸出手，"但你要先放下刀，自首。"

也许是你的职业光环，也许是他真的疼了太久。十分钟后，他跪在地上痛哭，刀落在一边。

【真结局：医者仁心】
你用专业知识瓦解了凶手的心理防线。警方在他自首后发现了地下室的全部证据，解决了困扰多年的连环失踪案。
    """,
    end_desc="结局：医者仁心 | 救赎者 | 你用仁慈和专业拯救了一个灵魂，也阻止了更多悲剧。"
)
game.add_node(doctor_win)

# ==================== 坏结局 ====================

bad_end = Node(
    game=game,
    node_id="bad_ending",
    name="雨夜终结",
    desc="""
你试图反抗，但老板比你快得多。

"第8个..."这是他对你说的最后一句话。

你的意识逐渐模糊，最后的画面是地下室墙上那些剪报，和一盏摇曳的灯泡。

【坏结局：雨夜终结】
安心旅馆继续营业，等待下一位客人...
    """,
    end_desc="结局：雨夜终结 | 牺牲者 | 提示：收集更多线索，或选择正确的职业策略。"
)
game.add_node(bad_end)

# ==================== 睡眠结局 ====================

sleep_end = Node(
    game=game,
    node_id="sleep_ending",
    name="长眠",
    desc="""
你太累了，很快就睡着了。

梦中，你感觉有人在看着你。你想醒来，但身体沉重如铅。

当你终于睁开眼睛时，发现自己无法动弹——你被注射了肌肉松弛剂。老板站在床边，微笑着：

"睡吧，这是最好的方式，没有痛苦。"

【结局：长眠】
有时候，好奇心是唯一的生存机会...
    """,
    end_desc="结局：长眠 | 过于大意 | 提示：在陌生环境中保持警惕。"
)
game.add_node(sleep_end)

# ==================== 逃跑结局 ====================

escape_end = Node(
    game=game,
    node_id="escape_ending",
    name="幸存者",
    desc="""
你从窗户爬出，在暴雨中狂奔。

身后传来老板的喊声，但你不敢回头。你跑了整整两个小时，直到看到公路上的车灯。

你活下来了，但那些证据永远留在了地下室。安心旅馆第二天就关门了，老板不知所踪。

三年后，另一座山区发生了类似的失踪案...

【结局：幸存者】
你保住了性命，但正义未得伸张。
    """,
    end_desc="结局：幸存者 | 谨慎的懦夫 | 提示：有时候，勇敢面对比逃跑更需要智慧。"
)
game.add_node(escape_end)

# ==================== 对峙 ====================

confront = Node(
    game=game,
    node_id="confront",
    name="正面对峙",
    desc="""
"你在我的车里放了什么？"你质问道。

老板的表情瞬间扭曲，他抄起柜台下的扳手向你冲来。

你转身就跑，但大门被锁死了。你被困在了大厅里！
    """,
    defaults=[
        {"condition": "clue_count >= 3", "node_id": "fight_back"},
        {"condition": "True", "node_id": "captured"}
    ]
)
game.add_node(confront)

# ==================== 反击 ====================

fight_back = Node(
    game=game,
    node_id="fight_back",
    name="绝地反击",
    desc="""
你抓起花瓶砸向他，同时大声喊出你掌握的证据：

"我知道地下室有什么！我知道那些尸体！我已经报警了！"

他迟疑了一秒——这一秒足够你抓起钥匙串，冲向地下室。

你反锁了地下室的门，用手机微弱的信号发出了定位。当警方破门而入时，你正用日记和名册作为证据，记录一切。

【结局：绝地反击】
险中求胜，你不仅活了下来，还将凶手绳之以法。
    """,
    end_desc="结局：绝地反击 | 勇敢的幸存者 | 你在绝境中保持冷静，用智慧扭转了局面。"
)
game.add_node(fight_back)

# ==================== 被捕 ====================

captured = Node(
    game=game,
    node_id="captured",
    name="无力反抗",
    desc="""
你试图反抗，但你对他的了解太少，无法找到他的软肋。

扳手击中你的头部，世界陷入黑暗。

当你再次醒来时，你发现自己被绑在地下室的椅子上。老板正在准备工具，哼着歌。

"别担心，"他说，"很快就会结束的。"

【结局：无力反抗】
知识就是力量，而无知在此刻是致命的。
    """,
    end_desc="结局：无力反抗 | 准备不足 | 提示：收集更多线索后再面对危险。"
)
game.add_node(captured)

# ==================== 下楼探查 ====================

downstairs = Node(
    game=game,
    node_id="downstairs",
    name="致命发现",
    desc="""
你悄悄下楼，声音来自厨房。

透过门缝，你看到老板正在...处理一具尸体。那具尸体穿着和你相似的衣服。

他早就准备好了"替代者"。如果你消失了，他会用这具尸体伪装成你，制造你"意外死亡"的假象。

你不小心碰倒了花瓶。他转过头，与你四目相对。
    """,
    set_data={"clue_count": "clue_count + 2"},
    defaults=[
        {"condition": "job == 1", "node_id": "detective_bluff"},
        {"condition": "True", "node_id": "chase"}
    ]
)
game.add_node(downstairs)

# ==================== 侦探虚张声势 ====================

bluff = Node(
    game=game,
    node_id="detective_bluff",
    name="虚张声势",
    desc="""
作为侦探，你迅速冷静下来，反而走进厨房。

"精彩的手法，"你鼓掌，"但你知道你留下了多少证据吗？我来的路上已经给搭档发了定位。如果我出事，你就是头号嫌疑人。"

你赌他不敢冒险。幸运的是，你赌对了——他犹豫的表情说明他还有理智。

"你想要什么？"他放下工具。

"钥匙。地下室钥匙。我要看证据，然后决定要不要帮你。"

你拿到了钥匙，也争取到了时间。

【获得地下室钥匙】
    """,
    set_data={"has_key": "True", "clue_count": "clue_count + 1"}
)
bluff.add_option(Option(game, option_id="to_basement_now", name="立即前往地下室", next_node_id="basement"))
bluff.add_option(Option(game, option_id="bluff_leave", name="趁机逃跑", next_node_id="escape_ending"))
game.add_node(bluff)

# ==================== 被追逐 ====================

chase = Node(
    game=game,
    node_id="chase",
    name="生死追逐",
    desc="""
他冲了过来！你转身就跑，但他对地形太熟悉了。

你撞进储藏室，情急之下抓起一瓶清洁剂喷向他的眼睛。他惨叫着后退，你趁机逃回房间锁门。

你的心脏快要跳出胸腔。你需要立刻做出决定！

【系统】危险等级：极高
    """
)
chase.add_option(Option(game, option_id="hide", name="跳窗逃跑", next_node_id="escape_ending"))
chase.add_option(Option(game, option_id="fight", name="拿武器拼命", next_node_id="captured"))
game.add_node(chase)

# ==================== 运行游戏 ====================

if __name__ == "__main__":
    game.play()
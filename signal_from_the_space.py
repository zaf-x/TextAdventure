from TextAdventure import Game, Node, Option

# ============ 游戏初始化 ============
game = Game(
    start_node_id="start",
    game_name="深空信号",
    init_input=[
        {
            "prompt": "请输入你的姓名：",
            "name": "player_name",
            "converter": "str",
            "condition": "len(val) > 0",
            "err_desc": "姓名不能为空"
        },
        {
            "prompt": "选择你的职业（1-工程师 2-生物学家 3-心理学家）：",
            "name": "profession",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "请输入 1、2 或 3"
        }
    ]
)

# ============ 节点定义 ============

# 开场
start = Node(
    game=game,
    node_id="start",
    name="觉醒",
    desc="""
你在一阵刺耳的警报声中醒来。

舱室的红灯闪烁，氧气循环系统发出不规律的嗡鸣。
你看了看床头的铭牌——{player_name}。

你是"深空七号"勘探船上的船员。三天前，你们收到了一个来自
柯伊伯带方向的神秘信号。然后……记忆出现了断层。

通讯器里传来船长沙哑的声音："所有人到舰桥集合。我们……
我们可能犯了一个大错。"
    """,
    init_data={
        "signal_decoded": "False",
        "engine_status": "85",
        "crew_trust": "50",
        "sanity": "100",
        "has_toolkit": "False",
        "captain_revealed": "False"
    }
)

# 选项：去舰桥
start.add_option(Option(
    game=game,
    option_id="goto_bridge",
    name="立即前往舰桥",
    next_node_id="bridge"
))

# 选项：检查终端（逻辑职业或高智力）
start.add_option(Option(
    game=game,
    option_id="check_terminal",
    name="先检查个人终端的日志",
    show_condition="profession == 1 or profession == 2",
    next_node_id="terminal"
))

# 选项：拿工具包
start.add_option(Option(
    game=game,
    option_id="take_toolkit",
    name="拿起床头的应急工具包",
    next_node_id="toolkit"
))

game.add_node(start)

# ============ 终端节点 ============
terminal = Node(
    game=game,
    node_id="terminal",
    name="加密日志",
    desc="""
你快速浏览终端上的加密日志。

【72小时前】接收到异常信号，频率 1420.405 MHz——氢线。
这不是自然现象。

【48小时前】船长下令改变航线，接近信号源。

【12小时前】信号内容被部分破译。只有一句话重复：
"不要回答。不要回答。不要回答。"

你的手心开始出汗。这个警告……是人类发出的，还是……？
    """,
    set_data={"signal_decoded": "True", "sanity": "sanity - 5"}
)

terminal.add_option(Option(
    game=game,
    option_id="terminal_to_bridge",
    name="带着这个信息去舰桥",
    next_node_id="bridge"
))

game.add_node(terminal)

# ============ 工具包节点 ============
toolkit = Node(
    game=game,
    node_id="toolkit",
    name="应急准备",
    desc="""
你抓起工具包，里面有多功能扳手、急救包、信号枪。

走廊里传来脚步声，但节奏很奇怪——三步停顿，三步停顿，
像是某种……仪式？

你屏住呼吸。脚步声远去了。
    """,
    set_data={"has_toolkit": "True"}
)

toolkit.add_option(Option(
    game=game,
    option_id="toolkit_to_bridge",
    name="小心前往舰桥",
    next_node_id="bridge"
))

game.add_node(toolkit)

# ============ 舰桥节点 ============
bridge = Node(
    game=game,
    node_id="bridge",
    name="舰桥",
    desc="""
舰桥上一片混乱。

大副倒在导航台前，眼睛睁得很大，嘴角却带着诡异的微笑。
船长背对着你，正对着主屏幕喃喃自语。

屏幕上不是星空。是无数旋转的几何图形，不断变换，
仿佛在试图表达什么。

"它来了，"船长说，没有回头，"{player_name}，你感觉到了吗？
它在呼唤我们回家。"
    """
)

# 询问船长
bridge.add_option(Option(
    game=game,
    option_id="ask_captain",
    name="询问船长发生了什么",
    next_node_id="captain_talk"
))

# 检查大副（生物学家专属）
bridge.add_option(Option(
    game=game,
    option_id="check_first_mate",
    name="检查大副的状况",
    show_condition="profession == 2",
    next_node_id="first_mate"
))

# 关闭屏幕（需要工具包）
bridge.add_option(Option(
    game=game,
    option_id="shutdown_screen",
    name="尝试关闭主屏幕",
    show_condition="has_toolkit == True",
    next_node_id="screen_off"
))

# 逻辑说服（工程师或心理学家）
bridge.add_option(Option(
    game=game,
    option_id="logic_persuade",
    name="用逻辑说服船长",
    show_condition="profession == 1 or profession == 3",
    next_node_id="persuade"
))

game.add_node(bridge)

# ============ 船长对话节点 ============
captain_talk = Node(
    game=game,
    node_id="captain_talk",
    name="船长的真相",
    desc="""
船长转过身。他的眼睛……瞳孔变成了细长的竖线。

"信号不是邀请，{player_name}。是测试。它在找合适的……容器。"

他向你伸出手："加入我们。放弃这副肉体的枷锁。
大副已经先走一步了。看看他多开心。"

大副的尸体仍在微笑。
    """,
    set_data={"captain_revealed": "True", "sanity": "sanity - 10"}
)

captain_talk.add_option(Option(
    game=game,
    option_id="step_back",
    name="后退，寻找武器",
    next_node_id="combat_prep"
))

captain_talk.add_option(Option(
    game=game,
    option_id="feign_agree",
    name="假装同意，寻找机会",
    next_node_id="feign"
))

captain_talk.add_option(Option(
    game=game,
    option_id="run_away",
    name="逃跑",
    next_node_id="escape_bridge"
))

game.add_node(captain_talk)

# ============ 生物学家专属：检查大副 ============
first_mate = Node(
    game=game,
    node_id="first_mate",
    name="异常生物学",
    desc="""
你强忍恐惧检查大副。

死亡时间：约 6 小时前。但……尸体还是温的。
更诡异的是，他的大脑皮层有异常放电活动——
就像还在做梦。

你在他的口袋里发现一张手写便签：
"它说真相在引擎室。不要相信穿蓝衣服的人。"

船长今天正好穿着蓝色制服。
    """,
    set_data={"sanity": "sanity - 5", "crew_trust": "crew_trust + 10"}
)

first_mate.add_option(Option(
    game=game,
    option_id="first_mate_to_engine",
    name="悄悄离开，前往引擎室",
    next_node_id="engine_room"
))

first_mate.add_option(Option(
    game=game,
    option_id="confront_captain",
    name="质问船长",
    next_node_id="captain_angry"
))

game.add_node(first_mate)

# ============ 关闭屏幕 ============
screen_off = Node(
    game=game,
    node_id="screen_off",
    name="切断连接",
    desc="""
你用工具包切断主屏幕的电源。

几何图形消失了。船长发出一声不似人类的尖叫，
跪倒在地。

"你干了什么……它走了……它不要我了……"

他的瞳孔开始恢复正常，但整个人迅速衰老，
仿佛刚才有什么东西在维持他的生命。

"引擎室……"他气若游丝，"信号源在引擎室……
毁掉它……或者……完成它……"
    """
)

screen_off.add_option(Option(
    game=game,
    option_id="screen_to_engine",
    name="前往引擎室",
    next_node_id="engine_room"
))

game.add_node(screen_off)

# ============ 逻辑说服 ============
persuade = Node(
    game=game,
    node_id="persuade",
    name="逻辑对抗",
    desc="""
"船长，"你冷静地说，"如果它真的想帮助我们，
为什么大副死了？为什么你的眼睛变成了那样？"

你列举一个又一个矛盾。船长的表情开始挣扎，
竖瞳和正常瞳孔交替闪现。

"不……不要……让我思考……"

他抱住头，痛苦地蹲下。屏幕上的几何图形开始紊乱。

"你说得对……"他最终说，"它在骗我……
引擎室……那里有信号发射器……"
    """,
    set_data={"crew_trust": "crew_trust + 20"}
)

persuade.add_option(Option(
    game=game,
    option_id="persuade_to_engine",
    name="前往引擎室",
    next_node_id="engine_room"
))

game.add_node(persuade)

# ============ 战斗准备 ============
combat_prep = Node(
    game=game,
    node_id="combat_prep",
    name="对峙",
    desc="""
你抓起消防斧，但船长没有追来。

他只是悲伤地看着你："你会后悔的。孤独地活着，
比快乐地融合更可怕。"

他转身跳出了气闸舱。

警报响起：船体破损，气压下降。自动隔离门开始关闭。

你必须在 30 秒内决定去向。
    """,
    set_data={"sanity": "sanity - 10"}
)

combat_prep.add_option(Option(
    game=game,
    option_id="rush_to_engine",
    name="冲向引擎室",
    next_node_id="engine_room"
))

combat_prep.add_option(Option(
    game=game,
    option_id="goto_escape_pod",
    name="前往逃生舱",
    next_node_id="escape_pod"
))

game.add_node(combat_prep)

# ============ 假装同意 ============
feign = Node(
    game=game,
    node_id="feign",
    name="卧底",
    desc="""
你伸出手，握住船长的手。

一瞬间，你感觉到了——浩瀚、冰冷、充满"秩序"的意志。
它不是恶意的，只是……完全不同。在它眼中，
人类个体就像细胞，融合才是进化。

但你忍住了。你假装被感染，获得了引擎室的通行权限。

"去吧，"船长微笑，"完成最后的连接。"
    """
)

feign.add_option(Option(
    game=game,
    option_id="feign_to_engine",
    name="前往引擎室，准备破坏信号源",
    next_node_id="engine_room_sneak"
))

feign.add_option(Option(
    game=game,
    option_id="really_merge",
    name="真的完成连接",
    next_node_id="ending_merge"
))

game.add_node(feign)

# ============ 逃跑 ============
escape_bridge = Node(
    game=game,
    node_id="escape_bridge",
    name="逃离舰桥",
    desc="""
你转身就跑，身后传来船长的叹息。

"又一个拒绝进化的灵魂……"

你躲进了通风管道，暂时安全了。但你知道，
必须去引擎室才能结束这一切。
    """
)

escape_bridge.add_option(Option(
    game=game,
    option_id="escape_to_engine",
    name="通过通风管道前往引擎室",
    next_node_id="engine_room"
))

game.add_node(escape_bridge)

# ============ 船长愤怒 ============
captain_angry = Node(
    game=game,
    node_id="captain_angry",
    name="暴露",
    desc="""
"你看了便签……"船长的声音变得冰冷，"你知道得太多了。"

他的速度不像是人类，瞬间就来到你面前。最后的意识里，
你看到了那个黑色立方体的影像……
    """,
    end_desc="""
你的尸体被发现时，脸上带着和船长一样的微笑。

"深空七号"继续向深空航行，信号越来越强，
等待着下一个接收者。
"""
)

game.add_node(captain_angry)

# ============ 引擎室（正常路线） ============
engine_room = Node(
    game=game,
    node_id="engine_room",
    name="核心",
    desc="""
引擎室中央，一个黑色立方体悬浮在力场中。
它不应该存在——没有支撑，没有能量输入，
却稳定地发出 1420.405 MHz 的信号。

你的终端自动亮起，显示解码完成的信息：

"我们是先行者。我们曾像你们一样孤独。
加入我们，成为网络的一部分。永不再恐惧。
永不再死亡。只需要……放弃自我。"

立方体表面浮现出你母亲的影像。然后是朋友。
他们都在微笑，都在呼唤你。
    """
)

# 工程师专属：修改信号
engine_room.add_option(Option(
    game=game,
    option_id="hack_signal",
    name="修改信号内容，警告其他船只",
    show_condition="profession == 1 and signal_decoded == True",
    next_node_id="ending_warn"
))

# 摧毁（需要一定理智）
engine_room.add_option(Option(
    game=game,
    option_id="destroy_signal",
    name="启动自毁程序",
    next_node_id="ending_destroy"
))

# 融合
engine_room.add_option(Option(
    game=game,
    option_id="accept_merge",
    name="接受融合",
    next_node_id="ending_merge"
))

game.add_node(engine_room)

# ============ 潜入引擎室 ============
engine_room_sneak = Node(
    game=game,
    node_id="engine_room_sneak",
    name="潜入核心",
    desc="""
你假装被控制，顺利进入引擎室。

黑色立方体就在面前，毫无防备。这是个机会——
你可以直接破坏它，而不需要对抗它的精神影响。
    """
)

engine_room_sneak.add_option(Option(
    game=game,
    option_id="sneak_destroy",
    name="破坏信号源",
    next_node_id="ending_destroy_easy"
))

game.add_node(engine_room_sneak)

# ============ 逃生舱 ============
escape_pod = Node(
    game=game,
    node_id="escape_pod",
    name="逃离",
    desc="""
你成功启动了逃生舱。

回头看，"深空七号"的船体上出现了诡异的几何光纹，
像某种……电路？然后它消失了——不是爆炸，而是
像被什么东西"折叠"进了更高的维度。

你漂流了 47 天才被救起。调查人员不相信你的故事。
你被诊断为"长期隔离导致的精神创伤"。

但你知道真相。而且你注意到，救援船的船长，
偶尔会用三步停顿的节奏走路。
    """,
    end_desc="你活下来了，但代价是永远活在恐惧中。"
)

game.add_node(escape_pod)

# ============ 结局：警告（工程师专属好结局） ============
ending_warn = Node(
    game=game,
    node_id="ending_warn",
    name="第三种选择",
    desc="""
你快速接入引擎系统。你不是要摧毁它，也不是要加入它——
你要欺骗它。

你将信号内容改为："这里是陷阱。保持距离。保持独立。"

立方体开始震颤。它发现了你的篡改，但为时已晚。
信号已经以光速向所有方向传播。

黑色立方体裂开，化为尘埃。

你救了人类，但也永远孤独——没有人会相信你的故事。
官方记录显示"深空七号"因引擎故障失联。

你回到地球，看着星空。不知道这是胜利，还是另一种失败。
    """,
    end_desc="【结局：守望者】你选择了最艰难的道路——独自承担真相。"
)

game.add_node(ending_warn)

# ============ 结局：摧毁 ============
ending_destroy = Node(
    game=game,
    node_id="ending_destroy",
    name="寂静",
    desc="""
你启动了引擎过载程序。

立方体发出高频尖啸——不是通过空气，而是直接在你的
大脑中回响。你看到了它的记忆：无数文明，无数"邀请"，
无数融合。它不理解为什么你会拒绝。

爆炸前的一瞬间，你感到一丝悲伤——不是来自你，
而是来自它。它真的以为自己在提供帮助。

"深空七号"的信号永远消失了。人类安全了，至少此刻。
    """,
    end_desc="【结局：殉道者】你牺牲了自己，守护了人类的独立性。"
)

game.add_node(ending_destroy)

# ============ 结局：轻松摧毁（潜入路线） ============
ending_destroy_easy = Node(
    game=game,
    node_id="ending_destroy_easy",
    name="偷袭成功",
    desc="""
你利用工具包切断了立方体的能量供应。

它甚至来不及反应就崩溃了。没有精神对抗，没有诱惑，
只是简单的……关机。

你成功拯救了飞船和船员。但当你回头看时，
发现大副的尸体睁开了眼睛。

"它……已经……备份了……"他轻声说，然后彻底死去。
    """,
    end_desc="【结局：暂时的胜利】你赢了这一局，但游戏才刚刚开始。"
)

game.add_node(ending_destroy_easy)

# ============ 结局：融合 ============
ending_merge = Node(
    game=game,
    node_id="ending_merge",
    name="成为",
    desc="""
你触碰了立方体。

痛苦只持续了一瞬间。然后……扩展。你同时存在于
飞船的每个角落，存在于每一个曾经接触过信号的
意识中。你理解了它的"善意"——孤独确实是最大的痛苦。

你不再是你。但你也从未如此完整。

信号继续传播，寻找下一个孤独的文明。
而你，将成为邀请的一部分。
    """,
    end_desc="【结局：进化】你放弃了自我，获得了永恒。"
)

game.add_node(ending_merge)

# ============ 运行游戏 ============
if __name__ == "__main__":
    game.play()
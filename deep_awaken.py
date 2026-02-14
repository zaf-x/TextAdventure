from TextAdventure import Game, Node, Option

# ==================== 游戏配置 ====================

game = Game(
    start_node_id="start",
    game_name="深空觉醒",
    init_input=[
        {
            "prompt": "输入船员编号：",
            "name": "player_id",
            "converter": "str",
            "condition": "len(val) > 0",
            "err_desc": "编号不能为空"
        },
        {
            "prompt": "选择专业（1-安全官 2-工程师 3-生物学家）：",
            "name": "profession",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "请输入 1、2 或 3"
        }
    ]
)

# ==================== 初始节点 ====================

start = Node(
    game=game,
    node_id="start",
    name="冷冻舱",
    desc="""
舱门滑开，冷凝雾气涌出。你睁开眼睛，头痛欲裂。

【深空采矿站 "普罗米修斯"】
【船员编号：{player_id}】
【专业：{profession_name}】
【状态：从冷冻休眠中强制唤醒】

警报灯在走廊尽头闪烁红光。广播系统断断续续：

"...全体船员...协议启动...未知生物...封锁..."

你一个人。冷冻舱其他位置空空如也——其他船员要么已经撤离，要么...

{profession_hint}

【系统】氧气：{oxygen}% | 理智：{sanity}% | 感染：{infection}%
    """.strip(),
    init_data={
        "oxygen": "100",
        "sanity": "100", 
        "infection": "0",
        "has_weapon": "False",
        "has_tools": "False",
        "has_sample": "False",
        "know_truth": "False",
        "escaped": "False",
        "profession_name": "'未设置'",
        "profession_hint": "' '",
        "temp_hint": "' '"
    },
    on_load="""
if profession == 1:
    data['profession_name'] = '安全官'
    data['profession_hint'] = '【安全官训练】你注意到舱门有暴力破坏的痕迹，不是系统故障...'
elif profession == 2:
    data['profession_name'] = '工程师'
    data['profession_hint'] = '【工程知识】警报系统被人为修改过，这不是意外事故...'
else:
    data['profession_name'] = '生物学家'
    data['profession_hint'] = '【生物直觉】空气中有一种奇怪的气味，像...腐烂的海藻混合着臭氧...'
    """
)

# 选项
opt_corridor = Option(game, option_id="to_corridor", name="进入走廊", desc="查看警报来源", next_node_id="corridor")
opt_locker = Option(game, option_id="check_locker", name="检查储物柜", desc="寻找装备", next_node_id="locker")
opt_terminal = Option(game, option_id="check_terminal", name="查看终端", desc="读取航行日志", next_node_id="terminal")

start.add_option(opt_corridor)
start.add_option(opt_locker)
start.add_option(opt_terminal)
game.add_node(start)

# ==================== 储物柜 ====================

locker = Node(
    game=game,
    node_id="locker",
    name="装备室",
    desc="""
金属柜门半开着，里面一片狼藉。

你找到了：
- 便携式氧气瓶（已装备）
- {locker_item}

【系统】氧气已补充至100%
    """,
    init_data={"locker_item": "'基础补给包'"},
    set_data={"oxygen": "100"},
    on_load="""
if profession == 1:
    data['has_weapon'] = True
    data['locker_item'] = '等离子切割枪（安全官专属武器）'
elif profession == 2:
    data['has_tools'] = True
    data['locker_item'] = '工程工具包（可修复系统或制作武器）'
else:
    data['has_sample'] = True
    data['locker_item'] = '生物采样器（可分析未知物质）'
    """
)

locker.add_option(Option(game, option_id="back_to_start", name="返回冷冻舱", next_node_id="start"))
locker.add_option(Option(game, option_id="locker_to_corridor", name="前往走廊", next_node_id="corridor"))
game.add_node(locker)

# ==================== 终端 ====================

terminal = Node(
    game=game,
    node_id="terminal",
    name="舰桥终端",
    desc="""
屏幕闪烁，你调出了最后的日志记录：

【船长日志 - 最后条目】
"...我们在小行星带发现了某种...结构体。不是自然的。
它...在呼唤我们。戴维斯博士坚持要带回样本。
现在样本舱封锁了，博士说他在'与它交流'。
我不信任那个东西。我已经启动了紧急冷冻协议——"

日志中断。最后的时间戳是72小时前。

{terminal_extra}
    """,
    init_data={"terminal_extra": "' '"},
    on_load="""
if profession == 2:
    data['terminal_extra'] = '【工程师专长】你发现冷冻协议被人为中断，有人故意唤醒了你...'
    data['know_truth'] = True
else:
    data['terminal_extra'] = '【系统】数据损坏，无法恢复更多信息'
    """
)

terminal.add_option(Option(game, option_id="terminal_back", name="返回冷冻舱", next_node_id="start"))
terminal.add_option(Option(game, option_id="terminal_to_corridor", name="前往走廊", next_node_id="corridor"))
game.add_node(terminal)

# ==================== 走廊 ====================

corridor = Node(
    game=game,
    node_id="corridor",
    name="主走廊",
    desc="""
走廊灯光忽明忽暗。墙壁上有...抓痕？不，是腐蚀痕迹，金属像蜡烛一样融化。

远处传来声音——像是某种湿滑的拖曳声。

左侧：样本舱（封锁状态，红灯闪烁）
右侧：逃生舱（需要授权代码）
前方：引擎室（氧气泄漏警告）

{corridor_hint}
    """,
    init_data={"corridor_hint": "' '"},
    on_load="""
if profession == 3 and has_sample:
    data['corridor_hint'] = '【生物采样器报警】空气中的有机成分...不是地球生命。DNA序列在不断变化。'
    data['infection'] = infection + 5
else:
    data['corridor_hint'] = '【系统】环境扫描完成，发现微量有机污染物'
    data['infection'] = infection + 10
    """
)

opt_sample = Option(
    game=game, 
    option_id="to_sample", 
    name="前往样本舱", 
    desc="调查源头",
    next_node_id="sample_room",
    move_condition="has_weapon or has_tools",
    cant_move_desc="太危险了，没有武器或工具不能贸然进入"
)

opt_escape = Option(
    game=game,
    option_id="to_escape",
    name="前往逃生舱",
    desc="放弃调查，优先求生",
    next_node_id="escape_pod",
    move_condition="know_truth or profession == 1",
    cant_move_desc="你不知道发生了什么，不能就这样逃跑。需要更多信息。"
)

opt_engine = Option(game, option_id="to_engine", name="前往引擎室", desc="修复氧气系统", next_node_id="engine_room")

corridor.add_option(opt_sample)
corridor.add_option(opt_escape)
corridor.add_option(opt_engine)
game.add_node(corridor)

# ==================== 引擎室 ====================

engine_room = Node(
    game=game,
    node_id="engine_room",
    name="引擎核心",
    desc="""
这里更糟。氧气管道破裂，低温气体喷涌。

墙壁上有更多的腐蚀痕迹...而且，你听到了——
那种湿滑的拖曳声，就在管道后面。

控制台显示：【反应堆不稳定 - 建议立即撤离】

{engine_option}
    """,
    init_data={"engine_option": "' '"},
    on_load="""
if profession == 2 and has_tools:
    data['engine_option'] = '【工程师专长】你有工具，可以尝试修复系统建立封锁，或者启动自毁程序。'
elif profession == 2:
    data['engine_option'] = '【工程师专长】你能看懂系统，但没有工具无法操作。需要返回储物柜获取工具。'
else:
    data['engine_option'] = '【系统警告】检测到危险能量反应，建议立即撤离'
    """
)

opt_fix = Option(
    game=game,
    option_id="fix_system",
    name="尝试修复系统",
    desc="稳定反应堆，建立封锁",
    next_node_id="engine_battle",
    move_condition="has_tools",
    cant_move_desc="没有工程工具，你无法操作控制台。先去储物柜获取装备。"
)

opt_destroy = Option(
    game=game,
    option_id="self_destruct",
    name="启动紧急自毁",
    desc="与敌人同归于尽",
    next_node_id="sacrifice_ending",
    move_condition="profession == 2"
)

opt_leave_engine = Option(game, option_id="leave_engine", name="离开", desc="返回走廊", next_node_id="corridor")

engine_room.add_option(opt_fix)
engine_room.add_option(opt_destroy)
engine_room.add_option(opt_leave_engine)
game.add_node(engine_room)

# ==================== 引擎室战斗 ====================

engine_battle = Node(
    game=game,
    node_id="engine_battle",
    name="阴影中的接触",
    desc="""
你开始操作控制台，手指在键盘上飞舞。

突然，管道破裂！一团...东西...喷涌而出。不是气体，是有机质，像活物一样蠕动。

它向你扑来！
    """,
    defaults=[
        {"condition": "profession == 2 and has_tools", "node_id": "engine_success"},
        {"condition": "True", "node_id": "engine_fail"}
    ]
)

game.add_node(engine_battle)

# ==================== 引擎室成功 ====================

engine_success = Node(
    game=game,
    node_id="engine_success",
    name="封锁完成",
    desc="""
你抓起等离子焊枪（工具包里的），将那团有机质逼退。

同时，你的另一只手没有停止操作——

【防火墙启动】
【样本舱封锁 - 完成】
【生命维持系统 - 转为抑制模式】

那东西尖叫，不是声音，是直接在脑海中的尖啸。但它被困住了，被能量场锁在样本舱。

你瘫坐在地上，喘着气。你赢了，但只是暂时的。

现在你有两个选择：
    """,
    on_load="data['know_truth'] = True"
)

opt_stay = Option(game, option_id="stay_guard", name="留下看守", desc="建立哨站，监测威胁", next_node_id="fix_ending")
opt_leave_now = Option(game, option_id="leave_now", name="坐逃生舱离开", desc="警告已发出，任务完成", next_node_id="escape_pod")

engine_success.add_option(opt_stay)
engine_success.add_option(opt_leave_now)
game.add_node(engine_success)

# ==================== 引擎室失败 ====================

engine_fail = Node(
    game=game,
    node_id="engine_fail",
    name="失控",
    desc="""
你没有工具，只能用双手对抗那团有机质。

它缠上了你的手臂，冰冷、湿滑，然后...温暖？不，是灼烧感。它在试图进入你。

你挣扎着按下了紧急按钮——不是修复，是自毁。

"一起死吧。"

【结局：失控】
你没能修复系统，但至少阻止了它扩散。采矿站的残骸将飘向深空，远离地球。
    """,
    end_desc="结局：失控 | 悲剧英雄 | 你失败了，但阻止了更大的灾难。"
)
game.add_node(engine_fail)

# ==================== 样本舱 ====================

sample_room = Node(
    game=game,
    node_id="sample_room",
    name="样本舱",
    desc="""
舱门在你身后锁死。

这里...曾经是实验室。现在是一座生物殿堂。

墙壁覆盖着脉动的肉质膜，发出幽蓝生物光。中央的培养舱破裂了，某种...东西...曾经在里面。

你看到了戴维斯博士。或者说，曾经是博士的东西。他悬浮在舱室中央，身体与肉质膜融合，数十条神经索连接着他的脊椎。

他的眼睛突然睁开——全是黑色，没有眼白。

"{player_id}..."他的声音像是从深海传来，"你终于来了。我们等你很久了。加入我们...终结孤独..."

{sample_reaction}

【系统】理智：{sanity}% | 感染：{infection}%
    """,
    init_data={
        "sample_reaction": "' '",
        "temp_sanity": "0",
        "temp_infection": "0"
    },
    set_data={
        "sanity": "sanity - 30",
        "infection": "infection + 20"
    },
    on_load="""
# 必须先通过 data 对象读写
if profession == 3:
    data['sample_reaction'] = '【生物学家洞察】这不是感染...是共生。它在提供永生，但代价是...失去个体意识。'
    data['temp_sanity'] = 10  # 生物学家理解更多，失去较少理智
else:
    data['sample_reaction'] = '【精神冲击】你的世界观在崩塌...'
    data['temp_sanity'] = -30

# 重新计算 - 使用 data 对象
data['sanity'] = sanity + data['temp_sanity']
    """,
    defaults=[
        {"condition": "profession == 3 and has_sample", "node_id": "biologist_ending"},
        {"condition": "has_weapon", "node_id": "fight_alien"},
        {"condition": "True", "node_id": "assimilated"}
    ]
)

game.add_node(sample_room)

# ==================== 生物学家专属结局 ====================

biologist_ending = Node(
    game=game,
    node_id="biologist_ending",
    name="进化之路",
    desc="""
你举起采样器，不是攻击，而是...调整频率。

"我理解你，"你说，"你是孤独的旅行者，寻找同伴。但强制融合不是答案。"

博士/它的表情变化了。好奇？

你继续："我可以帮你。真正的共生，不是吞噬，而是...合作。让我成为桥梁，而不是宿主。"

漫长的沉默。然后，神经索缓缓收回。博士的身体落下，昏迷但活着。

肉质膜开始收缩，凝聚成一个...胚胎？一个种子。

你捧着它，感受到了无限的知识——星际地图，失落的技术，还有...其他数百万个正在等待的"旅行者"。

【真结局：进化之路】
你建立了人类与星际生命的第一次真正接触。不是征服，不是屈服，而是理解。地球将永远改变，但你确保了人类的主体性。

种子在你手中脉动，像是一颗小小的心脏。
    """,
    end_desc="结局：进化之路 | 星际大使 | 你以科学和同理心开启了新纪元。"
)
game.add_node(biologist_ending)

# ==================== 战斗结局 ====================

fight_alien = Node(
    game=game,
    node_id="fight_alien",
    name="净化之火",
    desc="""
你举起武器。

"抱歉，博士。但你已经不是人类了。"

等离子束撕裂了肉质膜。尖叫——不是声音，是直接在脑海中响起的痛苦尖啸。

博士的身体抽搐，那些神经索疯狂舞动。你持续射击，直到...

爆炸。你设置了过载，整个舱室将化为火海。

你转身奔跑，在气闸关闭前的最后一秒逃出。身后，样本舱被真空和火焰净化。

【结局：净化之火】
你消灭了威胁，但也消灭了理解它的机会。当你被救援队找到时，你只说了一句话："烧掉一切。"

采矿站被遗弃，小行星带被划为禁区。但你知道...宇宙中还有更多的"旅行者"。
    """,
    end_desc="结局：净化之火 | 幸存者 | 你付出了代价，但保护了人类。"
)
game.add_node(fight_alien)

# ==================== 同化结局 ====================

assimilated = Node(
    game=game,
    node_id="assimilated",
    name="大融合",
    desc="""
你没有武器。

神经索缠上你的四肢，不痛苦...出乎意料地温暖。你的记忆开始流淌——童年、训练、这次任务——全部汇入某个更大的意识。

你看到了宇宙的真相：恒星诞生与死亡，文明的兴衰，无尽的黑暗与光。

"不再孤独..."你听见自己说，也听见千万个声音同时说。

你的身体融入肉质膜，成为圣殿的一部分。但在最后一刻，你保留了一丝...自我。一个观察者，见证着永恒。

【结局：大融合】
你失去了个体，但获得了无限。在这深空中，一个新的节点诞生了，等待下一个来访者。

也许有一天，你会再次醒来。作为"我们"的一部分。
    """,
    end_desc="结局：大融合 | 新节点 | 个体终结，意识延续。"
)
game.add_node(assimilated)

# ==================== 修复结局（守望者）====================

fix_ending = Node(
    game=game,
    node_id="fix_ending",
    name="守望者",
    desc="""
你将采矿站改造成了...监狱。样本舱被永久封锁，生命维持系统转为抑制模式，将那个东西困在永恒的休眠中。

然后你发送了信号。不是求救，是警告。

【深空哨站 "普罗米修斯" 已建立】
【威胁等级：最高】
【守望者：{player_id}】

你留了下来。十年？二十年？在冷冻舱的间歇清醒中，你监测着那个牢笼。

有时候，你能感觉到它在梦中与你对话。诱惑你。但你拒绝。

"不，"你说，"这是我们的星空。你找错宿主了。"

【真结局：守望者】
你牺牲了自己的岁月，确保了威胁不会扩散。直到有一天，真正的解决方案会被找到。在那之前，你是人类的边疆。
    """,
    end_desc="结局：守望者 | 孤独卫士 | 你以时间换取了安全。"
)
game.add_node(fix_ending)

# ==================== 牺牲结局 ====================

sacrifice_ending = Node(
    game=game,
    node_id="sacrifice_ending",
    name="超新星",
    desc="""
倒计时：60秒。

你没有逃跑。你坐在引擎核心旁，看着读数攀升。

"来吧，"你说，"看看谁更亮。"

爆炸没有声音，只有光。采矿站、样本、那个东西...全部化为基本粒子。

地球收到了最后信号：【威胁已清除 - 船员 {player_id} 签署】

你的原子现在飘散在小行星带，与星光混合。有时候，经过的飞船会报告看到奇怪的极光...像是一个微笑。

【结局：超新星】
你选择了最壮烈的方式。没有痛苦，只有一瞬间的辉煌。人类不会知道你的名字，但他们安全了。
    """,
    end_desc="结局：超新星 | 殉道者 | 你成为了星光。"
)
game.add_node(sacrifice_ending)

# ==================== 逃生舱 ====================

escape_pod = Node(
    game=game,
    node_id="escape_pod",
    name="逃生舱",
    desc="""
舱门打开，狭小的空间，足够的燃料到达最近的航道。

但你知道了真相。如果你逃跑，那个东西会继续生长。也许几年，也许几十年，但它会找到方法到达地球。

{escape_dilemma}
    """,
    init_data={"escape_dilemma": "' '"},
    on_load="""
if know_truth:
    data['escape_dilemma'] = '【知识即是重负】你知道太多，不能就这样离开。但活下去...也很重要。'
else:
    data['escape_dilemma'] = '【本能求生】警报在尖叫，你的本能催促你离开这个鬼地方。'
    """
)

opt_launch = Option(game, option_id="launch_pod", name="发射逃生舱", desc="逃离采矿站", next_node_id="coward_ending")
opt_return = Option(game, option_id="return_fight", name="返回战斗", desc="不能就这样逃跑", next_node_id="corridor")

escape_pod.add_option(opt_launch)
escape_pod.add_option(opt_return)
game.add_node(escape_pod)

# ==================== 懦夫结局 ====================

coward_ending = Node(
    game=game,
    node_id="coward_ending",
    name="归乡者",
    desc="""
逃生舱发射，采矿站在视野中缩小成一颗星星，然后消失。

你被救了。三个月后，你站在听证会上，讲述你的故事。

"...我不知道那是什么，"你说，"我只是...想活下去。"

他们没有责怪你。但有时候，在深夜，你会从梦中惊醒，听到那个声音：

"{player_id}...我们还在等你..."

三年后，深空望远镜发现"普罗米修斯"消失了。不是爆炸，是...离开。像种子一样，飘向地球。

你的余生都在等待。等待敲门声。

【结局：归乡者】
你活了下来，但永远不知道是否正确。也许有一天，你会再次见到你的"朋友"。
    """,
    end_desc="结局：归乡者 | 幸存者 | 你选择了生命，但背负了疑问。"
)
game.add_node(coward_ending)

# ==================== 运行 ====================

if __name__ == "__main__":
    game.play()
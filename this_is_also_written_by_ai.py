from TextAdventure import Node, Option, Game, Data, IOHandler

# 创建游戏实例
game = Game(
    start_node_id="camp",
    game_name="黄金城之谜：亚马逊惊魂",
    init_input=[
        {
            "prompt": "选择你的身份 [1]考古学家 [2]探险向导 [3]野外摄影师: ",
            "name": "player_class",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "请输入1、2或3"
        },
        {
            "prompt": "你的名字: ",
            "name": "player_name",
            "converter": "str",
            "condition": "2 <= len(val) <= 20",
            "err_desc": "名字长度2-20个字符"
        }
    ]
)

# ========== 节点定义 ==========

# 营地起点
camp = Node(
    game=game,
    node_id="camp",
    name="第一章：丛林深处的营地",
    desc='''亚马逊雨林，厄瓜多尔边境。

你站在临时营地中央，潮湿的空气弥漫着腐殖质和野花的混合气味。三天前，你在利马的古董市场发现了一张羊皮纸——十六世纪传教士的手绘地图，标记着"埃尔多拉多"的真正位置。

现在，你——{player_name}，作为一名{player_class_name}，终于抵达了地图指示的区域。

你的背包里只有基础装备：水壶、指南针、三天份口粮。帐篷外，丛林发出古老的低语，鹦鹉的尖叫划破天际，远处传来瀑布的轰鸣。

向导佩德罗昨天因为高烧撤退了，留下你独自面对这片绿色地狱。但羊皮纸上那段警告文字让你犹豫：

"唯有心灵纯净者，方能触及太阳之金；贪婪者，将永远成为丛林的养料。"

天色尚早，阳光透过树冠斑驳洒落。你必须选择前进的路线。''',
    init_data={
        "player_class_name": "'考古学家' if player_class == 1 else ('探险向导' if player_class == 2 else '野外摄影师')",
        "stamina": "80 if player_class == 2 else 100",
        "wisdom": "2 if player_class == 1 else (1 if player_class == 3 else 0)",
        "courage": "1 if player_class == 2 else (2 if player_class == 3 else 1)",
        "has_machete": "True if player_class == 2 else False",
        "has_camera": "True if player_class == 3 else False",
        "has_journal": "True if player_class == 1 else False",
        "has_rope": "False",
        "has_talisman": "False",
        "found_temple": "False",
        "knows_ritual": "False",
        "golden_idol": "False",
        "translation_notes": "0"
    }
)

# 密林小径
jungle_path = Node(
    game=game,
    node_id="jungle_path",
    name="密林深处",
    desc='''你选择穿越茂密的丛林，直插地图标记的核心区域。

砍刀劈开藤蔓（如果你没有砍刀，手掌被刺藤划得鲜血淋漓），每一步都要对抗纠缠的树根。这里的树木高达五十米，树冠密不透风，光线昏暗如同黄昏。

突然，你听到灌木丛中的响动。

一条翡翠色的森蚺盘绕在前方的树枝上，体型巨大，眼睛像两颗黑曜石般盯着你。它挡住了去路，而绕行意味着要穿越一片布满毒箭蛙的沼泽。

就在这时，你注意到树下的泥土里露出半截石像——是前哥伦比亚时期的风格，手持长矛的战士像，但面部被刻意磨损了。

石像底座刻着一行古老的奇布查语："尊敬森林者，得通行；破坏者，为肥料。"

蛇信吞吐，发出威胁的嘶嘶声。''',
    set_data={
        "stamina": "stamina - 10",
        "translation_notes": "translation_notes + 1 if has_journal else translation_notes"
    }
)

# 河流路线
river_path = Node(
    game=game,
    node_id="river_path",
    name="亚马逊支流",
    desc='''你决定沿着河流前进，水声是丛林中最好的向导。

河岸泥泞，巨树的板根像城墙般耸立。彩色的金刚鹦鹉在头顶飞过，一只树懒缓慢地眨着眼睛。这景象美得令人窒息，如果不是脚下的危险的话。

河流在这里形成一个急弯，水面下隐约可见尖锐的岩石。要继续前进，你必须：
- 涉水过河（节省体力但危险）
- 砍伐竹子做筏（安全但耗时）

正当你犹豫时，水面泛起涟漪。一双琥珀色的眼睛浮上水面——是黑凯门鳄，亚马逊的顶级掠食者，体长超过四米。

更糟的是，你注意到对岸的泥地上有新鲜的脚印，不是人类的，而是某种大型猫科动物，爪印 retracted（收起），说明是美洲豹，而且不久前刚经过这里。

你被困在了河中间的位置。''',
    set_data={
        "stamina": "stamina - 5"
    }
)

# 悬崖攀登
cliff_path = Node(
    game=game,
    node_id="cliff_path",
    name="花岗岩峭壁",
    desc='''你选择攀爬侧面的悬崖，从高处俯瞰寻找神庙位置。

岩壁潮湿长满苔藓，每一步都需要极度小心。你的手指抠进岩缝，肌肉颤抖，汗水流进眼睛刺痛难忍。高度让你头晕——脚下三十米就是嶙峋的岩石。

但高处的视野确实不同。透过望远镜（如果你有望远镜的话），你看到了丛林树冠中异常的几何形状——那是人工建筑！金字塔的顶端从绿色海洋中刺出，覆盖着金色涂料，在阳光下闪烁。

然而，你上方传来尖利的啸叫。一只角雕，翼展两米的雨林之王，正在巢穴旁警惕地注视着你。它把你当成了威胁幼鸟的入侵者。

更糟的是，岩壁上你发现了一些人工凿刻的凹坑——是古代的攀登路径，但年代久远，有些已经风化松动。

风在耳边呼啸，角雕俯冲而下！''',
    set_data={
        "stamina": "stamina - 20",
        "found_temple": "True"
    }
)

# 神庙大门
temple_gate = Node(
    game=game,
    node_id="temple_gate",
    name="遗忘的神庙",
    desc='''你终于站在了神庙前。

这不是普通的建筑，而是一座阶梯金字塔，高达百米，完全由黑色玄武岩砌成，表面覆盖着精美的浮雕，讲述着一个关于星辰和祭祀的故事。金字塔顶端有一座金色屋顶的神殿，那便是传说中的太阳神殿。

大门由两扇巨石组成，中央是一个圆盘机关，分成十二个扇区，每个扇区刻着不同的星座符号——但这不是现代的星座，而是南半球特有的星空图案。

门旁立着两尊雕像，不是战士，而是美洲豹人身的神兽，眼睛镶嵌着祖母绿宝石，在阴影中发出幽光。

你注意到地面上散落着一些现代物品：生锈的指南针，破烂的帆布背包，还有一本被雨水浸泡的笔记本——是之前探险队留下的。

笔记本最后一页潦草地写着："不要碰黄金！那不是财富，是囚牢！祭司们把意识封存在金属里，等待...（字迹中断）"

机关圆盘等待着你的操作。''',
    set_data={
        "stamina": "stamina - 5",
        "found_temple": "True"
    }
)

# 主殿
main_hall = Node(
    game=game,
    node_id="main_hall",
    name="太阳神殿",
    desc='''巨石在你身后轰然关闭，将你困在神庙内部。

主殿宏伟得令人窒息。穹顶是开放的，阳光直射进来，在特定角度会形成一道光柱——现在正是正午，光柱照射在房间中央的石台上。

石台上摆放着一个水晶头骨，不是恐怖故事里那种，而是精密的光学仪器，将阳光折射成七彩光谱，投射在四周墙壁上。那些光谱照亮的壁画讲述了黄金城的真相：

这不是一座城市，而是一个文明的知识库。古人将他们的智慧、历史、天文学和医学知识编码在黄金制品中，使用某种量子记忆技术。触碰黄金，就能获取知识，但代价是意识会被部分复制到黄金中。

墙壁上有三个通道：
- 左侧：通往"黄金之室"，堆满金器的密室
- 右侧：通往"观星台"，记载天文知识的房间
- 中央：通往"祭祀井"，深不见底的竖井，据说通往地下河

水晶头骨突然发出嗡鸣，似乎在警告你什么。''',
    set_data={
        "knows_ritual": "True"
    }
)

# 黄金之室
treasury = Node(
    game=game,
    node_id="treasury",
    name="黄金之室",
    desc='''你进入了传说中的黄金之室，探险家的终极梦想。

这里堆满了黄金制品——面具、雕像、器皿、珠宝，在黑暗中散发着柔和的光芒。但诡异的是，它们似乎... 在呼吸。金器表面有规律的脉动，像是金属制成的心脏。

最中央是一座黄金太阳神像，高约三米，双眼镶嵌着两颗巨大的红宝石。神像手中捧着一个完美的黄金球体，表面刻满了微观的文字和图案。

当你靠近时，脑海中突然涌入画面：古老的祭司，星夜的祭祀，知识的传承。你明白了——这些黄金是存储器，存储着整个文明的记忆。

触碰黄金球，你将获得人类失落的知识，医学、天文学、哲学... 但你的意识也会被复制，成为黄金网络的一部分，永远困在这里，作为"守护者"存在。

墙壁上的铭文警告："取一金，留一魂。"

你注意到地上有几具干尸，穿着二十世纪探险服，他们的手都触碰着金器，脸上带着诡异的微笑，仿佛死前看到了极乐世界。''',
    set_data={
        "golden_idol": "True",
        "courage": "courage - 1"
    }
)

# 观星台
observatory = Node(
    game=game,
    node_id="observatory",
    name="古代观星台",
    desc='''这里不是简单的天文台，而是一个信息解码中心。

墙壁上刻满了精确的星图，记录了三千年前的星空。中央是一个复杂的齿轮装置，由青铜和黄金制成，是一台古代计算机，用于预测日食和行星轨迹。

你发现了羊皮纸地图的完整版本——原来你手中的只是三分之一。完整的地图显示，神庙不是终点，而是中转站。真正的"黄金城"是知识本身，存储在全球十二处类似的神庙中，组成一个网络。

更重要的是，你找到了"离开的方法"。观星台的装置可以打开一条秘密通道，直接通往山下，避开所有危险。但启动装置需要输入正确的星图密码。

墙上刻着提示："当猎户座腰带三星与金字塔对齐时，真理之门开启。"

你还需要收集足够的线索才能解谜（至少需要3点智慧或拥有笔记本）。''',
    set_data={
        "wisdom": "wisdom + 2",
        "translation_notes": "translation_notes + 2"
    }
)

# 祭祀井
sacrificial_well = Node(
    game=game,
    node_id="sacrificial_well",
    name="祭祀之井",
    desc='''深井散发着寒气，黑暗仿佛有实质般浓稠。

这是古代人献祭的地方，不是献祭生命，而是献祭"记忆"。那些触碰黄金而疯癫的人，会被投入这里，他们的身体死去，但意识加入黄金网络。

井壁上刻满了名字——数千年来所有探险者的名字，包括佩德罗提到过的失踪队伍。你看到了1923年的英国探险队，1956年的德国考古组，以及... 明天的日期？还有你自己的名字，{player_name}，已经刻在上面，仿佛你注定会来到这里。

井底传来水声，地下河可能通往外界。如果你有绳索和足够的体力，可以尝试垂降。

但更可怕的是，你听到井底传来低语，像是 thousands of voices 在同时说话，讲述着不同的故事，不同的世纪，不同的语言。

一个声音特别清晰，用佩德罗的声音说："下来吧，这里很安全，这里没有痛苦，只有永恒的知识..."''',
    set_data={
        "courage": "courage - 2",
        "stamina": "stamina - 10"
    }
)

# 结局A：黄金诅咒
ending_cursed = Node(
    game=game,
    node_id="ending_cursed",
    name="结局：黄金囚徒",
    desc='''你拿起了黄金球。

瞬间，知识如海啸般涌入——如何治疗癌症，如何建造永动机，如何预测地震，失落的历史真相，宇宙的奥秘... 你变得全知，仿佛神明。

但你的身体僵住了。黄金从手指开始蔓延，爬上手臂，覆盖胸口。不是腐蚀，而是融合。你变成了黄金雕像，站在宝藏中央，脸上凝固着狂喜的微笑。

你并没有死去。你的意识活在黄金网络中，与所有之前的探险者交流，学习，永恒地思考。当未来的探险者进入这里，你会用他们的语言低语："拿起黄金，获得一切..."

你成为了新的诱饵。

百年后，你的雕像旁边又多了一个新探险者的雕像，而你们在内里交流着，等待着下一个灵魂加入这金色的永恒。

你获得了知识，却失去了自由。''',
    end_desc='''【黄金囚徒结局】

你成为了黄金城的一部分，永恒地守护着秘密。

你的"失踪"成为了探险界的谜团。偶尔有当地土著报告，在月圆之夜，神庙里会传出 multiple voices 的争论声，讨论着哲学和科学。

黄金城再次沉寂，等待下一个贪婪的灵魂。

"取一金，留一魂"''',
    set_data={
        "ending": "'cursed'",
        "stamina": "0"
    }
)

# 结局B：智慧守护者
ending_guardian = Node(
    game=game,
    node_id="ending_guardian",
    name="结局：丛林守护者",
    desc='''你理解了真相。

黄金城不是宝藏，而是一个考验。古代文明故意散布"黄金城"的传说，吸引世界各地的探险者，寻找值得继承他们知识的人。

你坐在观星台前，启动装置，输入了正确的星图坐标。墙壁移动，露出一个密室——不是黄金，而是图书馆，用不灭的材料制成的书籍，记录着一切。

但你可以选择：带走这些知识回到现代世界，或者留在这里成为守护者，维护这个知识库，等待下一个 worthy 的人。

你看着手中的相机（如果你有相机）或笔记本，想到了现代世界的战争、污染、贪婪。知识会被滥用。

你选择了留下。

你喝下了祭台上的草药茶，那是延长生命的秘药。你将成为新的神庙守护者，像传说中的绿胡子隐士一样，在丛林中生活数百年，偶尔帮助迷路的旅人，偶尔驱逐贪婪的盗宝者。

你走出了神庙，站在金字塔顶端，看着无边无际的雨林。一只角雕飞来，停在你身旁，接受了你的抚摸。

你找到了比黄金更珍贵的东西：目的。''',
    end_desc='''【守护者结局】

你成为了亚马逊的传说。

未来的探险者偶尔会报告，在丛林深处遇到一位知晓一切的长者，他/她会提供水、食物和警告，然后消失在绿色中。

你活了两百年，守护着人类失落的知识，直到下一个 worthy 的继承者出现。

当你最终离世时，你的身体化为金色的光，融入了神庙的墙壁，成为了永恒的一部分。

这是最好的结局：知识得到了保护，你也获得了超越凡人的生命意义。''',
    set_data={
        "ending": "'guardian'"
    }
)

# 结局C：生还者
ending_survivor = Node(
    game=game,
    node_id="ending_survivor",
    name="结局：生还者",
    desc='''你拒绝了诱惑。

没有碰黄金，没有跳入深井，你找到了秘密通道，在机关启动后逃离了神庙。

当你走出山洞，呼吸到外界潮湿但清新的空气时，太阳正在落山，丛林被染成金色——比任何黄金都美丽的颜色。

你回到了文明世界，带着照片（如果你有相机）和笔记，以及一个关于古代智慧的故事。没有人相信你关于"活着的黄金"的描述，认为那是丛林热病产生的幻觉。

但你不在乎。

你建立了一个保护基金，买下了神庙周围的土地，阻止了盗宝者的勘探。你写道："有些宝藏不应该被打扰。"

多年后，你成为了一名普通的教授或向导，偶尔在深夜看着亚马逊的方向，知道那里有一个秘密，只有你知道真相。

你失去了财富，但保住了灵魂。''',
    end_desc='''【生还者结局】

你带着生命和理智回到了家。

虽然学术界嘲笑你的"奇幻故事"，但你拍摄的星图和建筑照片成为了重要的考古资料。

最重要的是，你阻止了贪婪对神庙的破坏。在你死后，你的遗嘱将那片土地捐给了保护组织。

在临终的病床上，你仿佛听到丛林的风声，那是守护者在向你致谢。

你平凡地死去，但完整地活着。''',
    set_data={
        "ending": "'survivor'"
    }
)

# 结局D：深渊
ending_abyss = Node(
    game=game,
    node_id="ending_abyss",
    name="结局：坠入深渊",
    desc='''你决定探索祭祀井。

绳索不够长，但你太好奇了。你爬下去，进入地下河，被水流冲走，在黑暗的洞穴中漂流了三天。

当你终于看到光，爬出地面时，你发现自己在一个完全不同的世界——不是地理位置的改变，而是现实本身的改变。

天空有两颗月亮，植物发着荧光，金字塔漂浮在空中。

你穿越了。黄金城不是古代遗迹，而是维度之间的枢纽。那些"失踪"的探险者都来到了这里，建立了一个新的文明。

他们欢迎了你，因为你证明了勇气和好奇心——这是穿越的代价。

但你再也回不去了。现代世界成为了遥远的梦，你只能在这个奇异的平行世界度过余生，写下永远无法寄出的信件给佩德罗。

至少，你还活着。在这个新世界的丛林中。''',
    end_desc='''【深渊结局】

你成为了跨维度旅行者。

在那个世界，你活到了一百岁，学会了飞行和精神交流。你写下了《平行世界生存手册》，成为了那个世界的传奇。

偶尔，当特定的星象出现，你能看到现代世界的影子，看到朋友们在寻找你，但你无法触碰那个维度。

你成为了两个世界之间的传说：在地球，你是失踪的探险者；在新世界，你是来自地球的使者。

这就是探险的终极意义：发现无法想象的未知。''',
    set_data={
        "ending": "'abyss'"
    }
)

# 死亡结局：丛林吞噬
ending_death = Node(
    game=game,
    node_id="ending_death",
    name="结局：回归自然",
    desc='''你的体力耗尽了。

也许是蛇毒，也许是坠落，也许是饥饿，你倒在了离神庙只有一步之遥的地方。视野模糊，呼吸沉重，你感觉到生命在流逝。

但奇怪的是，你不感到恐惧。

丛林没有惩罚你，它只是在做它一直做的事——循环生命。你的身体将成为树木的养分，你的故事将成为传说，你的冒险精神将激励后来的探险者。

最后看到的景象是一只蓝色 Morpho 蝴蝶，停在你鼻尖，翅膀反射着天空的颜色。

然后，宁静。''',
    end_desc='''【回归自然结局】

你的遗体从未被找到。

但三年后，一位当地向导在丛林中发现了一棵异常巨大的古树，树根缠绕着一本湿透的笔记本——你的笔记。

树周围开满了罕见的花朵，动物们聚集在那里，仿佛圣地。

你的冒险结束了，但你的生命以另一种形式延续。这就是亚马逊的方式：死亡不是终点，而是转换。

Rest in nature, {player_name}.''',
    set_data={
        "ending": "'death'",
        "stamina": "0"
    }
)

# ========== 选项定义 ==========

# 从营地出发
opt_jungle = Option(
    game=game,
    option_id="opt_jungle",
    name="穿越密林",
    desc="走最直接的路线，穿过茂密的植被",
    next_node_id="jungle_path"
)

opt_river = Option(
    game=game,
    option_id="opt_river",
    name="沿河前进",
    desc="沿着河流走，寻找捷径",
    next_node_id="river_path"
)

opt_cliff = Option(
    game=game,
    option_id="opt_cliff",
    name="攀爬悬崖",
    desc="从高处俯瞰，寻找神庙位置",
    show_condition="stamina >= 80",
    next_node_id="cliff_path",
    cant_move_desc="体力不足，无法攀岩（需要80以上体力）"
)

# 密林选择
opt_fight_snake = Option(
    game=game,
    option_id="opt_fight_snake",
    name="驱赶森蚺",
    desc="用砍刀或火把驱赶巨蛇",
    show_condition="has_machete or stamina > 80",
    next_node_id="temple_gate",
    cant_move_desc="没有武器或体力不足，无法安全通过"
)

opt_avoid_snake = Option(
    game=game,
    option_id="opt_avoid_snake",
    name="绕道沼泽",
    desc="避开蛇，但穿越毒箭蛙沼泽",
    next_node_id="river_path"
)

opt_study_statue = Option(
    game=game,
    option_id="opt_study_statue",
    name="研究石像",
    desc="仔细记录奇布查语铭文",
    show_condition="has_journal",
    next_node_id="temple_gate"
)

# 河流选择
opt_cross_river = Option(
    game=game,
    option_id="opt_cross_river",
    name="强行渡河",
    desc="快速涉水过河，节省体力",
    move_condition="courage >= 2",
    next_node_id="temple_gate",
    cant_move_desc="勇气不足，不敢冒险渡河"
)

opt_build_raft = Option(
    game=game,
    option_id="opt_build_raft",
    name="扎筏渡河",
    desc="安全但耗时，收集竹子制作筏子",
    next_node_id="temple_gate",
    set_data={"has_rope": "True"}  # 获得绳索
)

opt_wait = Option(
    game=game,
    option_id="opt_wait",
    name="等待危险过去",
    desc="在河岸等待鳄鱼和美洲豹离开",
    next_node_id="ending_death"  # 等待会消耗太多体力/时间
)

# 悬崖选择
opt_climb_fast = Option(
    game=game,
    option_id="opt_climb_fast",
    name="快速攀登",
    desc="不顾角雕攻击，强行攀爬",
    move_condition="courage >= 3",
    next_node_id="temple_gate",
    cant_move_desc="勇气不足，无法面对角雕"
)

opt_find_path = Option(
    game=game,
    option_id="opt_find_path",
    name="寻找古代路径",
    desc="利用古代凿刻的凹坑攀登",
    show_condition="wisdom >= 2",
    next_node_id="temple_gate",
    cant_move_desc="智慧不足，无法识别安全路径"
)

opt_retreat = Option(
    game=game,
    option_id="opt_retreat",
    name="撤退",
    desc="太危险了，放弃攀岩",
    next_node_id="camp"
)

# 神庙大门
opt_solve_puzzle = Option(
    game=game,
    option_id="opt_solve_puzzle",
    name="破解机关",
    desc="根据星图知识旋转圆盘",
    show_condition="wisdom >= 2 or translation_notes >= 1",
    next_node_id="main_hall",
    cant_move_desc="知识不足，无法破解（需要智慧或考古笔记）"
)

opt_force_door = Option(
    game=game,
    option_id="opt_force_door",
    name="强行破门",
    desc="用砍刀或工具撬开大门",
    show_condition="has_machete",
    move_condition="stamina >= 70",
    next_node_id="main_hall",
    cant_move_desc="体力或工具不足"
)

# 主殿选择
opt_go_treasury = Option(
    game=game,
    option_id="opt_go_treasury",
    name="进入黄金之室",
    desc="寻找传说中的黄金",
    next_node_id="treasury"
)

opt_go_observatory = Option(
    game=game,
    option_id="opt_go_observatory",
    name="进入观星台",
    desc="寻找知识和出口",
    next_node_id="observatory"
)

opt_go_well = Option(
    game=game,
    option_id="opt_go_well",
    name="探查祭祀井",
    desc="探索地下通道",
    next_node_id="sacrificial_well"
)

# 黄金之室选择
opt_take_gold = Option(
    game=game,
    option_id="opt_take_gold",
    name="拿起黄金球",
    desc="获取古代知识和财富",
    next_node_id="ending_cursed"
)

opt_leave_gold = Option(
    game=game,
    option_id="opt_leave_gold",
    name="拒绝诱惑",
    desc="离开黄金，寻找其他出路",
    next_node_id="main_hall"
)

# 观星台选择
opt_decode = Option(
    game=game,
    option_id="opt_decode",
    name="解码星图",
    desc="输入密码打开秘密通道",
    show_condition="wisdom >= 3 or translation_notes >= 2",
    next_node_id="ending_survivor",
    cant_move_desc="线索不足，无法解码"
)

opt_stay_guardian = Option(
    game=game,
    option_id="opt_stay_guardian",
    name="成为守护者",
    desc="留在神庙保护知识",
    show_condition="knows_ritual == True and empathy >= 2",
    next_node_id="ending_guardian",
    cant_move_desc="需要理解仪式意义并具备同理心"
)

# 祭祀井选择
opt_descend = Option(
    game=game,
    option_id="opt_descend",
    name="垂降探索",
    desc="用绳索下降到井底",
    show_condition="has_rope and stamina >= 60",
    next_node_id="ending_abyss",
    cant_move_desc="需要绳索和足够体力"
)

opt_listen = Option(
    game=game,
    option_id="opt_listen",
    name="倾听低语",
    desc="尝试与声音交流",
    next_node_id="ending_cursed"  # 被诱惑
)

opt_return = Option(
    game=game,
    option_id="opt_return",
    name="返回主殿",
    desc="这里太危险了，回去",
    next_node_id="main_hall"
)

# ========== 添加选项 ==========

camp.add_option(opt_jungle)
camp.add_option(opt_river)
camp.add_option(opt_cliff)

jungle_path.add_option(opt_fight_snake)
jungle_path.add_option(opt_avoid_snake)
jungle_path.add_option(opt_study_statue)

river_path.add_option(opt_cross_river)
river_path.add_option(opt_build_raft)
river_path.add_option(opt_wait)

cliff_path.add_option(opt_climb_fast)
cliff_path.add_option(opt_find_path)
cliff_path.add_option(opt_retreat)

temple_gate.add_option(opt_solve_puzzle)
temple_gate.add_option(opt_force_door)

main_hall.add_option(opt_go_treasury)
main_hall.add_option(opt_go_observatory)
main_hall.add_option(opt_go_well)

treasury.add_option(opt_take_gold)
treasury.add_option(opt_leave_gold)

observatory.add_option(opt_decode)
observatory.add_option(opt_stay_guardian)
observatory.add_option(opt_leave_gold)

sacrificial_well.add_option(opt_descend)
sacrificial_well.add_option(opt_listen)
sacrificial_well.add_option(opt_return)

# 导出游戏
game.dump("amazon_gold_city.game")
print("游戏已导出到 amazon_gold_city.game")
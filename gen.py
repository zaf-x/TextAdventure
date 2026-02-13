# cyberpunk_game_fixed_v2.py - 完整修复版
game_data = {
    "game_name": "霓虹暗影：赛博侦探",
    "start_node_id": "character_creation",
    "init_inputs": {
        "player_name": {
            "prompt": "输入你的代号（字母数字）：",
            "converter": "str",
            "condition": "len(value) >= 2 and len(value) <= 20",
            "condition_desc": "代号长度必须在 2-20 个字符之间"
        },
        "player_age": {
            "prompt": "输入你的生理年龄（18-60）：",
            "converter": "int",
            "condition": "18 <= value <= 60",
            "condition_desc": "年龄必须在 18-60 岁之间"
        },
        "difficulty": {
            "prompt": "选择难度（1-简单 2-普通 3-困难）：",
            "converter": "int",
            "condition": "value in [1, 2, 3]",
            "condition_desc": "请输入 1、2 或 3"
        }
    },
    "on_load": """
print("=" * 50)
print("  NEON SHADOWS: CYBER DETECTIVE")
print("=" * 50)
print("系统初始化中...")
    """,
    "on_ready": """
difficulty_settings = {
    1: {"hp": 100, "credits": 5000, "hacking": 50},
    2: {"hp": 70, "credits": 3000, "hacking": 30},
    3: {"hp": 50, "credits": 1000, "hacking": 15}
}
settings = difficulty_settings.get(shared_data['difficulty'], difficulty_settings[2])

shared_data['hp'] = settings['hp']
shared_data['max_hp'] = settings['hp']
shared_data['credits'] = settings['credits']
shared_data['hacking'] = settings['hacking']
shared_data['strength'] = 10
shared_data['intelligence'] = 15
shared_data['charisma'] = 10
shared_data['reputation'] = 0
shared_data['inventory'] = []
shared_data['clues'] = []
shared_data['day'] = 1
shared_data['location'] = "公寓"
shared_data['contacts'] = []
shared_data['case_progress'] = 0
shared_data['profession'] = "未选择"

print(f"欢迎，侦探 {shared_data['player_name']}")
print(f"难度：{'简单' if shared_data['difficulty']==1 else '普通' if shared_data['difficulty']==2 else '困难'}")
print(f"初始资金：{shared_data['credits']} 信用点")
print(f"黑客技能：{shared_data['hacking']}")
print("=" * 50)
    """,
    "on_move": """
shared_data['day'] += 0.1
if shared_data['hp'] <= 0:
    print("警告：生命体征临界！")
    """,
    
    "nodes": {
        "character_creation": {
            "name": "角色定制",
            "desc": "你站在镜子前，准备开始新一天的调查。你需要选择你的专长方向。",
            "init_sd": {"created": "True"},
            "options": [
                {
                    "choose_hacker": {
                        "show_name": "技术专家",
                        "desc": "黑客技能+20，智力+5，获得电子工具包",
                        "next_node": "apartment_hacker",  # 跳转到特定版本公寓
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "choose_soldier": {
                        "show_name": "街头战士",
                        "desc": "力量+15，生命+20，获得格斗植入物",
                        "next_node": "apartment_soldier",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "choose_social": {
                        "show_name": "社交达人",
                        "desc": "魅力+20，声望+10，获得情报贩子联系方式",
                        "next_node": "apartment_social",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        # 三个职业的初始公寓，显示职业加成后跳转到标准公寓
        "apartment_hacker": {
            "name": "破旧公寓",
            "desc": "你安顿好电子工具包，感觉自己的技术能力提升了。",
            "on_ready": """
shared_data['hacking'] = shared_data.get('hacking', 0) + 20
shared_data['intelligence'] = shared_data.get('intelligence', 0) + 5
shared_data['inventory'] = shared_data.get('inventory', []) + ['电子工具包']
shared_data['profession'] = '技术专家'
print("[职业加成] 黑客技能 +20，智力 +5")
print("[获得物品] 电子工具包")
print(f"[当前黑客技能] {shared_data['hacking']}")
            """,
            "force_move": [{"condition": "True", "node_id": "apartment"}],
            "options": []
        },
        
        "apartment_soldier": {
            "name": "破旧公寓",
            "desc": "你感受着新植入的格斗芯片，力量涌上心头。",
            "on_ready": """
shared_data['strength'] = shared_data.get('strength', 0) + 15
shared_data['max_hp'] = shared_data.get('max_hp', 100) + 20
shared_data['hp'] = shared_data.get('hp', 100) + 20
shared_data['inventory'] = shared_data.get('inventory', []) + ['格斗植入物']
shared_data['profession'] = '街头战士'
print("[职业加成] 力量 +15，生命上限 +20")
print("[获得物品] 格斗植入物")
print(f"[当前力量] {shared_data['strength']}")
            """,
            "force_move": [{"condition": "True", "node_id": "apartment"}],
            "options": []
        },
        
        "apartment_social": {
            "name": "破旧公寓",
            "desc": "你整理着名片夹，人脉就是金钱。",
            "on_ready": """
shared_data['charisma'] = shared_data.get('charisma', 0) + 20
shared_data['reputation'] = shared_data.get('reputation', 0) + 10
shared_data['contacts'] = shared_data.get('contacts', []) + ['情报贩子']
shared_data['profession'] = '社交达人'
print("[职业加成] 魅力 +20，声望 +10")
print("[获得联系人] 情报贩子")
print(f"[当前魅力] {shared_data['charisma']}")
            """,
            "force_move": [{"condition": "True", "node_id": "apartment"}],
            "options": []
        },
        
        "apartment": {
            "name": "破旧公寓",
            "desc": "你的公寓位于第13区，窗外是永不停歇的霓虹广告。终端上有一条未读消息。",
            "init_sd": {"visited_apartment": "True"},
            "set_sd": {"location": "'公寓'"},
            "on_load": """
if '神经加速器' in shared_data.get('inventory', []):
    print("[系统] 神经加速器已安装，黑客能力大幅提升")
if '格斗植入物' in shared_data.get('inventory', []):
    print("[系统] 格斗植入物运行正常")
            """,
            "on_ready": """
if shared_data['hp'] < shared_data['max_hp']:
    heal = min(10, shared_data['max_hp'] - shared_data['hp'])
    shared_data['hp'] += heal
    print(f"[生命恢复] +{heal} HP，当前：{shared_data['hp']}/{shared_data['max_hp']}")
            """,
            "force_move": [
                {
                    "condition": "shared_data.get('hp', 100) <= 0",
                    "node_id": "hospital"
                }
            ],
            "options": [
                {
                    "check_message": {
                        "show_name": "查看终端消息",
                        "desc": "阅读未读消息，开始主线任务",
                        "next_node": "mission_brief",
                        "show_condition": "shared_data.get('case_progress', 0) == 0",
                        "move_condition": "True"
                    }
                },
                {
                    "hack_darknet": {
                        "show_name": "入侵暗网",
                        "desc": "尝试获取地下情报（需要黑客技能30）",
                        "next_node": "darknet",
                        "show_condition": "'电子工具包' in shared_data.get('inventory', []) or '神经加速器' in shared_data.get('inventory', [])",
                        "move_condition": "shared_data.get('hacking', 0) >= 30",
                        "cant_move_desc": "需要电子设备和30点以上黑客技能"
                    }
                },
                {
                    "go_street": {
                        "show_name": "前往街头",
                        "desc": "出去接点私活赚信用点",
                        "next_node": "street",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "visit_clinic": {
                        "show_name": "去诊所",
                        "desc": "治疗伤势（花费500信用点）",
                        "next_node": "clinic",
                        "show_condition": "shared_data.get('hp', 100) < shared_data.get('max_hp', 100)",
                        "move_condition": "shared_data.get('credits', 0) >= 500",
                        "cant_move_desc": "需要500信用点"
                    }
                },
                {
                    "case_progress": {
                        "show_name": "调查案件现场",
                        "desc": "前往工业区调查谋杀案",
                        "next_node": "industrial_zone",
                        "show_condition": "shared_data.get('case_progress', 0) >= 1",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "mission_brief": {
            "name": "任务简报",
            "desc": "消息来自神秘客户：'侦探，公司区发生了一起谋杀案，死者是义体医生。警方已经结案，但我怀疑有内情。报酬丰厚。'",
            "set_sd": {"case_progress": "1", "client_trust": "0"},
            "on_ready": """
shared_data['clues'].append("死者是义体医生")
shared_data['clues'].append("案件被警方快速结案")
print("[线索更新] 获得2条新线索")
            """,
            "options": [
                {
                    "accept_job": {
                        "show_name": "接受委托",
                        "desc": "开始调查，获得预付款1000信用点",
                        "next_node": "apartment_money",  # 跳转到显示金钱的节点
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "negotiate": {
                        "show_name": "讨价还价",
                        "desc": "要求更多报酬（需要魅力15）",
                        "next_node": "apartment_money_1500",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('charisma', 10) >= 15",
                        "cant_move_desc": "需要15点魅力才能说服客户加价"
                    }
                }
            ]
        },
        
        # 金钱获得提示节点
        "apartment_money": {
            "name": "公寓",
            "desc": "预付款已到账。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) + 1000
print("[金钱] +1000 信用点（预付款）")
print(f"[当前资金] {shared_data['credits']} 信用点")
            """,
            "force_move": [{"condition": "True", "node_id": "apartment"}],
            "options": []
        },
        
        "apartment_money_1500": {
            "name": "公寓",
            "desc": "经过一番谈判，客户同意了更高的价格，但似乎有些不悦。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) + 1500
shared_data['client_trust'] = -5
print("[金钱] +1500 信用点（谈判后）")
print("[注意] 客户信任度下降")
print(f"[当前资金] {shared_data['credits']} 信用点")
            """,
            "force_move": [{"condition": "True", "node_id": "apartment"}],
            "options": []
        },
        
        "street": {
            "name": "霓虹街头",
            "desc": "街头充斥着全息广告和改造人。你可以在这里找些零工，或者去酒吧打听情报。",
            "set_sd": {"location": "'街头'"},
            "on_load": """
import random
if random.random() < 0.3:
    print("[随机事件] 你遇到了街头混混！")
    shared_data['hp'] -= 5
    print(f"受到伤害：-5 HP，当前：{shared_data['hp']}")
            """,
            "options": [
                {
                    "do_job": {
                        "show_name": "接取零工",
                        "desc": "做些杂活赚300信用点",
                        "next_node": "working",  # 跳转到工作节点
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "go_bar": {
                        "show_name": "去酒吧",
                        "desc": "喝酒放松，可能打听到情报（花费200）",
                        "next_node": "bar",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('credits', 0) >= 200",
                        "cant_move_desc": "囊中羞涩，需要200信用点"
                    }
                },
                {
                    "back_home": {
                        "show_name": "返回公寓",
                        "desc": "回家整理线索",
                        "next_node": "apartment",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        # 零工节点 - 显示获得金钱
        "working": {
            "name": "工作中",
            "desc": "你帮商人搬运货物、发传单、修理简单电子设备...工作很累但确实有收入。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) + 300
print("[工作完成] 获得报酬 +300 信用点")
print(f"[当前资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "continue": {
                        "show_name": "继续",
                        "desc": "返回街头",
                        "next_node": "street"
                    }
                }
            ]
        },
        
        "bar":  {
    "name": "零点酒吧",
    "desc": "烟雾缭绕的地下酒吧，这里是情报贩子的聚集地。角落里有个戴着电子眼的老熟人。",
    "set_sd": {"location": "'酒吧'"},
    "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 200
print("[消费] -200 信用点（酒水费）")
print(f"[剩余资金] {shared_data['credits']} 信用点")
    """,
    "options": [
        {
            "buy_info": {
                "show_name": "购买情报",
                "desc": "花费1000信用点购买案件相关情报",
                "next_node": "bar_buy_info",
                "show_condition": "shared_data.get('case_progress', 0) >= 1",  # ✅ 只有开始调查后才显示
                "move_condition": "shared_data.get('credits', 0) >= 1000",
                "cant_move_desc": "需要1000信用点"
            }
        },
        {
            "social_engineer": {
                "show_name": "套近乎",
                "desc": "用魅力免费获取情报（魅力20）",
                "next_node": "info_reveal",
                "show_condition": "shared_data.get('case_progress', 0) >= 1",  # ✅ 只有开始调查后才显示
                "move_condition": "shared_data.get('charisma', 10) >= 20",
                "cant_move_desc": "你的魅力不足以说服他"
            }
        },
        {
            "recruit_hacker": {
                "show_name": "招募黑客助手",
                "desc": "支付2000信用点获得专业黑客协助（永久）",
                "next_node": "bar_recruit",
                "show_condition": "True",  # 招募人手随时可以，不一定要显示情报
                "move_condition": "shared_data.get('credits', 0) >= 2000 and '专业黑客' not in shared_data.get('contacts', [])",
                "cant_move_desc": "需要2000信用点"
            }
        },
        {
            "back": {
                "show_name": "离开",
                "desc": "回到街头",
                "next_node": "street",
                "show_condition": "True",
                "move_condition": "True"
            }
        }
    ]
},
        
        # 酒吧消费/获得节点
        "bar_buy_info": {
            "name": "情报交易",
            "desc": "你付了钱，酒保低声说出了关键信息。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 1000
shared_data['clues'].append("情报：死者研究禁忌芯片")
print("[金钱] -1000 信用点")
print("[线索更新] 死者研究禁忌神经芯片")
print(f"[剩余资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "back": {
                        "show_name": "继续",
                        "desc": "返回酒吧",
                        "next_node": "bar"
                    }
                }
            ]
        },
        
        "bar_recruit": {
            "name": "招募成功",
            "desc": "黑客答应帮你，只要你付得起价钱。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 2000
shared_data['contacts'] = shared_data.get('contacts', []) + ['专业黑客']
print("[金钱] -2000 信用点")
print("[获得联系人] 专业黑客 - 现在可以帮你解密芯片了")
print(f"[剩余资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "back": {
                        "show_name": "返回",
                        "desc": "回到酒吧",
                        "next_node": "bar"
                    }
                }
            ]
        },
        
        "info_reveal": {
            "name": "情报透露",
            "desc": "酒保压低声音：'听着，那个义体医生死前正在研究一种禁忌的神经芯片。公司不想让人知道。'",
            "set_sd": {"case_progress": "2"},
            "on_ready": """
shared_data['clues'].append("死者研究禁忌神经芯片")
shared_data['clues'].append("公司试图掩盖真相")
print("[线索更新] 获得关键情报！")
            """,
            "options": [
                {
                    "return": {
                        "show_name": "继续调查",
                        "desc": "返回街头",
                        "next_node": "street"
                    }
                }
            ]
        },
        
        "industrial_zone": {
            "name": "废弃工业区",
            "desc": "这里弥漫着化学烟雾。义体诊所的废墟就在前方，警戒线还在，但守卫已经撤离。",
            "set_sd": {"location": "'工业区'"},
            "on_load": """
if shared_data.get('hacking', 0) >= 40:
    print("[黑客技能] 你检测到附近有监控摄像头，可以黑入获取录像")
            """,
            "options": [
                {
                    "search_clinic": {
                        "show_name": "搜索诊所",
                        "desc": "仔细搜查现场（可能遇到危险）",
                        "next_node": "clinic_search",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "hack_camera": {
                        "show_name": "黑入监控",
                        "desc": "获取案发当晚录像（黑客40）",
                        "next_node": "camera_footage",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('hacking', 0) >= 40",
                        "cant_move_desc": "需要40点黑客技能"
                    }
                },
                {
                    "back_apartment": {
                        "show_name": "撤退",
                        "desc": "先回公寓整理思路",
                        "next_node": "apartment",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "clinic_search": {
            "name": "诊所内部",
            "desc": "一片狼藉。你在一堆碎玻璃中发现了一个隐藏的数据芯片，但触发了警报！",
            "set_sd": {"case_progress": "3", "has_evidence": "True"},
            "on_ready": """
shared_data['inventory'].append("加密数据芯片")
shared_data['hp'] -= 10
print("[获得物品] 加密数据芯片！")
print("[警告] 警报触发！受到伤害 -10 HP")
print(f"[当前生命] {shared_data['hp']}/{shared_data['max_hp']}")
            """,
            "force_move": [
                {
                    "condition": "True",
                    "node_id": "escape_sequence"
                }
            ],
            "options": []
        },
        
        "escape_sequence": {
            "name": "紧急撤离",
            "desc": "公司安保无人机正在接近！你必须迅速做出选择。",
            "on_load": "print('[危机] 无人机还有30秒到达！')",
            "options": [
                {
                    "fight_drone": {
                        "show_name": "战斗突围",
                        "desc": "用武器摧毁无人机（力量15）",
                        "next_node": "after_escape",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('strength', 10) >= 15",
                        "cant_move_desc": "力量不足，无法对抗无人机"
                    }
                },
                {
                    "hack_drone": {
                        "show_name": "黑入无人机",
                        "desc": "夺取控制权（黑客50）",
                        "next_node": "after_escape",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('hacking', 0) >= 50",
                        "cant_move_desc": "黑客技能不足"
                    }
                },
                {
                    "hide": {
                        "show_name": "躲藏",
                        "desc": "藏进下水道",
                        "next_node": "caught",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "after_escape": {
            "name": "安全屋",
            "desc": "你成功逃脱了。现在需要解密芯片才能知道真相。",
            "set_sd": {"case_progress": "4"},
            "options": [
                {
                    "decrypt": {
                        "show_name": "解密芯片",
                        "desc": "破解芯片内容（黑客60或专业人士）",
                        "next_node": "final_revelation",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('hacking', 0) >= 60 or '专业黑客' in shared_data.get('contacts', []) or '情报贩子' in shared_data.get('contacts', [])",
                        "cant_move_desc": "需要60点黑客技能或认识专业人士（情报贩子/黑客）"
                    }
                }
            ]
        },
        
        "final_revelation": {
            "name": "真相大白",
            "desc": "芯片里记录了可怕的真相：公司在研发控制人类思维的芯片，而那个医生是试图揭露才被灭口。",
            "set_sd": {"case_progress": "5", "has_proof": "True"},
            "on_ready": """
print("=" * 50)
print("[最终线索] 你发现了公司的阴谋！")
print("现在你有两个选择：")
print("1. 公之于众（危险但正义）")
print("2. 卖给公司换取财富（安全但堕落）")
print("=" * 50)
            """,
            "options": [
                {
                    "publish": {
                        "show_name": "公开真相",
                        "desc": "将证据上传到公共网络",
                        "next_node": "good_ending",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                },
                {
                    "sell_out": {
                        "show_name": "卖给公司",
                        "desc": "换取10000信用点和安全",
                        "next_node": "rich_ending",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "good_ending": {
            "name": "真相的代价",
            "desc": "你公开了证据，引发了全城的抗议。公司被迫停止了项目，但你成了通缉犯，必须隐姓埋名。",
            "end_desc": """
[结局：正义的流亡者]

你牺牲了自由，换取了真相大白。
全城因为你而觉醒，虽然你永远不能
以自己的名字生活，但你知道这是值得的。

侦探：{player_name}
案件：已解决 - 公司阴谋曝光
最终声望：{reputation} + 1000
存活天数：{day:.1f}

"在霓虹灯下，真相永不熄灭。"
            """,
            "set_sd": {"ending": "'good'", "reputation": "shared_data.get('reputation', 0) + 1000"}
        },
        
        "rich_ending": {
            "name": "黄金牢笼",
            "desc": "你接受了公司的贿赂，成为了他们的帮凶。你拥有了财富，但每晚都被噩梦困扰。",
            "end_desc": """
[结局：富有的傀儡]

账户：{credits} + 10000
地位：公司顾问
良心：-999

你活了下来，成为了体制的齿轮。
每当看到街头的流浪汉，你都会想起
那个死去的义体医生。

"在霓虹暗影中，每个人都有价格。
你的价格是10000信用点。"
            """,
            "set_sd": {"ending": "'rich'", "credits": "shared_data.get('credits', 0) + 10000"}
        },
        
        "caught": {
            "name": "被捕",
            "desc": "你被公司安保抓住了。他们删除了你的记忆，案件永远成了谜。",
            "end_desc": """
[结局：记忆抹除]

你成为了又一个被公司沉默的知情者。
侦探 {player_name} 从此消失，取而代之的是
一个普通的上班族，对过去的冒险毫无记忆。

案件：未解决
声望：{reputation}
存活天数：{day:.1f}
            """,
            "set_sd": {"ending": "'bad'"}
        },
        
        "hospital": {
            "name": "急救中心",
            "desc": "你在诊所醒来，医生说你的植入物出了故障。这次算你命大。",
            "set_sd": {"hp": "shared_data.get('max_hp', 100) // 2"},
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 1000
print("[医疗费用] -1000 信用点")
print(f"[剩余资金] {shared_data['credits']} 信用点")
            """,
            "force_move": [
                {
                    "condition": "shared_data.get('credits', 0) < 0",
                    "node_id": "debt_ending"
                }
            ],
            "options": [
                {
                    "wake": {
                        "show_name": "苏醒",
                        "desc": "回到公寓继续调查",
                        "next_node": "apartment",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "debt_ending": {
            "name": "债务奴隶",
            "desc": "你付不起医疗费，被迫卖身给公司作为实验体。",
            "end_desc": """
[结局：人体实验品]

由于无法支付医疗费用，
你成为了公司生物部门的实验体。
你的意识被上传到了服务器，
成为了永久的数字囚徒。

侦探 {player_name} 已注销
            """,
            "set_sd": {"ending": "'debt'"}
        },
        
        "darknet": {
            "name": "暗网深处",
            "desc": "这里充斥着非法数据和危险的交易。你找到了一个卖军用级植入物的商人。",
            "on_load": "print('[系统] 暗网连接不稳定...')",
            "options": [
                {
                    "buy_implant": {
                        "show_name": "购买神经加速器",
                        "desc": "黑客+20，花费3000",
                        "next_node": "darknet_buy",
                        "show_condition": "'神经加速器' not in shared_data.get('inventory', [])",
                        "move_condition": "shared_data.get('credits', 0) >= 3000",
                        "cant_move_desc": "需要3000信用点"
                    }
                },
                {
                    "steal_data": {
                        "show_name": "窃取数据",
                        "desc": "尝试黑入商人账户（风险高，黑客70）",
                        "next_node": "darknet_steal",
                        "show_condition": "True",
                        "move_condition": "shared_data.get('hacking', 0) >= 70",
                        "cant_move_desc": "需要70点黑客技能"
                    }
                },
                {
                    "disconnect": {
                        "show_name": "断开连接",
                        "desc": "返回现实世界",
                        "next_node": "apartment",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "darknet_buy": {
            "name": "交易完成",
            "desc": "你安装了神经加速器，感觉思维速度大幅提升。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 3000
shared_data['hacking'] = shared_data.get('hacking', 0) + 20
shared_data['inventory'] = shared_data.get('inventory', []) + ['神经加速器']
print("[金钱] -3000 信用点")
print("[能力提升] 黑客技能 +20")
print("[获得物品] 神经加速器")
print(f"[当前黑客技能] {shared_data['hacking']}")
print(f"[剩余资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "back": {
                        "show_name": "继续",
                        "desc": "返回暗网",
                        "next_node": "darknet"
                    }
                }
            ]
        },
        
        "darknet_steal": {
            "name": "窃取成功",
            "desc": "你成功黑入了商人的账户，但要注意警察的追查。",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) + 5000
shared_data['reputation'] = shared_data.get('reputation', 0) - 10
print("[金钱] +5000 信用点")
print("[声望] -10（犯罪分子）")
print(f"[当前资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "back": {
                        "show_name": "快撤",
                        "desc": "断开连接返回公寓",
                        "next_node": "apartment"
                    }
                }
            ]
        },
        
        "clinic": {
            "name": "地下诊所",
            "desc": "无照医生检查了你的伤势。'能修好，但价格不菲。'",
            "on_ready": """
shared_data['credits'] = shared_data.get('credits', 0) - 500
shared_data['hp'] = shared_data.get('max_hp', 100)
print("[医疗] -500 信用点")
print("[治疗] 生命值已恢复满")
print(f"[剩余资金] {shared_data['credits']} 信用点")
            """,
            "options": [
                {
                    "leave": {
                        "show_name": "离开",
                        "desc": "返回公寓",
                        "next_node": "apartment",
                        "show_condition": "True",
                        "move_condition": "True"
                    }
                }
            ]
        },
        
        "camera_footage": {
            "name": "监控录像",
            "desc": "录像显示案发当晚，一个穿着公司制服的武装小队进入了诊所。这证实了公司的参与。",
            "set_sd": {"case_progress": "max(shared_data.get('case_progress', 0), 3)", "has_video_proof": "True"},
            "on_ready": """
shared_data['clues'].append("公司武装小队出现在现场")
print("[线索更新] 获得决定性证据！")
print("[提示] 现在可以返回公寓整理线索，或继续搜索")
            """,
            "options": [
                {
                    "continue": {
                        "show_name": "继续",
                        "desc": "返回工业区",
                        "next_node": "industrial_zone"
                    }
                }
            ]
        }
    }
}

# convert_to_json.py
import json

def convert_to_json(data, output_file="game.json"):
    """
    将 Python 字典转换为 JSON 文件
    自动处理多行字符串的缩进和换行
    """
    
    class CustomEncoder(json.JSONEncoder):
        def encode(self, obj):
            if isinstance(obj, dict):
                items = []
                for k, v in obj.items():
                    items.append(f'{json.dumps(k)}: {self.encode(v)}')
                return '{\n  ' + ',\n  '.join(items) + '\n}'
            elif isinstance(obj, list):
                if not obj:
                    return '[]'
                items = [self.encode(item) for item in obj]
                # 检查是否需要换行（复杂对象）
                if any('\n' in item or len(item) > 50 for item in items):
                    return '[\n    ' + ',\n    '.join(items) + '\n  ]'
                return '[' + ', '.join(items) + ']'
            elif isinstance(obj, str):
                # 保留多行字符串的换行符
                return json.dumps(obj)
            else:
                return json.dumps(obj)
    
    # 使用标准 json 库，但美化输出
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 已成功转换到 {output_file}")
    print(f"  - 节点数量: {len(data.get('nodes', {}))}")
    print(f"  - 游戏名称: {data.get('game_name', 'Unknown')}")

def validate_game(data):
    """
    验证游戏数据的完整性
    """
    errors = []
    warnings = []
    
    # 检查必需字段
    if "game_name" not in data:
        errors.append("缺少 game_name")
    if "start_node_id" not in data:
        errors.append("缺少 start_node_id")
    if "nodes" not in data:
        errors.append("缺少 nodes")
    
    nodes = data.get("nodes", {})
    
    # 检查起始节点存在
    start_id = data.get("start_node_id")
    if start_id and start_id not in nodes:
        errors.append(f"起始节点 '{start_id}' 不存在于 nodes 中")
    
    # 检查所有节点的选项指向
    for node_id, node in nodes.items():
        if "options" in node:
            for opt in node["options"]:
                for opt_id, opt_data in opt.items():
                    next_node = opt_data.get("next_node")
                    if next_node and next_node not in nodes:
                        errors.append(f"节点 '{node_id}' 的选项 '{opt_id}' 指向不存在的节点 '{next_node}'")
        
        # 检查 force_move
        if "force_move" in node:
            for move in node["force_move"]:
                target = move.get("node_id")
                if target and target not in nodes:
                    errors.append(f"节点 '{node_id}' 的 force_move 指向不存在的节点 '{target}'")
    
    # 输出结果
    if errors:
        print("❌ 验证失败：")
        for e in errors:
            print(f"  - {e}")
        return False
    else:
        print("✓ 验证通过")
        if warnings:
            print("⚠️ 警告：")
            for w in warnings:
                print(f"  - {w}")
        return True

if __name__ == "__main__":
    # 验证
    if validate_game(game_data):
        # 转换
        convert_to_json(game_data, "game.json")
        print("\n游戏特色：")
        print("- 多结局系统（正义/财富/债务/被捕）")
        print("- 属性检定（力量/黑客/魅力）")
        print("- 物品收集（神经接口、数据芯片）")
        print("- 声望系统")
        print("- 随机事件")
        print("- 强制移动（战斗/逃跑/被捕）")
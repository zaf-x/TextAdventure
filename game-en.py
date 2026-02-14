from TextAdventure import Game, Node, Option

# ==================== Game Configuration ====================

game = Game(
    start_node_id="start",
    game_name="Rainy Night Inn",
    init_input=[
        {
            "prompt": "Enter your name: ",
            "name": "player_name",
            "converter": "str",
            "condition": "len(val) > 0",
            "err_desc": "Name cannot be empty"
        },
        {
            "prompt": "Choose your profession (1-Detective 2-Doctor): ",
            "name": "job",
            "converter": "int",
            "condition": "val in [1, 2]",
            "err_desc": "Please enter 1 or 2"
        }
    ]
)

# ==================== Variables Initialization ====================

start = Node(
    game=game,
    node_id="start",
    name="Stormy Night",
    desc="""
Thunder and lightning rage outside. Your car has broken down on a mountain road.
Ahead, you see the sign of an old inn - "Peace Inn".

Soaked to the bone, you enter the lobby. Behind the counter stands a pale man.
"Welcome. You're our only guest tonight." He smiles, but his eyes wander.

Welcome, {player_name}. Your profession: {job_name}.

{profession_hint}

[System] Clues: {clue_count} | Trust: {trust_owner}
    """.strip(),
    init_data={
        "clue_count": "0",
        "trust_owner": "50",
        "has_key": "False",
        "know_secret": "False",
        "investigated_room": "False",
        "checked_basement": "False",
        "job_name": "'Not Set'",
        "profession_hint": "'Please set profession'",
        "ending_rating": "'Unrated'"
    },
    on_load="""
if job == 1:
    data['job_name'] = 'Detective'
    data['profession_hint'] = '[Detective Intuition] You feel something is off about the owner...'
else:
    data['job_name'] = 'Doctor'
    data['profession_hint'] = "[Doctor's Observation] You notice fresh bandages on his left hand..."
    """
)

# ==================== Lobby Options ====================

opt_room = Option(
    game=game,
    option_id="go_room",
    name="Go to your room",
    desc="You're tired and want to rest",
    next_node_id="room"
)

opt_talk = Option(
    game=game,
    option_id="talk_owner",
    name="Talk to the owner",
    desc="Try to learn more information",
    next_node_id="talk"
)

opt_leave = Option(
    game=game,
    option_id="try_leave",
    name="Try to leave",
    desc="This place feels wrong. Risk leaving in the rain",
    next_node_id="leave_attempt",
    move_condition="trust_owner < 30",
    cant_move_desc="The owner seems very suspicious, but you don't have enough evidence. Try talking with him."
)

start.add_option(opt_room)
start.add_option(opt_talk)
start.add_option(opt_leave)
game.add_node(start)

# ==================== Talk with Owner ====================

talk = Node(
    game=game,
    node_id="talk",
    name="Eerie Conversation",
    desc="""
"How long has this inn been open?" you ask.

"Twenty years." The owner wipes a glass. "It used to be busy. Until... the accident. Fewer guests since then."

He pauses: "Do you believe in unexplained things?"

His gaze drifts past you to a closed door at the end of the hallway.

{system_hint}
    """,
    init_data={"system_hint": "' '"},
    set_data={"trust_owner": "trust_owner - 10"},
    on_load="data['system_hint'] = '[System] Trust decreased. You feel uneasy.'"
)

opt_ask_accident = Option(
    game=game,
    option_id="ask_accident",
    name="Ask about the accident",
    desc="Press for details about what happened twenty years ago",
    next_node_id="accident_story"
)

opt_ask_door = Option(
    game=game,
    option_id="ask_door",
    name="Ask about the door",
    desc="Ask where the door at the end of the hallway leads",
    next_node_id="door_story"
)

opt_back_start = Option(
    game=game,
    option_id="back_start",
    name="End conversation, return to lobby",
    desc="Stop asking questions",
    next_node_id="start"
)

talk.add_option(opt_ask_accident)
talk.add_option(opt_ask_door)
talk.add_option(opt_back_start)
game.add_node(talk)

# ==================== Accident Story ====================

accident = Node(
    game=game,
    node_id="accident_story",
    name="Shadows of Twenty Years Ago",
    desc="""
The owner's expression darkens.

"A fire... three people died. My wife and daughter..." His voice trembles. "Police said it was an accident, but I know it wasn't."

He suddenly grabs your hand: "If you can help me find the truth, I'll reward you handsomely!"

You notice he said "three people" but only mentioned his wife and daughter.

{clue_hint}
    """,
    init_data={"clue_hint": "' '"},
    set_data={
        "clue_count": "clue_count + 1",
        "know_secret": "True"
    },
    on_load="data['clue_hint'] = '[Clue +1] Suspicious death count in fire'"
)

back_opt = Option(game, option_id="back_from_accident", name="Continue conversation", next_node_id="talk")
accident.add_option(back_opt)
game.add_node(accident)

# ==================== Door Story ====================

door = Node(
    game=game,
    node_id="door_story",
    name="The Basement",
    desc="""
"That's the basement. Storage for old items." The owner's eyes flicker. "The lock is broken. I don't recommend going down."

He says he doesn't recommend it, but not that you can't.

You notice a rusty brass key on his keychain.

{clue_hint}
    """,
    init_data={"clue_hint": "' '"},
    set_data={"clue_count": "clue_count + 1"},
    on_load="data['clue_hint'] = '[Clue +1] The basement may hide something'"
)

door.add_option(back_opt)
game.add_node(door)

# ==================== Attempt to Leave ====================

leave = Node(
    game=game,
    node_id="leave_attempt",
    name="Choice in the Storm",
    desc="""
You push open the door. Wind and rain instantly soak you.

But in a flash of lightning, you see a car in the shed - no license plate, and the model doesn't match the "burned car from twenty years ago" he described.

More terrifying, beside your car stands a figure, pouring something into your gas tank...

You quickly retreat inside, heart pounding.

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
data['clue_hint'] = '[Clue +2] Suspicious vehicle & sabotage attempt'
data['system_hint'] = '[System] Trust plummets. You realize the danger is real.'
    """
)

leave.add_option(Option(game, option_id="rush_room", name="Sneak back to room and lock door", next_node_id="room"))
leave.add_option(Option(game, option_id="confront", name="Confront the owner", next_node_id="confront"))
game.add_node(leave)

# ==================== Room ====================

room = Node(
    game=game,
    node_id="room",
    name="Room 204",
    desc="""
The room is old but tidy. You lock the door and think.

Rain roars outside, but you faintly hear sounds from downstairs - like something heavy being dragged.

Your professional instincts tell you to investigate this room carefully.

{room_status}
    """,
    init_data={"room_status": "'[System] Room not yet investigated'"},
    on_load="""
if investigated_room:
    data['room_status'] = '[System] You have already searched here'
    """
)

opt_search = Option(
    game=game,
    option_id="search_room",
    name="Search the room",
    desc="Check every corner carefully",
    next_node_id="room_search",
    show_condition="not investigated_room"
)

opt_sleep = Option(
    game=game,
    option_id="sleep",
    name="Try to sleep",
    desc="Maybe you're just too nervous",
    next_node_id="sleep_ending"
)

opt_go_down = Option(
    game=game,
    option_id="go_down",
    name="Go downstairs to investigate",
    desc="Check out the dragging sound",
    next_node_id="downstairs"
)

room.add_option(opt_search)
room.add_option(opt_sleep)
room.add_option(opt_go_down)
game.add_node(room)

# ==================== Room Search ====================

room_search = Node(
    game=game,
    node_id="room_search",
    name="Shocking Discovery",
    desc="""
Under the mattress, you find a diary. The last page reads:

"He's going to kill me, like he killed the others before. Evidence is in the basement, but I can't get the key. If I die, please find what's in the basement..."

The writing stops abruptly.

You also find an old phone under the bed. It has power but no signal - the gallery contains photos of the owner with different guests, their faces crossed out in red.

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
data['clue_hint'] = '[Clue +2] Diary & victim photos'
data['system_hint'] = '[System] You realize you are the next target'
    """
)

room_search.add_option(opt_go_down)
room_search.add_option(Option(game, option_id="plan", name="Formulate escape plan", next_node_id="plan_escape"))
game.add_node(room_search)

# ==================== Plan Escape ====================

plan = Node(
    game=game,
    node_id="plan_escape",
    name="Calm Analysis",
    desc="""
You take a deep breath and organize your thoughts.

{analysis_text}

You need to choose: Risk going to the basement for evidence, or escape immediately?

[System] Current clues: {clue_count}
    """,
    init_data={"analysis_text": "' '"},
    on_load="""
if clue_count >= 4:
    if job == 1:
        data['analysis_text'] = '[Analysis] He is a serial killer. The basement has decisive evidence\\n[Detective Intuition] Need solid evidence to convict. Must check basement'
    else:
        data['analysis_text'] = "[Analysis] He is a serial killer. The basement has decisive evidence\\n[Doctor's Observation] His bandages are fake - no bleeding, wrong wrapping"
else:
    if job == 1:
        data['analysis_text'] = '[Analysis] He is suspicious, but evidence is insufficient\\n[Detective Intuition] Need more clues to be certain'
    else:
        data['analysis_text'] = "[Analysis] He is suspicious, but evidence is insufficient\\n[Doctor's Observation] His behavior is suspicious, but need more evidence"
    """
)

opt_basement = Option(
    game=game,
    option_id="to_basement",
    name="Go to basement",
    desc="Search for decisive evidence",
    next_node_id="basement",
    move_condition="clue_count >= 3",
    cant_move_desc="Insufficient evidence. Too dangerous to enter basement blindly. Need more clues."
)

opt_run = Option(
    game=game,
    option_id="run_away",
    name="Escape during the night",
    desc="Leave through the window, abandon investigation",
    next_node_id="escape_ending"
)

plan.add_option(opt_basement)
plan.add_option(opt_run)
game.add_node(plan)

# ==================== Basement ====================

basement = Node(
    game=game,
    node_id="basement",
    name="Gates of Hell",
    desc="""
You pry open the basement door. The smell of mold and formaldehyde hits you.

Newspaper clippings cover the walls - "Mountain Serial Disappearances, 7 Bodies Found".
A register on the table records "guests" from the past twenty years.

Suddenly, lights flare. The owner stands at the stairs, knife in hand.

"I usually don't act this quickly," he sighs, "but you're too clever."

[System] Final confrontation! Clues: {clue_count}, Profession: {job_name}
    """,
    set_data={"checked_basement": "True"},
    defaults=[
        {"condition": "job == 1 and clue_count >= 5", "node_id": "detective_win"},
        {"condition": "job == 2", "node_id": "doctor_win"},
        {"condition": "True", "node_id": "bad_ending"}
    ]
)

game.add_node(basement)

# ==================== Detective Victory ====================

detective_win = Node(
    game=game,
    node_id="detective_win",
    name="Justice Served",
    desc="""
You calmly raise your phone - you've been livestreaming this whole time.

"Officer Li, did you get all that?" you speak into the phone.

The owner's face changes. He turns to flee but is tackled by SWAT at the door. You contacted the police long ago. This was all a trap to catch the demon who escaped twenty years ago.

"Thank you, Detective." An elderly voice emerges from the shadows - the real survivor of the fire. "I can finally avenge my daughter."

[True Ending: Detective's Justice]
You saved yourself and uncovered the truth. The owner was the arsonist from twenty years ago, and "Peace Inn" was his hunting ground.
    """,
    end_desc="Ending: Justice Served | Master Detective | You demonstrated exceptional reasoning and courage."
)
game.add_node(detective_win)

# ==================== Doctor Victory ====================

doctor_win = Node(
    game=game,
    node_id="doctor_win",
    name="Healer's Heart",
    desc="""
You don't retreat. Instead, you step forward.

"Your left hand - not burns, but chemical corrosion, correct?" you say calmly. "From destroying evidence twenty years ago. It's been festering because you dared not see a doctor."

The owner freezes. The knife trembles slightly.

"I can treat you," you extend your hand, "but you must put down the knife and surrender."

Perhaps it was your professional aura, or perhaps he was truly in pain. Ten minutes later, he kneels sobbing, the knife on the ground.

[True Ending: Healer's Heart]
Your professional knowledge broke the killer's psychological defense. After his surrender, police found all evidence in the basement, solving the serial disappearance case.
    """,
    end_desc="Ending: Healer's Heart | Redeemer | You saved a soul with mercy and professionalism, preventing more tragedy."
)
game.add_node(doctor_win)

# ==================== Bad Ending ====================

bad_end = Node(
    game=game,
    node_id="bad_ending",
    name="Rainy Night Finale",
    desc="""
You try to resist, but the owner is faster.

"Number 8..." These are his last words to you.

Your consciousness fades. The last images are the newspaper clippings and a swaying lightbulb.

[Bad Ending: Rainy Night Finale]
Peace Inn remains open, waiting for the next guest...
    """,
    end_desc="Ending: Rainy Night Finale | Victim | Hint: Collect more clues or choose the right profession strategy."
)
game.add_node(bad_end)

# ==================== Sleep Ending ====================

sleep_end = Node(
    game=game,
    node_id="sleep_ending",
    name="Eternal Slumber",
    desc="""
You're too tired and fall asleep quickly.

In your dreams, you feel someone watching. You try to wake but your body is heavy as lead.

When you finally open your eyes, you can't move - you've been injected with muscle relaxant. The owner stands by the bed, smiling:

"Sleep. It's the best way, no pain."

[Ending: Eternal Slumber]
Sometimes, curiosity is the only chance for survival...
    """,
    end_desc="Ending: Eternal Slumber | Too Careless | Hint: Stay alert in unfamiliar environments."
)
game.add_node(sleep_end)

# ==================== Escape Ending ====================

escape_end = Node(
    game=game,
    node_id="escape_ending",
    name="Survivor",
    desc="""
You climb out the window and run madly through the storm.

The owner's shouts follow, but you dare not look back. You run for two hours until you see headlights on the highway.

You survived, but the evidence remains in the basement. Peace Inn closed the next day, the owner vanished.

Three years later, similar disappearances occur in another mountain region...

[Ending: Survivor]
You saved your life, but justice was not served.
    """,
    end_desc="Ending: Survivor | Cautious Coward | Hint: Sometimes, facing danger bravely requires more wisdom than running."
)
game.add_node(escape_end)

# ==================== Confrontation ====================

confront = Node(
    game=game,
    node_id="confront",
    name="Direct Confrontation",
    desc="""
"What did you put in my car?" you demand.

The owner's expression twists. He grabs a wrench from under the counter and charges.

You turn to run, but the front door is locked. You're trapped in the lobby!
    """,
    defaults=[
        {"condition": "clue_count >= 3", "node_id": "fight_back"},
        {"condition": "True", "node_id": "captured"}
    ]
)
game.add_node(confront)

# ==================== Fight Back ====================

fight_back = Node(
    game=game,
    node_id="fight_back",
    name="Desperate Counterattack",
    desc="""
You grab a vase and throw it while shouting evidence you possess:

"I know what's in the basement! I know about the bodies! I've already called the police!"

He hesitates for one second - enough for you to grab his keys and rush to the basement.

You barricade the door and send your location with weak phone signal. When police break in, you're documenting everything with the diary and register.

[Ending: Desperate Counterattack]
Victory against odds. You survived and brought the killer to justice.
    """,
    end_desc="Ending: Desperate Counterattack | Brave Survivor | You stayed calm in desperation and turned the tables with wit."
)
game.add_node(fight_back)

# ==================== Captured ====================

captured = Node(
    game=game,
    node_id="captured",
    name="Powerless Resistance",
    desc="""
You try to resist, but you know too little about him to find his weakness.

The wrench strikes your head. Darkness falls.

When you wake, you're tied to a chair in the basement. The owner prepares tools, humming.

"Don't worry," he says, "It will be over soon."

[Ending: Powerless Resistance]
Knowledge is power, and ignorance is fatal here.
    """,
    end_desc="Ending: Powerless Resistance | Unprepared | Hint: Collect more clues before facing danger."
)
game.add_node(captured)

# ==================== Downstairs Investigation ====================

downstairs = Node(
    game=game,
    node_id="downstairs",
    name="Fatal Discovery",
    desc="""
You sneak downstairs. The sound comes from the kitchen.

Through the door crack, you see the owner... processing a corpse. It wears clothes similar to yours.

He prepared a "replacement." If you disappeared, he'd use this body to fake your "accidental death."

You accidentally knock over a vase. He turns. Your eyes meet.
    """,
    set_data={"clue_count": "clue_count + 2"},
    defaults=[
        {"condition": "job == 1", "node_id": "detective_bluff"},
        {"condition": "True", "node_id": "chase"}
    ]
)
game.add_node(downstairs)

# ==================== Detective Bluff ====================

bluff = Node(
    game=game,
    node_id="detective_bluff",
    name="Bluffing",
    desc="""
As a detective, you calm down and enter the kitchen.

"Brilliant technique," you applaud. "But do you know how much evidence you left? I sent my location to my partner on the way here. If anything happens to me, you're the prime suspect."

You gamble he won't risk it. Fortunately, you're right - his hesitation shows he still has reason.

"What do you want?" He lowers the tool.

"The key. The basement key. I want to see the evidence, then decide whether to help you."

You get the key and buy time.

[Obtained Basement Key]
    """,
    set_data={"has_key": "True", "clue_count": "clue_count + 1"}
)
bluff.add_option(Option(game, option_id="to_basement_now", name="Go to basement immediately", next_node_id="basement"))
bluff.add_option(Option(game, option_id="bluff_leave", name="Escape while you can", next_node_id="escape_ending"))
game.add_node(bluff)

# ==================== Chase ====================

chase = Node(
    game=game,
    node_id="chase",
    name="Life and Death Chase",
    desc="""
He charges! You turn and run, but he knows the terrain too well.

You crash into a storage room. Desperate, you grab cleaning spray and hit his eyes. He screams and retreats. You escape back to your room and lock the door.

Your heart pounds. You must decide immediately!

[System] Danger Level: EXTREME
    """
)
chase.add_option(Option(game, option_id="hide", name="Jump out window and run", next_node_id="escape_ending"))
chase.add_option(Option(game, option_id="fight", name="Grab a weapon and fight", next_node_id="captured"))
game.add_node(chase)

# ==================== Run Game ====================

if __name__ == "__main__":
    game.play()
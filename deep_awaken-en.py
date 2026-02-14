from TextAdventure import Game, Node, Option

# ==================== Game Configuration ====================

game = Game(
    start_node_id="start",
    game_name="Deep Awakening",
    init_input=[
        {
            "prompt": "Enter crew ID: ",
            "name": "player_id",
            "converter": "str",
            "condition": "len(val) > 0",
            "err_desc": "ID cannot be empty"
        },
        {
            "prompt": "Choose specialty (1-Security Officer 2-Engineer 3-Biologist): ",
            "name": "profession",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "Please enter 1, 2, or 3"
        }
    ]
)

# ==================== Initial Node ====================

start = Node(
    game=game,
    node_id="start",
    name="Cryo Chamber",
    desc="""
The hatch slides open, condensation mist pouring out. You open your eyes, your head throbbing with pain.

[Deep Space Mining Station "PROMETHEUS"]
[Crew ID: {player_id}]
[Specialty: {profession_name}]
[Status: Forcibly awakened from cryosleep]

Alarm lights flash red at the end of the corridor. The intercom crackles:

"...All crew...protocol initiated...unknown biological...containment..."

You're alone. The other cryo pods are empty—the rest of the crew either evacuated or...

{profession_hint}

[SYSTEM] Oxygen: {oxygen}% | Sanity: {sanity}% | Infection: {infection}%
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
        "profession_name": "'Not Set'",
        "profession_hint": "' '",
        "temp_hint": "' '"
    },
    on_load="""
if profession == 1:
    data['profession_name'] = 'Security Officer'
    data['profession_hint'] = '[Security Training] You notice signs of violent forced entry on the hatch—not a system malfunction...'
elif profession == 2:
    data['profession_name'] = 'Engineer'
    data['profession_hint'] = '[Engineering Knowledge] The alarm system has been manually modified—this is no accident...'
else:
    data['profession_name'] = 'Biologist'
    data['profession_hint'] = '[Biological Intuition] The air carries a strange scent, like... rotting seaweed mixed with ozone...'
    """
)

# Options
opt_corridor = Option(game, option_id="to_corridor", name="Enter Corridor", desc="Investigate the alarm source", next_node_id="corridor")
opt_locker = Option(game, option_id="check_locker", name="Check Locker", desc="Search for equipment", next_node_id="locker")
opt_terminal = Option(game, option_id="check_terminal", name="Access Terminal", desc="Review ship logs", next_node_id="terminal")

start.add_option(opt_corridor)
start.add_option(opt_locker)
start.add_option(opt_terminal)
game.add_node(start)

# ==================== Locker ====================

locker = Node(
    game=game,
    node_id="locker",
    name="Equipment Room",
    desc="""
The metal locker hangs half-open, contents scattered everywhere.

You found:
- Portable oxygen tank (equipped)
- {locker_item}

[SYSTEM] Oxygen replenished to 100%
    """,
    init_data={"locker_item": "'Basic Supply Pack'"},
    set_data={"oxygen": "100"},
    on_load="""
if profession == 1:
    data['has_weapon'] = True
    data['locker_item'] = 'Plasma Cutter (Security Officer exclusive weapon)'
elif profession == 2:
    data['has_tools'] = True
    data['locker_item'] = 'Engineering Toolkit (can repair systems or craft weapons)'
else:
    data['has_sample'] = True
    data['locker_item'] = 'Biological Sampler (can analyze unknown substances)'
    """
)

locker.add_option(Option(game, option_id="back_to_start", name="Return to Cryo Chamber", next_node_id="start"))
locker.add_option(Option(game, option_id="locker_to_corridor", name="Go to Corridor", next_node_id="corridor"))
game.add_node(locker)

# ==================== Terminal ====================

terminal = Node(
    game=game,
    node_id="terminal",
    name="Bridge Terminal",
    desc="""
The screen flickers as you pull up the final log entries:

[Captain's Log - Final Entry]
"...We discovered something in the asteroid belt... a structure. Not natural.
It... called to us. Dr. Davis insisted on bringing back a sample.
Now the sample bay is sealed. Davis says he's 'communing with it.'
I don't trust that thing. I've initiated emergency cryo protocol—"

The log ends. Final timestamp: 72 hours ago.

{terminal_extra}
    """,
    init_data={"terminal_extra": "' '"},
    on_load="""
if profession == 2:
    data['terminal_extra'] = '[Engineering Expertise] You discover the cryo protocol was manually interrupted—someone deliberately woke you...'
    data['know_truth'] = True
else:
    data['terminal_extra'] = '[SYSTEM] Data corrupted. Unable to recover additional information.'
    """
)

terminal.add_option(Option(game, option_id="terminal_back", name="Return to Cryo Chamber", next_node_id="start"))
terminal.add_option(Option(game, option_id="terminal_to_corridor", name="Go to Corridor", next_node_id="corridor"))
game.add_node(terminal)

# ==================== Corridor ====================

corridor = Node(
    game=game,
    node_id="corridor",
    name="Main Corridor",
    desc="""
The corridor lights flicker. The walls bear... scratch marks? No, corrosion—metal melting like candle wax.

You hear something in the distance—a wet, dragging sound.

Left: Sample Bay (sealed, red light flashing)
Right: Escape Pod (authorization code required)
Forward: Engine Room (oxygen leak warning)

{corridor_hint}
    """,
    init_data={"corridor_hint": "' '"},
    on_load="""
if profession == 3 and has_sample:
    data['corridor_hint'] = '[Biological Sampler Alert] Organic compounds in the air... not terrestrial life. DNA sequences constantly shifting.'
    data['infection'] = infection + 5
else:
    data['corridor_hint'] = '[SYSTEM] Environmental scan complete. Trace organic contaminants detected.'
    data['infection'] = infection + 10
    """
)

opt_sample = Option(
    game=game, 
    option_id="to_sample", 
    name="Go to Sample Bay", 
    desc="Investigate the source",
    next_node_id="sample_room",
    move_condition="has_weapon or has_tools",
    cant_move_desc="Too dangerous to enter without weapons or tools."
)

opt_escape = Option(
    game=game,
    option_id="to_escape",
    name="Go to Escape Pod",
    desc="Abandon investigation, prioritize survival",
    next_node_id="escape_pod",
    move_condition="know_truth or profession == 1",
    cant_move_desc="You don't know what's happening. Can't run yet. Need more information."
)

opt_engine = Option(game, option_id="to_engine", name="Go to Engine Room", desc="Repair oxygen systems", next_node_id="engine_room")

corridor.add_option(opt_sample)
corridor.add_option(opt_escape)
corridor.add_option(opt_engine)
game.add_node(corridor)

# ==================== Engine Room ====================

engine_room = Node(
    game=game,
    node_id="engine_room",
    name="Engine Core",
    desc="""
It's worse here. Oxygen pipes ruptured, cryogenic gas venting.

More corrosion on the walls... and you hear it—that wet dragging sound, inside the pipes.

Console display: [REACTOR UNSTABLE - EVACUATE IMMEDIATELY]

{engine_option}
    """,
    init_data={"engine_option": "' '"},
    on_load="""
if profession == 2 and has_tools:
    data['engine_option'] = '[Engineering Expertise] You have tools. You can attempt to repair the system and establish containment, or initiate self-destruct.'
elif profession == 2:
    data['engine_option'] = '[Engineering Expertise] You understand the system, but cannot operate it without tools. Return to the locker.'
else:
    data['engine_option'] = '[SYSTEM WARNING] Dangerous energy levels detected. Immediate evacuation recommended.'
    """
)

opt_fix = Option(
    game=game,
    option_id="fix_system",
    name="Attempt System Repair",
    desc="Stabilize reactor, establish containment",
    next_node_id="engine_battle",
    move_condition="has_tools",
    cant_move_desc="Without engineering tools, you cannot operate the console. Go to the locker first."
)

opt_destroy = Option(
    game=game,
    option_id="self_destruct",
    name="Initiate Emergency Self-Destruct",
    desc="Destroy the station with you in it",
    next_node_id="sacrifice_ending",
    move_condition="profession == 2"
)

opt_leave_engine = Option(game, option_id="leave_engine", name="Leave", desc="Return to corridor", next_node_id="corridor")

engine_room.add_option(opt_fix)
engine_room.add_option(opt_destroy)
engine_room.add_option(opt_leave_engine)
game.add_node(engine_room)

# ==================== Engine Room Battle ====================

engine_battle = Node(
    game=game,
    node_id="engine_battle",
    name="Contact in the Shadows",
    desc="""
You begin working the console, fingers flying across the keys.

Suddenly, a pipe bursts! A mass of... something... pours out. Not gas—organic matter, writhing like a living thing.

It lunges at you!
    """,
    defaults=[
        {"condition": "profession == 2 and has_tools", "node_id": "engine_success"},
        {"condition": "True", "node_id": "engine_fail"}
    ]
)

game.add_node(engine_battle)

# ==================== Engine Room Success ====================

engine_success = Node(
    game=game,
    node_id="engine_success",
    name="Containment Established",
    desc="""
You grab the plasma torch (from your toolkit) and drive the organic mass back.

Meanwhile, your other hand never stops working—

[FIREWALL ACTIVATED]
[SAMPLE BAY SEALED - COMPLETE]
[LIFE SUPPORT - CONTAINMENT MODE ENGAGED]

The thing screams—not a sound, but a psychic shriek in your mind. But it's trapped, locked in the sample bay by energy fields.

You collapse, gasping. You won, but only for now.

You have two choices:
    """,
    on_load="data['know_truth'] = True"
)

opt_stay = Option(game, option_id="stay_guard", name="Stay and Guard", desc="Establish outpost, monitor threat", next_node_id="fix_ending")
opt_leave_now = Option(game, option_id="leave_now", name="Take Escape Pod", desc="Warning sent, mission complete", next_node_id="escape_pod")

engine_success.add_option(opt_stay)
engine_success.add_option(opt_leave_now)
game.add_node(engine_success)

# ==================== Engine Room Failure ====================

engine_fail = Node(
    game=game,
    node_id="engine_fail",
    name="Out of Control",
    desc="""
You have no tools. You can only fight the organic mass with your bare hands.

It wraps around your arm—cold, wet, then... warm? No, burning. It's trying to enter you.

You struggle to hit the emergency button—not repair, but self-destruct.

"Die with me."

[ENDING: OUT OF CONTROL]
You failed to repair the system, but at least you stopped it from spreading. The station's wreckage will drift into deep space, far from Earth.
    """,
    end_desc="Ending: Out of Control | Tragic Hero | You failed, but prevented greater disaster."
)
game.add_node(engine_fail)

# ==================== Sample Bay ====================

sample_room = Node(
    game=game,
    node_id="sample_room",
    name="Sample Bay",
    desc="""
The hatch seals behind you.

This... was once a laboratory. Now it's a biological cathedral.

The walls are covered in pulsating flesh-membrane, emitting bioluminescent blue light. The central containment pod is ruptured, something... once inside.

You see Dr. Davis. Or what was Dr. Davis. He floats in the chamber center, body fused with the flesh-membrane, dozens of neural tendrils connected to his spine.

His eyes suddenly open—completely black, no whites.

"{player_id}..." His voice comes from the deep sea, "You've finally come. We've been waiting. Join us... end the loneliness..."

{sample_reaction}

[SYSTEM] Sanity: {sanity}% | Infection: {infection}%
    """,
    init_data={
        "sample_reaction": "' '",
        "temp_sanity": "0"
    },
    set_data={
        "sanity": "sanity - 30",
        "infection": "infection + 20"
    },
    on_load="""
# Note: In script environment, write operations must use data['key']
if profession == 3:
    data['sample_reaction'] = '[Biologist Insight] This is not infection... it is symbiosis. It offers immortality, but the price is... loss of individual consciousness.'
    data['temp_sanity'] = 10  # Biologists understand more, lose less sanity
else:
    data['sample_reaction'] = '[Mental Shock] Your worldview is collapsing...'
    data['temp_sanity'] = -30

# Read operations can use variable names directly, write operations must use data[]
data['sanity'] = sanity + data['temp_sanity']
    """,
    defaults=[
        {"condition": "profession == 3 and has_sample", "node_id": "biologist_ending"},
        {"condition": "has_weapon", "node_id": "fight_alien"},
        {"condition": "True", "node_id": "assimilated"}
    ]
)

game.add_node(sample_room)

# ==================== Biologist Exclusive Ending ====================

biologist_ending = Node(
    game=game,
    node_id="biologist_ending",
    name="Path of Evolution",
    desc="""
You raise the sampler—not to attack, but to... adjust frequency.

"I understand you," you say. "You are a lonely traveler, seeking companions. But forced fusion is not the answer."

The Doctor/It tilts its head. Curiosity?

You continue: "I can help you. True symbiosis, not consumption, but... cooperation. Let me be a bridge, not a host."

Long silence. Then, the neural tendrils slowly retract. Davis's body falls, unconscious but alive.

The flesh-membrane contracts, condensing into... an embryo? A seed.

You hold it, feeling infinite knowledge—star maps, lost technologies, and... millions of other "travelers" waiting.

[TRUE ENDING: PATH OF EVOLUTION]
You established humanity's first true contact with interstellar life. Not conquest, not submission, but understanding. Earth will change forever, but you ensured human agency.

The seed pulses in your hand, like a tiny heart.
    """,
    end_desc="Ending: Path of Evolution | Star Ambassador | You opened a new era with science and empathy."
)
game.add_node(biologist_ending)

# ==================== Combat Ending ====================

fight_alien = Node(
    game=game,
    node_id="fight_alien",
    name="Purifying Fire",
    desc="""
You raise your weapon.

"Sorry, Doctor. But you're no longer human."

Plasma tears through the flesh-membrane. A scream—not sound, but psychic agony in your mind.

Davis's body convulses, neural tendrils thrashing wildly. You keep firing until...

Explosion. You triggered overload. The entire bay becomes an inferno.

You run, escaping through the airlock in the final second. Behind you, the sample bay is purified by vacuum and flame.

[ENDING: PURIFYING FIRE]
You destroyed the threat, but also destroyed the chance to understand it. When rescuers found you, you said only one thing: "Burn it all."

The station was abandoned, the asteroid belt declared restricted. But you know... there are more "travelers" in the universe.
    """,
    end_desc="Ending: Purifying Fire | Survivor | You paid the price, but protected humanity."
)
game.add_node(fight_alien)

# ==================== Assimilation Ending ====================

assimilated = Node(
    game=game,
    node_id="assimilated",
    name="The Great Merge",
    desc="""
You have no weapon.

Neural tendrils wrap your limbs—not painful... surprisingly warm. Your memories begin to flow—childhood, training, this mission—all pouring into some greater consciousness.

You see the truth of the universe: stars born and dying, civilizations rising and falling, endless dark and light.

"No longer alone..." you hear yourself say, and hear a thousand voices say as one.

Your body merges with the flesh-membrane, becoming part of the cathedral. But in the final moment, you retain a shred of... self. An observer, witnessing eternity.

[ENDING: THE GREAT MERGE]
You lost your individuality, but gained infinity. In deep space, a new node is born, waiting for the next visitor.

Perhaps one day, you will awaken again. As part of "Us."
    """,
    end_desc="Ending: The Great Merge | New Node | Individuality ends, consciousness continues."
)
game.add_node(assimilated)

# ==================== Repair Ending (The Watcher) ====================

fix_ending = Node(
    game=game,
    node_id="fix_ending",
    name="The Watcher",
    desc="""
You transformed the station into... a prison. The sample bay permanently sealed, life support converted to containment mode, trapping that thing in eternal dormancy.

Then you sent the signal. Not a distress call—a warning.

[DEEP SPACE OUTPOST "PROMETHEUS" ESTABLISHED]
[THREAT LEVEL: MAXIMUM]
[WATCHER: {player_id}]

You stayed. Ten years? Twenty? In intermittent cryosleep awakenings, you monitored the cage.

Sometimes, you feel it speaking in your dreams. Tempting you. But you refuse.

"No," you say. "This is our sky. You chose the wrong host."

[TRUE ENDING: THE WATCHER]
You sacrificed your years to ensure the threat would not spread. Until one day, a true solution will be found. Until then, you are humanity's frontier.
    """,
    end_desc="Ending: The Watcher | Lone Guardian | You bought safety with time."
)
game.add_node(fix_ending)

# ==================== Sacrifice Ending ====================

sacrifice_ending = Node(
    game=game,
    node_id="sacrifice_ending",
    name="Supernova",
    desc="""
Countdown: 60 seconds.

You don't run. You sit by the reactor core, watching the readings climb.

"Come on," you say, "let's see who's brighter."

The explosion has no sound, only light. The station, the sample, the thing... all reduced to elementary particles.

Earth receives the final signal: [THREAT NEUTRALIZED - CREWMAN {player_id} SIGNED]

Your atoms now drift through the asteroid belt, mingling with starlight. Sometimes, passing ships report strange auroras... like a smile.

[ENDING: SUPERNOVA]
You chose the most magnificent end. No pain, only a moment of glory. Humanity will never know your name, but they are safe.
    """,
    end_desc="Ending: Supernova | Martyr | You became starlight."
)
game.add_node(sacrifice_ending)

# ==================== Escape Pod ====================

escape_pod = Node(
    game=game,
    node_id="escape_pod",
    name="Escape Pod",
    desc="""
The hatch opens. Cramped space, enough fuel to reach the nearest shipping lane.

But you know the truth. If you run, that thing will continue to grow. Maybe years, maybe decades, but it will find a way to reach Earth.

{escape_dilemma}
    """,
    init_data={"escape_dilemma": "' '"},
    on_load="""
if know_truth:
    data['escape_dilemma'] = '[Knowledge is Burden] You know too much to just leave. But survival... also matters.'
else:
    data['escape_dilemma'] = '[Survival Instinct] Alarms scream, instinct urges you to flee this hellhole.'
    """
)

opt_launch = Option(game, option_id="launch_pod", name="Launch Escape Pod", desc="Abandon the station", next_node_id="coward_ending")
opt_return = Option(game, option_id="return_fight", name="Return to Fight", desc="Cannot run like this", next_node_id="corridor")

escape_pod.add_option(opt_launch)
escape_pod.add_option(opt_return)
game.add_node(escape_pod)

# ==================== Coward Ending ====================

coward_ending = Node(
    game=game,
    node_id="coward_ending",
    name="The Returnee",
    desc="""
The escape pod launches. The station shrinks to a star, then vanishes.

You are rescued. Three months later, you stand at the hearing, telling your story.

"...I don't know what it was," you say, "I just... wanted to live."

They don't blame you. But sometimes, late at night, you wake from dreams hearing that voice:

"{player_id}... we are still waiting..."

Three years later, deep space telescopes discover "PROMETHEUS" is gone. Not destroyed, but... departed. Like a seed, drifting toward Earth.

You spend the rest of your life waiting. Waiting for a knock at the door.

[ENDING: THE RETURNEE]
You survived, but will never know if you chose right. Perhaps one day, you will meet your "friend" again.
    """,
    end_desc="Ending: The Returnee | Survivor | You chose life, but carry the question."
)
game.add_node(coward_ending)

# ==================== Run ====================

if __name__ == "__main__":
    game.play()
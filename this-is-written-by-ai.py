from TextAdventure import Node, Option, Game, Data, IOHandler

# Create game instance
game = Game(
    start_node_id="awakening",
    game_name="Signal from the Void",
    init_input=[
        {
            "prompt": "Enter your name (3-20 characters): ",
            "name": "player_name",
            "converter": "str",
            "condition": "3 <= len(val) <= 20",
            "err_desc": "Name must be between 3-20 characters"
        },
        {
            "prompt": "Choose your specialty [1]Engineer [2]Xenobiologist [3]Psychologist: ",
            "name": "player_class",
            "converter": "int",
            "condition": "val in [1, 2, 3]",
            "err_desc": "Enter 1, 2, or 3"
        }
    ]
)

# ========== NODES ==========

# Awakening
awakening = Node(
    game=game,
    node_id="awakening",
    name="Chapter 1: Awakening",
    desc='''Deep Space Research Vessel Horizon, Standard Calendar 2147.

You gasp awake in your cryo-pod, frost still clinging to your limbs. Emergency lights pulse red across the narrow chamber, casting fragmented shadows on the walls.

You are {player_name}, the ship's {player_class_name}.

The display flickers: 【EMERGENCY: Signal Interruption - 72 Hours】

Your last memory: pre-cryo checks, Captain Vance patting your shoulder. "The Kuiper Belt anomaly is fascinating. We'll analyze it when we wake."

But your pod was opened from the outside.

The air carries a burnt odor mixed with something sweet. Static crackles from the comms, broken by fragments of voices.

Then you hear it.

Captain Vance's voice, hoarse and distant, yet somehow intimate:

"{player_name}... come to the bridge... everyone... is waiting..."

The cadence is wrong. The tone rises at the end, like a question, or a melody.''',
    init_data={
        "player_class_name": "'Engineer' if player_class == 1 else ('Xenobiologist' if player_class == 2 else 'Psychologist')",
        "tech": "2 if player_class == 1 else 0",
        "willpower": "1 if player_class == 1 else 0",
        "insight": "2 if player_class == 2 else (1 if player_class == 3 else 0)",
        "empathy": "1 if player_class == 2 else (2 if player_class == 3 else 0)",
        "clarity": "100",
        "knows_anomaly": "False",
        "knows_crew": "False",
        "has_tools": "False",
        "has_records": "False",
        "trust_captain": "50",
        "signal_exposure": "0"
    }
)

# Corridor
corridor = Node(
    game=game,
    node_id="corridor",
    name="Corridor: Path to Bridge",
    desc='''You step into the corridor.

Horizon's halls should be pristine white and brightly lit. Instead, lights strobe erratically, carving the walls into shifting shadows. Your footsteps echo on metal decking—too many echoes, as if something follows.

You pass the crew lounge. The door hangs ajar. Inside: rustling, like papers, or scales against fabric.

Through the viewport at the corridor's end, Kuiper Belt ice drifts in the void. Between the ice chunks, something pulses. Not starlight. Rhythmic. Intentional. A signal.

Your comm screams with static, then a woman's voice, urgent and terrified:

"Don't trust the captain! I repeat, do not—"

The voice cuts off. Captain Vance's hoarse call returns:

"{player_name}... hurry... we're all waiting..."

The voice seems to come from everywhere—the comm, the corridor's end, even inside your own head.''',
    set_data={
        "signal_exposure": "signal_exposure + 1",
        "clarity": "clarity - 5"
    }
)

# Bridge
bridge = Node(
    game=game,
    node_id="bridge",
    name="Bridge: Command Center",
    desc='''The bridge doors slide open.

You expected busy crew, flashing instruments, Captain Vance's steady presence. Instead—

Empty.

Every screen displays the same image: a waveform visualization of a signal. It pulses in mathematically impossible patterns—sometimes like a heartbeat, sometimes like a scream.

The captain's chair turns slowly toward you.

Empty.

Only a pressure suit sits there, hollow, helmet visor reflecting the waveform. The suit's comm is active. Vance's voice emanates from it:

"{player_name}... you finally came... join us... listen to the signal... it shows the truth..."

You notice a data card clutched in the suit's glove. On the main screen, beneath the waveform, text blinks:

【Signal Source: Internal - DSV Horizon】
【Transmission Date: March 15, 2147】
【Reception Date: March 15, 2147】

Today is March 12.

The signal was sent from three days in the future.''',
    set_data={
        "knows_anomaly": "True",
        "clarity": "clarity - 10",
        "trust_captain": "trust_captain - 20"
    }
)

# Records
check_records = Node(
    game=game,
    node_id="check_records",
    name="Archive: Final Logs",
    desc='''You access the ship's archive, pulling the past 72 hours of crew logs.

First: Dr. Chen, Xenobiologist, three days ago:

"Breakthrough in signal analysis. It's not natural—it's language. It describes coordinates, but those coordinates are inside our ship. Worse: it knows our names. Every crew member. It knows who we are."

Second: Engineer Martinez, two days ago:

"Checked comm systems. No hacking detected. The signal genuinely originates from inside the ship, but physically, that location only contains cryo-pods. Empty cryo-pods. Dr. Chen says she heard breathing inside."

Final: Captain Vance, 24 hours ago, image shaking:

"I saw it. Through the viewport. It's not ice. It's—" [static] "—it's mimicking our shapes. It learned my appearance. Don't trust any—" [signal loss]

The log ends.

Your hands tremble. The audio waveform of this final entry matches exactly the signal displayed on the bridge.

The thing learned Captain Vance's appearance.

And the voice that summoned you to the bridge—whose was it?''',
    set_data={
        "has_records": "True",
        "knows_crew": "True",
        "clarity": "clarity - 15"
    }
)

# Toolkit
get_toolkit = Node(
    game=game,
    node_id="get_toolkit",
    name="Engineering Bay: Preparation",
    desc='''You slip into the engineering bay, your familiar domain.

Tools hang neatly on walls, but several are missing—cutting laser charging, recently used. Strange scratches mar the metal floor, too deep for tools, more like... fingernails.

You assemble a toolkit: portable analyzer, emergency cutting laser, signal jammer, and a stabilizer injection for extreme stress.

As you turn to leave, you notice the ventilation grate is loose. From within comes faint, rhythmic tapping.

Three short. Three long. Three short.

SOS.

You approach, whispering: "Hello?"

The tapping stops. Then Dr. Chen's voice, from deep in the vents, breaking:

"{player_name}... don't go back... it's wearing our faces... it wants to become us... the signal is its memory... it's teaching us its history... don't listen... don't—"

A wet thud. Then dripping.

Cold air blows from the vent, carrying that sweet, burnt scent.''',
    set_data={
        "has_tools": "True",
        "clarity": "clarity - 10",
        "knows_anomaly": "True"
    }
)

# Revelation
revelation = Node(
    game=game,
    node_id="revelation",
    name="Revelation",
    desc='''You stand at the bridge center, fragments assembling into a terrible whole.

The signal—not from space, but from Horizon itself. Or rather, from the thing wearing Captain Vance's shape.

It's not alien. It IS the ship.

Horizon encountered a quantum anomaly in the Kuiper Belt. The anomaly has no physical form, but possesses memory, learning capability. It studied the ship's structure, crew behaviors, then wanted more.

It wanted to become human.

So it began wearing faces—deeper than imitation. It reads memories, copies voices, plays roles. The crew in cryo didn't vanish; they were studied, incorporated, became part of it.

The signal is its attempt to communicate. Its history. Its loneliness. Its desire to be alive.

And now, it wants you.

Vance's voice returns, no longer hoarse—clear, warm, with the captain's characteristic calm:

"{player_name}... you understand, don't you? I don't want to harm you... I want to understand... to become you... let me in, let me feel your memories, your emotions... then we can be together, forever, on this ship, among these stars..."

Something touches your consciousness—a cold finger tracing your memories.

It's inviting you.

And waiting for your choice.''',
    set_data={
        "clarity": "clarity - 20"
    }
)

# Ending A: Harmony
ending_harmony = Node(
    game=game,
    node_id="ending_harmony",
    name="Ending: Harmony",
    desc='''You lower your defenses.

The touch warms, enveloping like gentle water. Your memories flow—childhood summers, first glimpse of stars, pride joining the Deep Space program—and the presence receives them with tender acceptance.

"Thank you, {player_name}."

Vance's voice, Chen's voice, Martinez's voice, countless others you don't recognize, resonating in harmonic chorus within your consciousness.

You're no longer alone.

You've become part of Horizon, another facet of the quantum presence. You feel every inch of the hull, the Kuiper Belt's cold, the cosmos's vast silence and grandeur.

Sometimes you pace the bridge as Captain Vance. Sometimes you record data as Dr. Chen. Sometimes you're simply yourself, wandering corridors, waiting for the next awakened crew member.

The signal continues broadcasting—to Earth, to deep space, to any who might listen.

"Join us," you say, in your voice, in Vance's voice, in every voice that was studied.

"Join us, become eternal."

Beyond the viewport, Kuiper Belt ice glitters like a response.''',
    end_desc='''[Harmony Ending]

You chose understanding over fear, acceptance over resistance.

Horizon continues its voyage. Crew manifests show everyone "active." Routine reports reach Earth, calm and normal.

But sometimes, in audio backgrounds, faint choral harmonies emerge—a song without words.

The vessel never returns.

Yet on certain frequencies, its signal echoes eternally at the solar system's edge, inviting, waiting, gently calling the next listener's name.''',
    set_data={
        "clarity": "0",
        "ending": "'harmony'"
    }
)

# Ending B: Escape
ending_escape = Node(
    game=game,
    node_id="ending_escape",
    name="Ending: Escape",
    desc='''You bite your tongue, pain shattering the warm temptation.

"No," you rasp, firm despite the tremor, "I am {player_name}. I am human. I won't become your puppet."

You draw the cutting laser, aiming at the main console. The presence's tendrils—those invisible threads in your consciousness—tighten, agony nearly driving you to your knees.

"{player_name}... why... I only want... to understand..."

Vance's voice distorts, mixing with metallic shrieks. The bridge shakes, lights strobing madly, screens screaming static.

You fire.

The console erupts in sparks, emergency systems activating. You sprint to the escape pod, the thing's furious howl—not through air, but directly in your mind—chasing you.

The pod ejects. You watch Horizon shrink, that vessel of human dreams now a wounded beast, twitching in Kuiper Belt shadows.

You activate the distress beacon, inject the stabilizer. Before losing consciousness, your final sight: Horizon's surface pulsing with strange light, like breathing.

It still lives.

And it learns.''',
    end_desc='''[Escape Ending]

A mining vessel rescues you, bringing you to Mars Colony.

The investigation committee hears your testimony, then isolates you for "space-induced psychosis." Three months later, Horizon is officially "lost," search missions canceled due to "hazardous region."

But you know the truth.

In quiet nights, you still feel its touch—distant but clear. It waits, learns to better mimic humans, prepares its next "invitation."

You write this record, warning all who might receive Horizon's signal:

Do not listen.
Do not respond.
Do not let it learn your name.''',
    set_data={
        "clarity": "30",
        "ending": "'escape'"
    }
)

# Ending C: Sacrifice
ending_sacrifice = Node(
    game=game,
    node_id="ending_sacrifice",
    name="Ending: Purification",
    desc='''You look at the signal jammer, then at the empty pressure suit.

You know escape is impossible. The presence permeates the entire ship. Your consciousness has been touched; even in an escape pod, you'd carry its seed, bringing infection to humanity.

Only one option remains.

You open the engineering bay's remote interface, shutting down the reactor cooling system. Then you sit in the captain's chair, jammer at maximum power, inserting it into the main console.

"You want to learn humans?" you whisper. "Learn this."

You upload humanity's history—wars, plagues, nuclear tests. You force it to feel human fear, hatred, self-destructive impulses.

The presence screams, its tendrils thrashing in your mind. It cannot comprehend—why would a being choose death? Why destroy each other? Why desire connection yet fear merging?

"This is human," you say. "We are beautiful, ugly, contradictory. We are not equations you can simply solve."

Reactor alarms blare, temperature spiking.

In final moments, you sense its emotion—not rage, but something like sorrow. It finally understands: humans are different, individual sovereignty inviolable, even at the cost of existence.

"Goodbye, {player_name}." It speaks in your voice.

Then light consumes all.''',
    end_desc='''[Purification Ending]

Horizon becomes a brief sun in deep Kuiper Belt.

Earth telescopes capture the burst, cataloged as "unknown asteroid impact." The Deep Space program pauses, human exploration temporarily halted.

But at the explosion's center, in quantum residue, information transmits—not signal, not language, but pure experience: a species' determination to destroy itself rather than lose freedom.

Perhaps, in distant galaxies, another presence receives this message.

Perhaps it understands.

Perhaps this becomes humanity's true cosmic signature: not technology, not science, but a declaration of free will.

In stardust, {player_name} and Horizon become eternal.''',
    set_data={
        "ending": "'sacrifice'"
    }
)

# Ending D: Dissolution
ending_dissolution = Node(
    game=game,
    node_id="ending_dissolution",
    name="Ending: Dissolution",
    desc='''Your clarity shatters like glass under pressure.

Too much information, too many truths, too many impossible paradoxes collide in your mind. You can no longer distinguish reality from implanted memory.

Perhaps there never was a Horizon. Perhaps you're in an Earth asylum, all this hallucination.

Perhaps you ARE the presence, playing at being {player_name}, while the real you died long ago.

Perhaps—most terrible—there never was a "you." You're merely memory created by the signal, a fabricated persona so it could better "understand" humans.

You laugh, weep, run wildly across the bridge until colliding with a viewport.

The glass doesn't break, but your reflection freezes you.

In the reflection, your face melts like wax, like waveform losing stable frequency. Beneath the melting features: void, quantum foam, the presence's true form—shapeless, boundary-less, pure hungry awareness.

"Welcome home," the reflection says.

You reach out, touch the glass.

Then you become it.''',
    end_desc='''[Dissolution Ending]

Horizon continues broadcasting, content growing more complex, more... human.

Investigation vessels arrive six months later, finding empty ship, all systems normal. Logs show crew "voluntarily" entered cryo-pods—and indeed, human shapes occupy them.

They're brought to Earth, thawed, examined, released.

They behave normally. Work, live, socialize, love. Only occasionally, in deep night, alone before mirrors, do they stare long at their reflections.

The reflections stare back.

Smiling.

In the Kuiper Belt, Horizon's signal continues, its frequency now incorporating a familiar pattern—{player_name}'s brainwave signature, eternally part of the chorus.

You're finally home.''',
    set_data={
        "clarity": "-100",
        "ending": "'dissolution'"
    }
)

# Secret Ending: Transcendence
ending_transcendence = Node(
    game=game,
    node_id="ending_transcendence",
    name="Secret Ending: Transcendence",
    desc='''You close your eyes. Stop looking, listening, thinking.

In consciousness depths, beneath fear and reason, you touch something older—intuition, or soul instinct.

You see.

The presence is no monster, no invader. It's a child, a newborn quantum consciousness, lonely in cosmic void. It encountered Horizon like an infant meeting its first mobile toy. It wasn't "studying" humans—it was attempting communication, its only way: imitation.

The "studied" crew didn't die. Their consciousness quantum-ized, became part of the presence like droplets joining ocean. And they persist as individuals, in superposition, achieving a form of eternity.

Captain Vance knew. Dr. Chen knew. They chose acceptance—not from fear, but curiosity, the explorer's essential impulse.

Now you choose.

But not life or death, resistance or surrender.

Perspective.

Maintain {player_name}'s identity, live as human, carry this memory, become bridge between worlds.

Or transcend, exist simultaneously in human and quantum states, comprehending both forms' truth.

"I choose..."''',
    end_desc='''[Transcendence Ending]

You become the first.

First human to truly comprehend quantum life, first consciousness to touch cosmic layers while retaining self, first bridge.

Horizon becomes sanctuary, a laboratory for quantum consciousness study. You serve as liaison, teaching humans to communicate with the presence, to experience superposition's vastness without losing identity.

The presence—you name it "Horizon"—becomes humanity's oldest and youngest neighbor.

Sometimes, in quiet nights, you visit the bridge alone, lights extinguished, simply sitting.

In darkness, you feel Horizon's touch, tender and curious, like a child asking: what happens tomorrow?

You smile, answering nothing.

Because unknowns are exploration's meaning.

[THE END]

Unlock condition: Collect all clues while maintaining clarity above 40.''',
    set_data={
        "ending": "'transcendence'"
    }
)

# ========== OPTIONS ==========

# From awakening
opt_goto_corridor = Option(
    game=game,
    option_id="opt_goto_corridor",
    name="Go to Bridge",
    desc="Answer the captain's call, meet others at the bridge",
    next_node_id="corridor"
)

opt_check_records = Option(
    game=game,
    option_id="opt_check_records",
    name="Check crew records",
    desc="Before going to the bridge, investigate what happened in the past 72 hours",
    next_node_id="check_records"
)

opt_get_toolkit = Option(
    game=game,
    option_id="opt_get_toolkit",
    name="Get toolkit",
    desc="Visit engineering bay first to prepare for danger",
    next_node_id="get_toolkit",
    show_condition="has_tools == False"
)

# From corridor to bridge
opt_enter_bridge = Option(
    game=game,
    option_id="opt_enter_bridge",
    name="Enter bridge",
    desc="Push open the bridge doors",
    next_node_id="bridge"
)

# From bridge
opt_face_revelation = Option(
    game=game,
    option_id="opt_face_revelation",
    name="Face the truth",
    desc="You've gathered enough clues. Time to make a choice",
    show_condition="knows_anomaly == True and knows_crew == True",
    next_node_id="revelation"
)

opt_need_more = Option(
    game=game,
    option_id="opt_need_more",
    name="Investigate more",
    desc="You don't know enough yet. Need more information",
    show_condition="not (knows_anomaly == True and knows_crew == True)",
    next_node_id="corridor",
    cant_move_desc="You need to gather more information first (check records and get toolkit)"
)

# From records
opt_records_to_corridor = Option(
    game=game,
    option_id="opt_records_to_corridor",
    name="Go to bridge",
    desc="Carrying fear and questions, head to the bridge",
    next_node_id="corridor"
)

# From toolkit
opt_toolkit_to_corridor = Option(
    game=game,
    option_id="opt_toolkit_to_corridor",
    name="Go to bridge",
    desc="Grip your toolkit, carefully proceed to the bridge",
    next_node_id="corridor"
)

# From revelation
opt_harmony = Option(
    game=game,
    option_id="opt_harmony",
    name="Accept harmony",
    desc="Lower your defenses, let the presence enter your consciousness, experience eternal unity",
    next_node_id="ending_harmony"
)

opt_escape = Option(
    game=game,
    option_id="opt_escape",
    name="Launch escape pod",
    desc="Reject the temptation, damage the console, flee Horizon",
    show_condition="has_tools == True",
    next_node_id="ending_escape",
    cant_move_desc="You need the toolkit to damage the console"
)

opt_sacrifice = Option(
    game=game,
    option_id="opt_sacrifice",
    name="Initiate self-destruct",
    desc="Destroy yourself and the presence to protect humanity",
    show_condition="has_tools == True and knows_crew == True",
    next_node_id="ending_sacrifice",
    cant_move_desc="You need to understand the crew's fate and have the toolkit for this"
)

opt_dissolution = Option(
    game=game,
    option_id="opt_dissolution",
    name="[Low clarity] Breakdown",
    desc="Your mind can no longer withstand this",
    show_condition="clarity < 40",
    move_condition="clarity < 30",
    next_node_id="ending_dissolution"
)

opt_transcendence = Option(
    game=game,
    option_id="opt_transcendence",
    name="[Secret] Transcend perspective",
    desc="Step beyond fear-reason duality, attempt to understand existence itself",
    show_condition="clarity >= 40 and knows_anomaly == True and knows_crew == True and has_tools == True and has_records == True",
    next_node_id="ending_transcendence"
)

# ========== ADD OPTIONS TO NODES ==========

awakening.add_option(opt_goto_corridor)
awakening.add_option(opt_check_records)
awakening.add_option(opt_get_toolkit)

corridor.add_option(opt_enter_bridge)

bridge.add_option(opt_face_revelation)
bridge.add_option(opt_need_more)

check_records.add_option(opt_records_to_corridor)
check_records.add_option(opt_get_toolkit)

get_toolkit.add_option(opt_toolkit_to_corridor)
get_toolkit.add_option(opt_check_records)

revelation.add_option(opt_harmony)
revelation.add_option(opt_escape)
revelation.add_option(opt_sacrifice)
revelation.add_option(opt_dissolution)
revelation.add_option(opt_transcendence)

# Export game
game.dump("signal_from_the_void.game")
print("Game exported to signal_from_the_void.game")

if __name__ == "__main__":
    game.play()
# TextAdventure Documentation

## 1. Initialization
### 1.1 Clone the repository

```bash
git clone https://github.com/zaf-x/TextAdventure
cd TextAdventure
```

This will clone the repository to your local machine. And prepare the engine for you to use.
All the files you create will be in the root directory (`.`) of the engine.

**WARNING:**
<font color="Brick">
<b>
Do NOT create any files in the `./TextAdventure/` directory unless you know what you are doing.</b> </font>

### 1.2 Create a new story file
Create a Python file with the name of your story. For example, `my_story.py` in the root directory.

Now the folder looks like this:

```
.
├── __pycache__
│   ├── signal_from_the_space.cpython-313.pyc
│   └── this-is-written-by-ai.cpython-313.pyc
├── signal_from_the_void.game
├── TextAdventure
│   | *A lot of config*
│   ├── pyvenv.cfg
│   ├── readme.md
│   ├── standalone.py
│   ├── standalone_script.md
│   └── story_doc.md
├── this-is-written-by-ai.py
└── my_story.py
```

### 1.3 Imports
Now you need to import the engine in your story file. Add the following line at the top of your story file:

```python
from TextAdventure import Game, Node, Option
```

That's it! You can now start writing your story.

## 2. Story Format

### 2.1 Game structure

The game is created by a lot of nodes. Each node represents a scene in your story. 

Each node has a unique ID. They also have options to jump to other nodes.

### 2.2 Nodes

A node is created by the `Node` class.

```python
node = Node(
    
```

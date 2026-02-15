# standalone_script_creator.py -- 制作独立的文字冒险脚本程序

import argparse
import importlib.util
import os
import base64
from TextAdventure import Game
import sys
from consts import STANDALONE_SCRIPT_MOD

class StandaloneScriptCreator:
    def __init__(self, script_path, talib_path: str = "TextAdventure", consts: str = "consts.py", out_path: str = "standalone.py"):
        self.script_path = script_path
        self.consts_path = consts
        self.talib_path = talib_path
        self.out_path = out_path

        self.script_module = None
        self.lib_cont = ''
        self.consts_cont = ''

        self.game_obj: Game = None

    def get_script_module(self):
        try:
            print(f"[INFO] Getting script module from {self.script_path}.")

            spec = importlib.util.spec_from_file_location("game_mod", self.script_path)
            self.script_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.script_module)

            sys.modules["game_mod"] = self.script_module
            print(f"[INFO] Script module {self.script_module} loaded.")
        except ImportError as e:
            print(f"[ERROR] Failed to import script module: {e}")
            print(f"[ERROR] Please check if the script module exists and is in the correct path.")
            print("Abort")
            exit(1)
        
        try:
            self.game_obj = self.script_module.game
            print(f"[INFO] Game object {self.game_obj} created.")
        except AttributeError as e:
            print(f"[ERROR] Failed to create game object: {e}")
            print(f"[ERROR] Please check if the game object exists in the script module.")
            print("Abort")
            exit(1)
        
        try:
            with open(self.talib_path, "r") as f:
                self.lib_cont = f.read()
        except FileNotFoundError as e:
            print(f"[ERROR] Failed to read library file: {e}")
            print(f"[ERROR] Please check if the library file exists and is in the correct path.")
            print("Abort")
            exit(1)
        
        try:
            with open(self.consts_path, "r") as f:
                self.consts_cont = f.read()
        except FileNotFoundError as e:
            print(f"[ERROR] Failed to read consts file: {e}")
            print(f"[ERROR] Please check if the consts file exists and is in the correct path.")
            print("Abort")
            exit(1)
    
    def merge(self):
        print("[INFO] Merging Runtime and script...")

        self.game_obj.dump("tmp.game")
        with open("tmp.game", "rb") as f:
            game_data = base64.b64encode(f.read())
        
        with open(self.out_path, "w") as f:
            f.write(STANDALONE_SCRIPT_MOD.format(consts=self.consts_cont, lib_cont=self.lib_cont, gamedata=repr(game_data)))

        print(f"[INFO] Standalone script {self.out_path} created.")
        os.remove("tmp.game")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a standalone script for a text adventure game.")
    parser.add_argument("script_path", help="Path to the script file.")
    parser.add_argument("--talib_path", default="TextAdventure.py", help="Path to the TextAdventure library file.")
    parser.add_argument("--consts", default="consts.py", help="Path to the consts file.")
    parser.add_argument("--out_path", default="standalone.py", help="Path to the output script file.")
    args = parser.parse_args()

    creator = StandaloneScriptCreator(args.script_path, args.talib_path, args.consts, args.out_path)
    creator.get_script_module()
    creator.merge()
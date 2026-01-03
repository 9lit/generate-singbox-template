import tomllib
import json
from pathlib import Path
import subprocess

def read(path:Path="", mode='r', encoding=None): 
    with open(path, mode, encoding=encoding) as f: 
        if path.suffix == ".json":
            return json.load(f)
        elif path.suffix == ".toml":
            return tomllib.load(f)
        else:
            return f.read().splitlines()

def write(data, path:Path="", mode="w", encoding="utf-8"):
    with open(path, mode, encoding=encoding) as f: 
        if path.suffix == ".json":
            json.dump(data, f, ensure_ascii=False, indent=4)
        else:
            f.write(data)

def process_script(cmd:list):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
            encoding='utf-8',errors='ignore')
        if result.returncode != 0: raise Exception(result.stderr)
    except Exception as e: exit(f"命令执行失败，检查输入{e}")

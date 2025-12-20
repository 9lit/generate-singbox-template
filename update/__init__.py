import logging
logging.basicConfig(level=logging.INFO)

import subprocess
import json

def process_script(cmd:list):
    try:
        result = subprocess.run(cmd, capture_output=True, text=True,
            encoding='utf-8',errors='ignore')
        if result.returncode != 0: raise Exception(result.stderr)
    except Exception as e: exit(f"命令执行失败，检查输入{e}")
    
def readJSON(path):
    with open(path, 'r', encoding='utf-8') as f: return json.load(f)
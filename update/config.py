from pathlib import Path
import tomllib

class FilePath:
    __work = Path().cwd()
    __root = __work.joinpath('update')
    __base = __root.joinpath("base")

    pref_file = __base.joinpath("pref.update.toml")
    output = __work.joinpath("rule-set")
    downloads = output.joinpath("downloads")


# 读取文件配置
with open(FilePath.pref_file, 'rb') as f: 
    pref_update = tomllib.load(f)



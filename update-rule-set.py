import requests
import shutil
import os
from update import logging
from update import config, enum
from update import process_script as script, readJSON

download_urls = config.pref_update[enum.Pref.downloads]

for urls in download_urls:

    # 获取下载地址， 并创建文件夹
    download_dir = config.FilePath.downloads.joinpath(urls)
    try:
        if not download_dir.exists(): 
            download_dir.mkdir(parents=True, exist_ok=True)
            logging.debug("创建成功")
    except PermissionError as e:
        logging.error("权限不足，无法创建文件夹，跳过本次下载")


    # 下载文件
    for url in download_urls[urls]:
        filename = url.split("/")[-1]
        if len(filename.split(".")) == 1:
            filename = filename + ".txt"
        path = download_dir.joinpath(filename)
        response = requests.get(url, stream=True)
        
        with open(path, 'wb') as b: b.write(response.content)
        logging.info("成功下载文件：%s"%filename)

program = config.pref_update[enum.Pref.program][enum.Pref.singbox]

""" 将下载后的文件转换为 json"""
srs_list = [f for f in config.FilePath.downloads.rglob("*") if f.is_file and f.suffix == enum.Suffix.srs]
for fsrs in srs_list:

    fjson = fsrs.with_suffix(enum.Suffix.json)
    cmd = [program, "rule-set", "decompile", fsrs, "-o", fjson]
    script(cmd)


""" 合并同组文件 """
# 清除之前产生的文件
json_list = [f for f in config.FilePath.output.iterdir() if f.is_file and f.suffix == enum.Suffix.json]

for f in json_list: os.remove(f); logging.info("清除之前产生的文件")

json_list = [f for f in config.FilePath.downloads.rglob("*") if f.is_file and f.suffix == enum.Suffix.json]

for fjson in json_list:
    group_rule_set = fjson.parent.with_suffix(enum.Suffix.json)
    group_rule_set = group_rule_set.parent.parent.joinpath(group_rule_set.name)
    if group_rule_set.exists():
        old_content = readJSON(group_rule_set)
        new_content = readJSON(fjson)

        new_rules = new_content[enum.RuleSet.rules][0]
        old_rules = old_content[enum.RuleSet.rules][0]
        for rule in new_rules:
            if rule in old_content:
                old_rules[rule] = list(set(new_rules[rule] + old_rules[rule]))
            else:
                old_rules[rule] = new_rules[rule]

    else:
        shutil.copy(fjson, group_rule_set)
        logging.info(f"目标文件不存在， 复制文件{fjson.name} 到 {group_rule_set.name}")


"""将文件编码"""

json_list = [f for f in config.FilePath.output.iterdir() if f.is_file and f.suffix == enum.Suffix.json]
for fjson in json_list:

    fsrs = fjson.with_name(f'site-{fjson.name.replace("_","-")}').with_suffix(enum.Suffix.srs)
    cmd = [program, "rule-set", "compile", fjson, "-o", fsrs]
    script(cmd)

"""将 adguard 编码为 srs 文件"""

all_file = config.FilePath.output.rglob("*")

for f in all_file:
    if f.is_file and f.parent.name == enum.groups.adguard: adguard = f

binary_adguard = config.FilePath.output.joinpath(enum.groups.adguard).with_suffix(enum.Suffix.srs)

cmd = [program, "rule-set", "convert", "--type", "adguard", "--output", binary_adguard, adguard]
script(cmd)
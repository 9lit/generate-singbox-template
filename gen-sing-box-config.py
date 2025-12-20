from singbox import config, enum
from singbox import group_sing_box_tag
from singbox import set_inline, new_sing_box
from singbox import UpdateRules, deepcopy
from singbox import writeJSON
import tomllib
import requests
import logging

logging.basicConfig(level=logging.INFO)

# 重命名枚举
element = enum.Element
# 读取文件配置
with open(config.FilePath.pref_example, 'rb') as f: 
    pref_example = tomllib.load(f)

dns = pref_example[element.dns]
route = pref_example[element.route]

set_inline(route)
logging.info(f"创建文件{config.FilePath.outinline.name}, 并生成内部规则集。")

"""获取分组后的 rule_set 标签"""
content = new_sing_box()
groups = group_sing_box_tag(content)

"""更新 dns.rules 配置"""
update_dns_rules = UpdateRules(content, element.dns)

# 获取模板

dns_rules = dns[element.rules]
dns_server = dns[element.server]
# 配置 proxy dirct block 内容
for g in groups:
    dns_rules = deepcopy(dns_rules)
    dns_rules[element.rule_set] = groups[g]
    dns_rules[element.server] = dns_server[g]
    update_dns_rules.rules(dns_rules)

logging.info(f"创建 sing-box DNS规则")
update_dns_rules.update()
logging.info(f"更新文件{config.FilePath.outinline.name}")

"""更新 route.rules 配置"""
update_route_rules = UpdateRules(content, element.route)
# 获取模板
route_rules = route[element.rules]
# 配置 proxy dirct block 内容
for g in groups:
    route_rules = deepcopy(route_rules)
    route_rules[g][element.rule_set] = groups[g]
    update_route_rules.rules(route_rules[g])

# 更新 sing-box inline 文件
logging.info(f"创建 sing-box 路由规则")
update_dns_rules.update()
logging.info(f"更新文件{config.FilePath.outinline.name}")

""" 将 rule-set 替换为远程规则集 并生成新的文件"""
# pref_remote = route[element.rule_set][element.remote]
# remote_rule_set = []
# content = new_sing_box()

# # 获取仓库文件列表
# response = requests.get(config.Github.api)
# if response.status_code == 200: github_data = response.json()
# else: logging.error("github 仓库信息获取失败"); exit()

# # GIthub 枚举信息重命名
# enum_github = enum.Github
# # 格式化仓库文件信息
# for github_item in github_data:
#     name = github_item[enum_github.name]
#     download_url = github_item[enum_github.download_url]
#     name, suffix = name.split(".")
#     if suffix != 'srs': continue

#     remote = deepcopy(pref_remote)
#     remote[element.tag] = name.replace("_","-")
#     remote[element.url] = download_url
#     remote_rule_set.append(remote)

# content[element.route][element.rule_set] = remote_rule_set

# writeJSON(content, config.FilePath.outremote)
# logging.info(f"根据文件{config.FilePath.outinline.name}, 更新规则集， 并生成文件{config.FilePath.outremote.name}")
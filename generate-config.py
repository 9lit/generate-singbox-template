import base
import base.config
import base.enum

def update(tag):

    group = all_group[tag]

    # 更新 route rule-set
    rule_set = {
        enum.config.type: group[enum.config.type],
        enum.config.tag: tag,
        enum.config.format: group[enum.config.format],
        enum.url: after_config[tag][enum.url] 
        }
        
    before_config[enum.config.route][enum.rule_set].append(rule_set)

    # 更新 route rules
    route_rules = {
        enum.config.action: group[enum.config.action],
        enum.rule_set: tag,
        enum.config.outbound: group[enum.config.outbound]
        }
    
    if tag == enum.direct:
        route_rules[enum.config.ip_is_private]  = True
        
        try: route_rules[enum.config.domain_suffix] = group[enum.config.domain_suffix]
        except KeyError: pass

    before_config[enum.config.route][enum.config.rules].append(route_rules)

    # 更新 dns rules    
    if tag not in [enum.direct] + block: return
    dns_rules = {
        enum.rule_set : tag,
        enum.config.action : group[enum.config.action],
        enum.config.server : group[enum.config.server]
        }
    
    before_config[enum.config.dns][enum.config.rules].append(dns_rules)

def generate_config():

    version = pref_config[enum.version]
    out_file = path.out_config.joinpath(f"singbox_config_{version}.json")
    base.write(before_config, out_file, encoding='utf-8')

def run():

    for group_tag in after_config.keys(): update(group_tag)

    generate_config()

    print("sing-box 配置文件已生成")

if __name__ == "__main__":
    enum = base.enum

    config = base.config
    
    path = config.Path
    after_config = path.after_config

    content = config.Content
    pref_config = content.pref_config
    all_group = pref_config[enum.group.group]
    
    before_config = content.template_config
    after_config = content.after_config

    block = [enum.group.adguard, enum.group.ads]
    run()
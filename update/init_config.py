from pathlib import Path
import update

Default = update.Default
File = update.File
log = update.Log()

config_text = Default.config.py_text
config_content = File.Read(Default.config.toml_file).toml()
py_config = Default.config.py_file
outfile = Default.outfile
env = Path.cwd()

def splicing_config_content(content:str, is_empty=True, indent=4):
    global config_text
    empty = " " if is_empty else ""
    empty = empty * indent
    config_text += f"{empty}{content}\n"

    if "class" in content:
        log.debug("生成配置 %s"%content)
    else:
        log.debug(content)

def generate_file_config(class_content:dict):
    """生成 project 类的配置项"""

    splicing_config_content("class File:", is_empty=False)

    # 获取根目录
    try:
        root = class_content['root']
    except KeyError:
        root = outfile.root
        log.debug("没有指定根目录地址，使用默认根目录%s"%Path(root))
    root = Path(root)

    if not root.is_absolute():
        root = env.joinpath(root)

    splicing_config_content(f"root = r'{root}'")

    try:
        prefile = class_content['prefile']
        if not Path(prefile).is_absolute():
            prefile = env.joinpath(prefile)

        splicing_config_content(f"prefile = r'{prefile}'")
    except:
        exit("缺少模板文件")


def generate_requests_config(requests_content:dict):
    """
    generate_requests_config 的 Docstring
    将配置项写入到 config.py 文件中
    class requests:
        headers = {}
        class url:
            __generate_group_url()

    :param requests_content: dict
        requests_content: {
            "header": "Accept": "application/json",
            "url": {
                "site-miceosoft": [
                    "https://raw.githubusercontent.com/SagerNet/sing-geosite/rule-set/geosite-microsoft.srs"
                ],
                "site-github": [
                	"https://raw.githubusercontent.com/SagerNet/sing-geosite/rule-set/geosite-github.srs"
                ] 
            },
        }
    :return None
    """
    def __generate_group_url(greoup_url_list:dict):
        """
        __generate_group_url 的 Docstring
        将配置写入到配置文件中 config.py
        class url:
            site_microsoft = [a_url, b_url]
            site_microsoft_cn = [c_url]
        
        :param greoup_url_list: dict
        url = {
            "site-microsoft" : [a_url, b_url],
            "site-microsoft-cn" : [c_url] 
        }
        :return None
        """
        splicing_config_content("class url:", indent=4)
        for group_name in greoup_url_list:
            url_list = greoup_url_list[group_name]
            group_name = group_name.replace("-", "_")
            splicing_config_content(f"{group_name} = {url_list}", indent=8)
        
    
    if not requests_content: 
        log.warn("配置项 requests 没有内容， 停止生成 requests 类"); return
    splicing_config_content("class Requests:", is_empty=False)
    
    # 生成 requests 配置 
    for key in requests_content:
        # 生成 url 配置
        if key == 'url':
            greoup_url_list = requests_content[key]
            __generate_group_url(greoup_url_list)
        # 生成 header 配置
        elif key == "headers":
            headers = requests_content[key]
            splicing_config_content(f"{key} = {headers}")
        
def generate_proxy_config(proxy_content):
    
    try:
        flag = proxy_content['flag']
        url = proxy_content['url']
        port =proxy_content['port']
    except KeyError:
        return 

    if not flag: return

    splicing_config_content("class Proxy:", is_empty=False)

    url = "'http://%s:%s'" % (url, port)
    content = '''import os
    os.environ["HTTP_PROXY"] = {0}
    os.environ["HTTPS_PROXY"] = {0}
    os.environ["http_proxy"] = {0}
    os.environ["https_proxy"] = {0}\n'''.format(url)
    splicing_config_content(content)


def generate_program_config(program_content):

    if not program_content: return
    splicing_config_content("class Program:", is_empty=False)
    for param in program_content:
        param_path = program_content[param]
        param = param.replace('-', '_')
        splicing_config_content(f"{param} = '{param_path}'")

def generate_version_config(version_content):
    if not version_content: return
    
    ver = 'num'
    splicing_config_content("class Version:", is_empty=False)
    
    try:
        version = version_content[ver]
    except KeyError:
        version = "Unknown"

    splicing_config_content(f"{ver} = {version}")

log.info("初始化 update sing-box config 配置文件")


for name in config_content:
    class_content = config_content[name]
    func_name = f'generate_{name.lower()}_config'
    try:
        eval(func_name)(class_content)
        log.info(f"生成类 {name}")
    except NameError:
        pass

File.write(py_config).common(config_text)
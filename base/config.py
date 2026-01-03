import pathlib
import base
import logging
logging.basicConfig(level=logging.INFO)

class Path:
    root = pathlib.Path.cwd()
    base = root.joinpath("base")
    template_config = base.joinpath("template.json")
    pref_config = base.joinpath("pref_config.toml")

    outpath = root.joinpath("output")
    downloads = outpath.joinpath("download")
    out_config = outpath.joinpath("config")
    after_config = out_config.joinpath("set_config.json")

class Content:
    pref_config = base.read(Path.pref_config, mode='rb')
    template_config = base.read(Path.template_config, encoding='utf-8')
    if Path.after_config.exists():
        after_config = base.read(Path.after_config, encoding='utf-8')
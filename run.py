from update import init_config, main

main.Downloads().download()

main.Convert.tosource()

main.MergeJsonConfig().merge()

main.Convert.to_binary()

g = main.Generate()
g.inline()
g.dns()
g.update()
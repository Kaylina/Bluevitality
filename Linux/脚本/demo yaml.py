#!/usr/bin/env python
# need pip install pyyaml

import yaml

a = yaml.load("""
name: Vorlin Laruknuzum
sex: Male
class: Priest
title: Acolyte
hp: [32, 71]
sp: [1, 13]
gold: 423
inventory:
- a Holy Book of Prayers (Words of Wisdom)
- an Azure Potion of Cure Light Wounds
- a Silver Wand of Wonder
""")

print a['inventory'][1]     # 字典
print yaml.dump(a)          # 把字典生成yaml文件
yaml.load_all               # 生成迭代器

print yaml.dump({'name': "The Cloak 'Colluin'", 'depth': 5, 'rarity': 45, \
'weight': 10, 'cost': 50000, 'flags': ['INT', 'WIS', 'SPEED', 'STEALTH']})

from PayLine import PayLine
from State import State
from Symbol import Symbol

STATE_NORMAL = State("通常")

# 図柄
redseven = Symbol("赤７", "redseven_1.png")
blueseven = Symbol("青７", "blueseven_1.png")
bar = Symbol("ＢＡＲ", "bar_1.png")
cherry = Symbol("チェリー", "cherry_1.png")
watermelon = Symbol("スイカ", "watermelon_1.png")
bell = Symbol("ベル", "bell_1.png")
replay = Symbol("リプレイ", "replay_1.png")

# 左リール配列
REEL_SYMBOLPATTERN_L = [
    watermelon,
    cherry,
    redseven,
    bell,
    replay,
    watermelon,
    blueseven,
    bell,
    replay,
    watermelon,
    redseven,
    cherry,
    bar,
    bell,
    replay,
    watermelon,
    blueseven,
    blueseven,
    blueseven,
    bell,
    replay,
]

# 中リール配列
REEL_SYMBOLPATTERN_C = [
    cherry,
    watermelon,
    redseven,
    replay,
    bell,
    cherry,
    watermelon,
    cherry,
    replay,
    bell,
    cherry,
    blueseven,
    replay,
    bell,
    bar,
    cherry,
    replay,
    bell,
    cherry,
    replay,
    bell,
]

# 右リール配列
REEL_SYMBOLPATTERN_R = [
    replay,
    cherry,
    redseven,
    watermelon,
    bell,
    replay,
    bar,
    watermelon,
    bell,
    replay,
    cherry,
    watermelon,
    bell,
    replay,
    blueseven,
    watermelon,
    bell,
    replay,
    cherry,
    watermelon,
    bell,
]

# 有効ライン
PAYLINE_UPPER = PayLine("上段", payline=(0, 0, 0))
PAYLINE_MIDDLE = PayLine("中段", payline=(1, 1, 1))
PAYLINE_LOWER = PayLine("下段", payline=(2, 2, 2))
PAYLINE_RIGHTUP = PayLine("右上がり", payline=(2, 1, 0))
PAYLINE_RIGHTDOWN = PayLine("右下がり", payline=(0, 1, 2))

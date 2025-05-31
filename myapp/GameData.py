import os

# ゲームデータフォルダ名
GAMEDATA_FOLDER_NAME: str = "assets"
# ゲーム画像フォルダ名
IMAGE_FOLDER_NAME: str = "images"

# 現在のスクリプトファイルのディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))
# 1つ上の階層のディレクトリパスを取得
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
# ゲーム画像ディレクトリ
IMAGE_DIRECTORY: str = os.path.join(
    parent_dir, GAMEDATA_FOLDER_NAME, IMAGE_FOLDER_NAME
)

# ゲーム画面幅
SCREEN_WIDTH: int = 800
# ゲーム画面高さ
SCREEN_HEIGHT: int = 600
# ゲームタイトル
GAME_TITLE: str = "test"

# フォント
FONT_WANPAKURUIKA = "わんぱくルイカ-０７"
# フレームレート指定
FRAMERATE_LIMIT: int | None = None

# 図柄画像幅
SYMBOL_WIDTH: int = 150
# 図柄画像高さ
SYMBOL_HEIGHT: int = 70
# リール図柄数
REEL_SYMBOL_LENGTH: int = 21
# リール画像幅
REEL_WIDTH: int = SYMBOL_WIDTH
# リール画像高さ
REEL_HEIGHT: int = SYMBOL_HEIGHT * REEL_SYMBOL_LENGTH

# 各リール間の間隔
REEL_SPACE_BETWEEN_REELS: int = int(SYMBOL_WIDTH / 6)
# 各リールの枠外の描画範囲
REEL_OUTSIDE_DRAW_RANGE: int = int(SYMBOL_HEIGHT / 6)

# リール描画共通オフセット
REEL_DRAW_COMMON_OFFSET_X: int = int(SCREEN_WIDTH / 2 - SYMBOL_WIDTH / 2)
REEL_DRAW_COMMON_OFFSET_Y: int = int(SCREEN_HEIGHT / 2 - SYMBOL_HEIGHT / 2)

# リール描画固有オフセット
REEL_DRAW_LEFT_OFFSET_X: int = (REEL_SPACE_BETWEEN_REELS + SYMBOL_WIDTH) * -1
REEL_DRAW_CENTER_OFFSET_X: int = 0
REEL_DRAW_RIGHT_OFFSET_X: int = REEL_SPACE_BETWEEN_REELS + SYMBOL_WIDTH

# リール枠上端
REEL_FRAME_TOP: int = int(
    REEL_HEIGHT - SYMBOL_HEIGHT - REEL_OUTSIDE_DRAW_RANGE
)
# リール枠下端
REEL_FRAME_BOTTOM: int = int(SYMBOL_HEIGHT * 2 + REEL_OUTSIDE_DRAW_RANGE)


# UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
UIDRAW_CONST_A: int = int(REEL_SPACE_BETWEEN_REELS // 1.5)
# UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
UIDRAW_CONST_B: int = int(REEL_SPACE_BETWEEN_REELS // 2)


# リール回転速度[r/sec]
REEL_SPEED: float = 0.8
# BET処理時にBETを行う間隔[sec]
BET_INTERVAL: float = (1 / 30) * 2
# リールウェイト時間[sec]
REELWAIT_TIME: float = 4.1

# 色
COLORS: dict[str, tuple[int, int, int]] = {
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "SILVER": (192, 192, 192),
    "GRAY": (128, 128, 128),
    "RED": (255, 0, 0),
    "MAROON": (128, 0, 0),
    "YELLOW": (255, 255, 0),
    "OLIVE": (128, 128, 0),
    "LIME": (0, 255, 0),
    "GREEN": (0, 128, 0),
    "AQUA": (0, 255, 255),
    "TEAL": (0, 128, 128),
    "BLUE": (0, 0, 255),
    "NAVY": (0, 0, 128),
    "FUCHSIA": (255, 0, 255),
    "PURPLE": (128, 0, 128),
}

# 有効BET数: 最小
VALIDBET_MIN: int = 1
# 有効BET数: 最大
VALIDBET_MAX: int = 3

# リール位置: 上段
REEL_POSITION_TOP: int = 0
# リール位置: 中段
REEL_POSITION_MIDDLE: int = 1
# リール位置: 下段
REEL_POSITION_BOTTOM: int = 2

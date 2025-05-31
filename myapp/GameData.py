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
IMAGE_DIRECTORY: str = os.path.join(parent_dir, GAMEDATA_FOLDER_NAME, IMAGE_FOLDER_NAME)

# ゲーム画面幅
SCREEN_WIDTH: int = 800
# ゲーム画面高さ
SCREEN_HEIGHT: int = 600
# ゲームタイトル
GAME_TITLE: str = "test"

# フォント
FONT_WANPAKURUIKA = "わんぱくルイカ-０７"

# フレームレート指定
FRAMERATE: int | None = None
# より高品質な時間管理(CPU使用率増加)
HIGHQUALITY_TIMECALC: bool = True

# 図柄画像幅
SYMBOL_WIDTH: int = 150
# 図柄画像高さ
SYMBOL_HEIGHT: int = 70
# リール図柄数
SYMBOLARRAY_LENGTH: int = 21
# リール画像幅
REEL_WIDTH: int = SYMBOL_WIDTH
# リール画像高さ
REEL_HEIGHT: int = SYMBOL_HEIGHT * SYMBOLARRAY_LENGTH

# リール描画用定数A (各リールの左右に確保する間隔)
REELDRAW_CONST_A: int = int(SYMBOL_WIDTH // 6)
# リール描画用定数B (各リールの上下に確保する間隔)
REELDRAW_CONST_B: int = int(SYMBOL_WIDTH // 6)
# リール描画用定数C (各リールの枠上/枠下の描画範囲)
REELDRAW_CONST_C: int = int(SYMBOL_HEIGHT // 6)

# UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
UIDRAW_CONST_A: int = int(REELDRAW_CONST_A // 1.5)
# UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
UIDRAW_CONST_B: int = int(REELDRAW_CONST_A // 2)

# リール回転速度[r/sec]
REEL_SPEED: float = 0.8
# BET処理時にBETを行う間隔[sec]
BET_INTERVAL: float = (1 / 30) * 2
# リールウェイト時間[sec]
REELWAIT_TIME: float = 4.1

# 色
RGB_WHITE: tuple[int, int, int] = (255, 255, 255)
RGB_BLACK: tuple[int, int, int] = (0, 0, 0)
RGB_SILVER: tuple[int, int, int] = (192, 192, 192)
RGB_GRAY: tuple[int, int, int] = (128, 128, 128)
RGB_RED: tuple[int, int, int] = (255, 0, 0)
RGB_MAROON: tuple[int, int, int] = (128, 0, 0)
RGB_YELLOW: tuple[int, int, int] = (255, 255, 0)
RGB_OLIVE: tuple[int, int, int] = (128, 128, 0)
RGB_LIME: tuple[int, int, int] = (0, 255, 0)
RGB_GREEN: tuple[int, int, int] = (0, 128, 0)
RGB_AQUA: tuple[int, int, int] = (0, 255, 255)
RGB_TEAL: tuple[int, int, int] = (0, 128, 128)
RGB_BLUE: tuple[int, int, int] = (0, 0, 255)
RGB_NAVY: tuple[int, int, int] = (0, 0, 128)
RGB_FUCHSIA: tuple[int, int, int] = (255, 0, 255)
RGB_PURPLE: tuple[int, int, int] = (128, 0, 128)


# ゲーム定数
# 最小有効BET数
VALIDBET_MIN: int = 1
# 最大有効BET数
VALIDBET_MAX: int = 3

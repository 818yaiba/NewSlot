import sys
import time

import pygame
from cv2.typing import MatLike

import GameData
import SlotData
from Reel import Reel


class Slot:
    """
    スロットマシン

    Attributes
    ----------
    credit : int
        クレジット数
    payout : int
        払出クレジット数
    bet : int
        BET数
    validbet : list[int]
        有効BET数
    payline : list[PayLine]
        入賞ライン
    role : list[Role]
        成立役
    reel : list[Reel]
        リール ([0]: 左リール, [1]: 中リール, [2]:右リール)
    start : bool
        遊技可能状態
    replay : bool
        再遊技可能状態
    gaming : bool
        遊技状態
    setting : int
        設定
    """

    def __init__(self, setting: int | None = None):
        self._credit = 0
        self._payout = 0
        self._bet = 0
        self._validbet: list[int] = [3]
        # self._payline: list[payline] = None
        self._roles = None
        self._reel = [
            Reel("REEL_L", SlotData.REEL_SYMBOLPATTERN_L),
            Reel("REEL_C", SlotData.REEL_SYMBOLPATTERN_C),
            Reel("REEL_R", SlotData.REEL_SYMBOLPATTERN_R),
        ]
        self._start: bool = False
        self._replay: bool = False
        self._wait: bool = False
        self._gaming: bool = False
        self._setting = setting
        self._beting: bool = False
        self._targetbet: int = False
        self._latest_betstart_time: float = time.perf_counter()

        self.internalState = SlotData.STATE_NORMAL
        self.ATState = SlotData.STATE_NORMAL
        self.NaviState = SlotData.STATE_NORMAL
        self.RTState = SlotData.STATE_NORMAL

    # ボタン処理
    def onebet_keydown(self):
        """ONEBETボタンを押した場合の処理"""
        # ONEBETボタン状態 = 押下
        self._onebet()

    def onebet_keyup(self):
        """ONEBETボタンを離した場合の処理"""
        # ONEBETボタン状態 = 開放
        pass

    def maxbet_keydown(self):
        """MAXBETボタンを押した場合の処理"""
        # MAXBETボタン状態 = 押下
        self._maxbet()

    def maxbet_keyup(self):
        """MAXBETボタンを離した場合の処理"""
        # MAXBETボタン状態 = 開放
        pass

    def lever_keydown(self):
        """LEVERボタンを押した場合の処理"""
        # LEVERボタン状態 = 押下
        self._leveron()

    def lever_keyup(self):
        """LEVERボタンを離した場合の処理"""
        # LEVERボタン状態 = 開放
        pass

    def leftreelstop_keydown(self):
        """左リール停止ボタンを押した場合の処理"""
        # 左リール停止ボタン状態 = 押下
        self._leftreelstop()

    def leftreelstop_keyup(self):
        """左リール停止ボタンを離した場合の処理"""
        # 左リール停止ボタン状態 = 開放
        pass

    def centerreelstop_keydown(self):
        """中リール停止ボタンを押した場合の処理"""
        # 中リール停止ボタン状態 = 押下
        self._centerreelstop()

    def centerreelstop_keyup(self):
        """中リール停止ボタンを離した場合の処理"""
        # 中リール停止ボタン状態 = 開放
        pass

    def rightreelstop_keydown(self):
        """右リール停止ボタンを押した場合の処理"""
        # 右リール停止ボタン状態 = 押下
        self._rightreelstop()

    def rightreelstop_keyup(self):
        """右リール停止ボタンを離した場合の処理"""
        # 右リール停止ボタン状態 = 開放
        pass

    # イベント処理
    def _onebet(self):
        """ONEBET処理"""
        if not self._is_gaming():
            current_bet = self._bet
            current_validbet_max = self._get_current_validbet_max()
            if current_bet != current_validbet_max:
                self._beting = True
                self._targetbet = current_bet + 1
                self._latest_bet_interval_time = GameData.BET_INTERVAL
            else:
                self._beting = True
                self._targetbet = 1
                self._latest_bet_interval_time = GameData.BET_INTERVAL

    def _maxbet(self):
        """MAXBET処理"""
        if not self._is_gaming():
            current_bet = self._bet
            current_validbet_max = self._get_current_validbet_max()
            if current_bet != current_validbet_max:
                self._beting = True
                self._targetbet = current_validbet_max
                self._latest_bet_interval_time = GameData.BET_INTERVAL

    def _leveron(self):
        """遊技開始処理(仮)"""
        if self._bet in self._validbet:
            self._reel[0].reelstart()
            self._reel[1].reelstart()
            self._reel[2].reelstart()
        # if '遊技可能()?':
        #     if 'リールウェイト中()?':
        #         # 遊技開始予約処理()
        #         pass
        #     else:
        #         # 遊技開始()
        #         pass

    def _leftreelstop(self):
        """左リール停止処理"""
        if "左リール回転中()?":
            if "左リールに停止指示がない()?":
                # 左リール停止指示()
                pass

    def _centerreelstop(self):
        """中リール停止処理"""
        if "中リール回転中()?":
            if "中リールに停止指示がない()?":
                # 中リール停止指示()
                pass

    def _rightreelstop(self):
        """右リール停止処理"""
        if "右リール回転中()?":
            if "右リールに停止指示がない()?":
                # 右リール停止指示()
                pass

    def _get_current_validbet_max(self) -> int:
        """現在の有効BET数の最大値を返す"""
        validbet_max = max(self._validbet)

        return validbet_max

    def _bet_process(self, dt: float):
        """BET処理(仮)

        Parameters
        ----------
        dt: float
            前回からの経過時間
        """
        if self._beting:
            self._latest_bet_interval_time -= dt
            if self._latest_bet_interval_time <= 0:
                current_validbet_max = self._get_current_validbet_max()
                # A
                if self._bet != current_validbet_max:
                    self._bet += 1
                else:
                    self._bet = 1

                self._latest_bet_interval_time += GameData.BET_INTERVAL
                # ここで本来はAに戻る必要がある。←forでよさそう

                if self._bet == self._targetbet:
                    self._beting = False

    def _is_gaming(self):
        """現在遊技中であればTrueを返す"""
        # 以下は仮のコード (self._gamingが仮)
        # 最終的には、この関数内で遊技中であるか判定するようにしたい
        if self._gaming is True:
            result = True
        else:
            result = False

        return result

    # 状態更新
    def update(self, dt: float):
        """スロット状態を更新する

        Parameters
        ----------
        dt: float
            前回からの経過時間
        """

        self._bet_process(dt)

        # リール状態更新
        self._reel[0].update(dt)
        self._reel[1].update(dt)
        self._reel[2].update(dt)

    @property
    def reel(self) -> list[Reel]:
        return self._reel

    @property
    def credit(self) -> int:
        return self._credit

    @property
    def payout(self) -> int:
        return self._payout

    @property
    def bet(self) -> int:
        return self._bet

    @property
    def replay(self) -> bool:
        return self._replay

    @property
    def start(self) -> bool:
        return self._start

    @property
    def wait(self) -> bool:
        return self._wait


class BetManager:
    """
    BET管理を行う

    Attributes
    ----------
    id : int
        ゲームID
    name : str
        ゲーム名
    """

    def __init__(self) -> None:
        self._beting: bool = False
        self._targetbet: int = False
        self._latest_betstart_time: float = time.perf_counter()


class Game:
    """
    ゲーム

    Attributes
    ----------
    id : int
        ゲームID
    name : str
        ゲーム名
    """

    _Id: int = 0

    def __init__(self, name: str):
        """
        Parameters
        ----------
        name : str
            ゲーム名
        """
        self._id: int = Reel._Id
        Reel._Id += 1
        self._name: str = name

        # ゲーム画面幅, 高さ
        self._screen_width: int = GameData.SCREEN_WIDTH
        self._screen_height: int = GameData.SCREEN_HEIGHT

        # pygame
        pygame.init()
        self._screen = pygame.display.set_mode(
            (self._screen_width, self._screen_height)
        )
        pygame.display.set_caption(self._name)
        self._clock = pygame.time.Clock()
        self._previous_time: float = time.perf_counter()
        self._timedelta: float = time.perf_counter() - self._previous_time

        self._systemfont_name = GameData.FONT_WANPAKURUIKA
        self._system_font = pygame.font.SysFont(self._systemfont_name, 16)

        # フレームレート指定
        self._framerate: int | None = GameData.FRAMERATE
        # より高品質な時間管理のオプション
        self._highquality_timecalc: bool = GameData.HIGHQUALITY_TIMECALC

        # slot
        self._slot = Slot()

        # リール描画用リール画像 (OpenCV → pygame)
        self._reelimg_l = self._convert_cv2_to_pg(self._slot.reel[0].reelimage)
        self._reelimg_c = self._convert_cv2_to_pg(self._slot.reel[1].reelimage)
        self._reelimg_r = self._convert_cv2_to_pg(self._slot.reel[2].reelimage)

    def _convert_cv2_to_pg(self, cv2_image: MatLike) -> pygame.Surface:
        """OpenCVの画像をPygame用に変換"""
        # BGR(OpenCV) → RGB(pygame)
        img = cv2_image[:, :, ::-1]
        # 高さ, 幅, 色数(OpenCV) → 幅, 高さ(pygame)
        shape = img.shape[1::-1]
        # image(pygame)
        img = pygame.image.frombuffer(img.tobytes(), shape, "RGB").convert()

        return img

    def game_quit(self):
        """ゲームを終了する"""
        pygame.quit()
        sys.exit()

    def _gameevent_update(self):
        """イベントを検知し更新する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # ゲーム終了
                self.game_quit()
            elif event.type == pygame.KEYDOWN:
                self._keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._keyup_event(event)

    def _keydown_event(self, event: pygame.event.Event):
        """コメント"""
        if event.key == pygame.K_1:
            # ONEBET BUTTON
            self._slot.onebet_keydown()
        elif event.key == pygame.K_RSHIFT:
            # MAXBET BUTTON
            self._slot.maxbet_keydown()
        elif event.key == pygame.K_RCTRL:
            # LEVER-ON BUTTON
            self._slot.lever_keydown()
        else:
            if event.key == pygame.K_LEFT:
                # LEFTREEL-STOP BUTTON
                self._slot.leftreelstop_keydown()
            if event.key == pygame.K_DOWN:
                # CENTERREEL-STOP BUTTON
                self._slot.centerreelstop_keydown()
            if event.key == pygame.K_RIGHT:
                # RIGHTREEL-STOP BUTTON
                self._slot.rightreelstop_keydown()

    def _keyup_event(self, event: pygame.event.Event):
        """コメント"""
        if event.key == pygame.K_1:
            # ONEBET BUTTON
            self._slot.onebet_keyup()
        elif event.key == pygame.K_RSHIFT:
            # MAXBET BUTTON
            self._slot.maxbet_keyup()
        elif event.key == pygame.K_RCTRL:
            # LEVER-ON BUTTON
            self._slot.lever_keyup()
        else:
            if event.key == pygame.K_LEFT:
                # LEFTREEL-STOP BUTTON
                self._slot.leftreelstop_keyup()
            if event.key == pygame.K_DOWN:
                # CENTERREEL-STOP BUTTON
                self._slot.centerreelstop_keyup()
            if event.key == pygame.K_RIGHT:
                # RIGHTREEL-STOP BUTTON
                self._slot.rightreelstop_keyup()

    def _gameclock_update(self):
        """clockを更新する"""
        if self._highquality_timecalc is True:
            # 高品質な時間管理が有効の場合、tick_busy_loop()を使用する
            if self._framerate is not None:
                # フレームレート指定がある場合、フレームレート制限を行う
                self._clock.tick_busy_loop(self._framerate)
            else:
                self._clock.tick_busy_loop()
        else:
            if self._framerate is not None:
                # フレームレート指定がある場合、フレームレート制限を行う
                self._clock.tick(self._framerate)
            else:
                self._clock.tick()

    def _timedelta_update(self):
        """前回からの経過時間を更新する"""
        self._timedelta = time.perf_counter() - self._previous_time
        self._previous_time = time.perf_counter()

    def _game_update(self):
        """ゲーム状態を更新する"""
        self._slot.update(self._timedelta)

    def _gamescreen_update(self):
        """Surfaceオブジェクトを更新する"""
        self._screen.fill(color=GameData.RGB_BLACK)
        self._gamereel_draw()
        self._gameui_draw()

    def _gamereel_draw(self):
        """リールを描画する"""
        self._left_reel_draw()
        self._center_reel_draw()
        self._right_reel_draw()
        self._upper_reelcover_draw()
        self._lower_reelcover_draw()

    def _left_reel_draw(self):
        """左リールを描画する"""
        # 左リール座標
        currentcoord_leftreel = self._slot.reel[0].currentcoord

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の高さ
        reel_height = GameData.REEL_HEIGHT
        # リール画像(全体)の幅
        symbol_width = GameData.SYMBOL_WIDTH
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # リール描画用定数A (各リールの左右に確保する間隔)
        reeldraw_const_a = GameData.REELDRAW_CONST_A
        # リール描画用定数C (各リールの枠上/枠下の描画範囲)
        reeldraw_const_c = GameData.REELDRAW_CONST_C

        # リール描画
        # 左リール
        if 0 <= currentcoord_leftreel and currentcoord_leftreel <= (
            symbol_height * 2 + reeldraw_const_c
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_l,
                (
                    screen_width / 2 - symbol_width * 3 / 2 - reeldraw_const_a,
                    currentcoord_leftreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_l,
                (
                    screen_width / 2 - symbol_width * 3 / 2 - reeldraw_const_a,
                    currentcoord_leftreel + screen_height / 2 - symbol_height / 2,
                ),
            )
        elif (
            symbol_height * 2 + reeldraw_const_c < currentcoord_leftreel
            and currentcoord_leftreel <= reel_height - symbol_height - reeldraw_const_c
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_l,
                (
                    screen_width / 2 - symbol_width * 3 / 2 - reeldraw_const_a,
                    currentcoord_leftreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
        else:
            # 上側画像
            self._screen.blit(
                self._reelimg_l,
                (
                    screen_width / 2 - symbol_width * 3 / 2 - reeldraw_const_a,
                    currentcoord_leftreel
                    - reel_height * 2
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_l,
                (
                    screen_width / 2 - symbol_width * 3 / 2 - reeldraw_const_a,
                    currentcoord_leftreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )

    def _center_reel_draw(self):
        """中リールを描画する"""
        # 中リール座標
        currentcoord_centerreel = self._slot.reel[1].currentcoord

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の高さ
        reel_height = GameData.REEL_HEIGHT
        # リール画像(全体)の幅
        symbol_width = GameData.SYMBOL_WIDTH
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # リール描画用定数C (各リールの枠上/枠下の描画範囲)
        reeldraw_const_c = GameData.REELDRAW_CONST_C

        # リール描画
        # 中リール
        if 0 <= currentcoord_centerreel and currentcoord_centerreel <= (
            symbol_height * 2 + reeldraw_const_c
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_c,
                (
                    screen_width / 2 - symbol_width / 2,
                    currentcoord_centerreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_c,
                (
                    screen_width / 2 - symbol_width / 2,
                    currentcoord_centerreel + screen_height / 2 - symbol_height / 2,
                ),
            )
        elif (
            symbol_height * 2 + reeldraw_const_c < currentcoord_centerreel
            and currentcoord_centerreel
            <= (reel_height - symbol_height - reeldraw_const_c)
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_c,
                (
                    screen_width / 2 - symbol_width / 2,
                    currentcoord_centerreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
        else:
            # 上側画像
            self._screen.blit(
                self._reelimg_c,
                (
                    screen_width / 2 - symbol_width / 2,
                    currentcoord_centerreel
                    - reel_height * 2
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_c,
                (
                    screen_width / 2 - symbol_width / 2,
                    currentcoord_centerreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )

    def _right_reel_draw(self):
        """右リールを描画する"""
        # 右リール座標
        currentcoord_rightreel = self._slot.reel[2].currentcoord

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の高さ
        reel_height = GameData.REEL_HEIGHT
        # リール画像(全体)の幅
        symbol_width = GameData.SYMBOL_WIDTH
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # リール描画用定数A (各リールの左右に確保する間隔)
        reeldraw_const_a = GameData.REELDRAW_CONST_A
        # リール描画用定数C (各リールの枠上/枠下の描画範囲)
        reeldraw_const_c = GameData.REELDRAW_CONST_C

        # リール描画
        # 右リール
        if 0 <= currentcoord_rightreel and currentcoord_rightreel <= (
            symbol_height * 2 + reeldraw_const_c
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_r,
                (
                    screen_width / 2 + symbol_width / 2 + reeldraw_const_a,
                    currentcoord_rightreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_r,
                (
                    screen_width / 2 + symbol_width / 2 + reeldraw_const_a,
                    currentcoord_rightreel + screen_height / 2 - symbol_height / 2,
                ),
            )
        elif (
            symbol_height * 2 + reeldraw_const_c < currentcoord_rightreel
            and currentcoord_rightreel
            <= (reel_height - symbol_height - reeldraw_const_c)
        ):
            # 上側画像
            self._screen.blit(
                self._reelimg_r,
                (
                    screen_width / 2 + symbol_width / 2 + reeldraw_const_a,
                    currentcoord_rightreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
        else:
            # 上側画像
            self._screen.blit(
                self._reelimg_r,
                (
                    screen_width / 2 + symbol_width / 2 + reeldraw_const_a,
                    currentcoord_rightreel
                    - reel_height * 2
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
            # 下側画像
            self._screen.blit(
                self._reelimg_r,
                (
                    screen_width / 2 + symbol_width / 2 + reeldraw_const_a,
                    currentcoord_rightreel
                    - reel_height
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )

    def _upper_reelcover_draw(self):
        """リール上側を黒塗りする"""
        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # リール描画用定数C (各リールの枠上/枠下の描画範囲)
        reeldraw_const_c = GameData.REELDRAW_CONST_C

        pygame.draw.rect(
            self._screen,
            GameData.RGB_BLACK,
            (
                0,
                0,
                screen_width,
                int(screen_height / 2 - symbol_height * 3 / 2 - reeldraw_const_c),
            ),
        )

    def _lower_reelcover_draw(self):
        """リール下側を黒塗りする"""
        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # リール描画用定数C (各リールの枠上/枠下の描画範囲)
        reeldraw_const_c = GameData.REELDRAW_CONST_C

        pygame.draw.rect(
            self._screen,
            GameData.RGB_BLACK,
            (
                0,
                int(screen_height / 2 + symbol_height * 3 / 2 + reeldraw_const_c),
                screen_width,
                screen_height,
            ),
        )

    def _gameui_draw(self):
        """UIを描画する"""
        self._ui_credit_draw()
        self._ui_payout_draw()
        self._ui_replay_draw()
        self._ui_bet_draw()
        self._ui_start_draw()
        self._ui_wait_draw()

    def _ui_credit_draw(self):
        """CREDIT表示を描画する"""
        credit = self._slot.credit

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH

        text = self._system_font.render("CREDIT: ", True, GameData.RGB_WHITE)
        text_rect = text.get_rect(topright=(screen_width - 80, 10))
        self._screen.blit(text, text_rect)
        text = self._system_font.render(str(credit), True, GameData.RGB_WHITE)
        text_rect = text.get_rect(topright=(screen_width - 10, 10))
        self._screen.blit(text, text_rect)

    def _ui_payout_draw(self):
        """PAYOUT表示を描画する"""
        payout = self._slot.payout

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH

        text = self._system_font.render("PAY: ", True, GameData.RGB_WHITE)
        text_rect = text.get_rect(topright=(screen_width - 80, 35))
        self._screen.blit(text, text_rect)
        text = self._system_font.render(str(payout), True, GameData.RGB_WHITE)
        text_rect = text.get_rect(topright=(screen_width - 10, 35))
        self._screen.blit(text, text_rect)

    def _ui_replay_draw(self):
        """REPLAYランプを描画する"""
        replay = self._slot.replay

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の幅
        symbol_width = GameData.SYMBOL_WIDTH

        # リール描画用定数A (各リールの左右に確保する間隔)
        reeldraw_const_a = GameData.REELDRAW_CONST_A

        # UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
        uidraw_const_a = GameData.UIDRAW_CONST_A
        # UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
        uidraw_const_b = GameData.UIDRAW_CONST_B

        if replay:
            replay_font_color = GameData.RGB_WHITE
        else:
            replay_font_color = GameData.RGB_GRAY
        text = self._system_font.render("REP", True, replay_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topright=(
                    screen_width / 2
                    - symbol_width * 3 / 2
                    - reeldraw_const_a
                    - uidraw_const_a,
                    screen_height / 2 + uidraw_const_b,
                )
            ),
        )

    def _ui_wait_draw(self):
        """WAITランプを描画する"""
        wait = self._slot.wait

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の幅
        symbol_width = GameData.SYMBOL_WIDTH

        # リール描画用定数A (各リールの左右に確保する間隔)
        reeldraw_const_a = GameData.REELDRAW_CONST_A

        # UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
        uidraw_const_a = GameData.UIDRAW_CONST_A
        # UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
        uidraw_const_b = GameData.UIDRAW_CONST_B

        if wait:
            wait_font_color = GameData.RGB_WHITE
        else:
            wait_font_color = GameData.RGB_GRAY
        text = self._system_font.render("WAIT", True, wait_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topright=(
                    screen_width / 2
                    - symbol_width * 3 / 2
                    - reeldraw_const_a
                    - uidraw_const_a,
                    screen_height / 2 + uidraw_const_b * 3,
                )
            ),
        )

    def _ui_start_draw(self):
        """STARTランプを描画する"""
        start = self._slot.start

        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT

        # UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
        uidraw_const_a = GameData.UIDRAW_CONST_A
        # UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
        uidraw_const_b = GameData.UIDRAW_CONST_B

        if start:
            start_font_color = GameData.RGB_WHITE
        else:
            start_font_color = GameData.RGB_GRAY
        text = self._system_font.render("START", True, start_font_color)
        self._screen.blit(
            text,
            text.get_rect(topleft=(uidraw_const_a, screen_height / 2 + uidraw_const_b)),
        )

    def _ui_bet_draw(self):
        """BETランプ(1BET/2BET/3BET)を描画する"""
        bet = self._slot.bet

        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT

        # UI描画用定数A (START/BET/REP/WAITランプの左右に確保する間隔)
        uidraw_const_a = GameData.UIDRAW_CONST_A
        # UI描画用定数B (START/BET/REP/WAITランプの上下に確保する間隔)
        uidraw_const_b = GameData.UIDRAW_CONST_B

        if bet == 1:
            bet3_font_color = GameData.RGB_GRAY
            bet2_font_color = GameData.RGB_GRAY
            bet1_font_color = GameData.RGB_WHITE
        elif bet == 2:
            bet3_font_color = GameData.RGB_GRAY
            bet2_font_color = GameData.RGB_WHITE
            bet1_font_color = GameData.RGB_WHITE
        elif bet == 3:
            bet3_font_color = GameData.RGB_WHITE
            bet2_font_color = GameData.RGB_WHITE
            bet1_font_color = GameData.RGB_WHITE
        else:
            bet3_font_color = GameData.RGB_GRAY
            bet2_font_color = GameData.RGB_GRAY
            bet1_font_color = GameData.RGB_GRAY
        text = self._system_font.render("3BET", True, bet3_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topleft=(
                    uidraw_const_a,
                    screen_height / 2 + uidraw_const_b * 3,
                )
            ),
        )
        text = self._system_font.render("2BET", True, bet2_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topleft=(
                    uidraw_const_a,
                    screen_height / 2 + uidraw_const_b * 5,
                )
            ),
        )
        text = self._system_font.render("1BET", True, bet1_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topleft=(
                    uidraw_const_a,
                    screen_height / 2 + uidraw_const_b * 7,
                )
            ),
        )

    def _gamedisplay_update(self):
        """displayオブジェクトを更新する"""
        pygame.display.update()

    def main_loop(self):
        """メインループ"""
        while True:
            # イベントを検知し更新する
            self._gameevent_update()

            # 前回からの経過時間を更新する
            self._timedelta_update()

            # ゲーム状態を更新する
            self._game_update()

            # Surfaceオブジェクトを更新する
            self._gameclock_update()

            # Surfaceオブジェクトを更新する
            self._gamescreen_update()

            # displayオブジェクトを更新する
            self._gamedisplay_update()


if __name__ == "__main__":
    game = Game(GameData.GAME_TITLE)
    game.main_loop()

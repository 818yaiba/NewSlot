import sys
import time

import GameData
import pygame
from cv2.typing import MatLike
from Slot import Slot


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
        self._id: int = Game._Id
        Game._Id += 1
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
        self._screen.fill(color=GameData.COLORS["BLACK"])
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
                    currentcoord_leftreel
                    + screen_height / 2
                    - symbol_height / 2,
                ),
            )
        elif (
            symbol_height * 2 + reeldraw_const_c < currentcoord_leftreel
            and currentcoord_leftreel
            <= reel_height - symbol_height - reeldraw_const_c
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
                    currentcoord_centerreel
                    + screen_height / 2
                    - symbol_height / 2,
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
                    currentcoord_rightreel
                    + screen_height / 2
                    - symbol_height / 2,
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
            GameData.COLORS["BLACK"],
            (
                0,
                0,
                screen_width,
                int(
                    screen_height / 2
                    - symbol_height * 3 / 2
                    - reeldraw_const_c
                ),
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
            GameData.COLORS["BLACK"],
            (
                0,
                int(
                    screen_height / 2
                    + symbol_height * 3 / 2
                    + reeldraw_const_c
                ),
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

        text = self._system_font.render(
            "CREDIT: ", True, GameData.COLORS["WHITE"]
        )
        text_rect = text.get_rect(topright=(screen_width - 80, 10))
        self._screen.blit(text, text_rect)
        text = self._system_font.render(
            str(credit), True, GameData.COLORS["WHITE"]
        )
        text_rect = text.get_rect(topright=(screen_width - 10, 10))
        self._screen.blit(text, text_rect)

    def _ui_payout_draw(self):
        """PAYOUT表示を描画する"""
        payout = self._slot.payout

        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH

        text = self._system_font.render(
            "PAY: ", True, GameData.COLORS["WHITE"]
        )
        text_rect = text.get_rect(topright=(screen_width - 80, 35))
        self._screen.blit(text, text_rect)
        text = self._system_font.render(
            str(payout), True, GameData.COLORS["WHITE"]
        )
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
            replay_font_color = GameData.COLORS["WHITE"]
        else:
            replay_font_color = GameData.COLORS["GRAY"]
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
            wait_font_color = GameData.COLORS["WHITE"]
        else:
            wait_font_color = GameData.COLORS["GRAY"]
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
            start_font_color = GameData.COLORS["WHITE"]
        else:
            start_font_color = GameData.COLORS["GRAY"]
        text = self._system_font.render("START", True, start_font_color)
        self._screen.blit(
            text,
            text.get_rect(
                topleft=(uidraw_const_a, screen_height / 2 + uidraw_const_b)
            ),
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
            bet3_font_color = GameData.COLORS["GRAY"]
            bet2_font_color = GameData.COLORS["GRAY"]
            bet1_font_color = GameData.COLORS["WHITE"]
        elif bet == 2:
            bet3_font_color = GameData.COLORS["GRAY"]
            bet2_font_color = GameData.COLORS["WHITE"]
            bet1_font_color = GameData.COLORS["WHITE"]
        elif bet == 3:
            bet3_font_color = GameData.COLORS["WHITE"]
            bet2_font_color = GameData.COLORS["WHITE"]
            bet1_font_color = GameData.COLORS["WHITE"]
        else:
            bet3_font_color = GameData.COLORS["GRAY"]
            bet2_font_color = GameData.COLORS["GRAY"]
            bet1_font_color = GameData.COLORS["GRAY"]
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

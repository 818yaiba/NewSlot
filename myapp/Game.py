import sys

import GameData
import pygame
import utils
from Slot import Slot


class Game:
    """ゲーム

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

        self._screen_width: int = GameData.SCREEN_WIDTH
        self._screen_height: int = GameData.SCREEN_HEIGHT

        pygame.init()
        self._screen = pygame.display.set_mode(
            (self._screen_width, self._screen_height)
        )
        pygame.display.set_caption(self._name)
        self._clock = pygame.time.Clock()

        self._systemfont_name = GameData.FONT_WANPAKURUIKA
        self._system_font = pygame.font.SysFont(self._systemfont_name, 16)

        self._framerate_limit: int | None = GameData.FRAMERATE_LIMIT

        # slot
        self._slot = Slot()

        # リール描画用リール画像 (OpenCV → pygame)
        self._left_reel_image = utils.cv2_to_pygame_surface(
            self._slot.reel[0].reel_image
        )
        self._center_reel_image = utils.cv2_to_pygame_surface(
            self._slot.reel[1].reel_image
        )
        self._right_reel_image = utils.cv2_to_pygame_surface(
            self._slot.reel[2].reel_image
        )

    def game_quit(self) -> None:
        """ゲームを終了する"""
        pygame.quit()
        sys.exit()

    def _gameevent_update(self) -> None:
        """イベントを検知し更新する"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_quit()
            elif event.type == pygame.KEYDOWN:
                self._keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._keyup_event(event)

    def _keydown_event(self, event: pygame.event.Event) -> None:
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

    def _keyup_event(self, event: pygame.event.Event) -> None:
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

    def _clock_update(self) -> float:
        """clockを更新する

        Returns
        -------
        ticktime_sec: float
            前回tick命令実行からの経過時間[sec]
        """
        if GameData.FRAMERATE_LIMIT is None:
            ticktime_msec = self._clock.tick_busy_loop()
        else:
            ticktime_msec = self._clock.tick_busy_loop(
                GameData.FRAMERATE_LIMIT
            )

        ticktime_sec = ticktime_msec / 1000.0

        return ticktime_sec

    def _get_ticktime(self) -> float:
        """前回tick命令実行からの経過時間を返す

        Returns
        -------
        timedelta_sec: float
            前回tick命令実行からの経過時間[sec]
        """
        timedelta_msec = self._clock.get_time()

        timedelta_sec = timedelta_msec / 1000.0

        return timedelta_sec

    def _game_update(self) -> None:
        """ゲーム状態を更新する"""
        timedelta_sec = self._get_ticktime()
        self._slot.update(timedelta_sec)

    def _screen_update(self):
        """Surfaceオブジェクトを更新する"""
        self._screen.fill(color=GameData.COLORS["BLACK"])
        self._screen_reel_draw()
        self._screen_ui_draw()

    def _draw_reel(
        self,
        reel_image_surface: pygame.Surface,
        current_coord: float,
        reel_draw_offset_x: int,
    ) -> None:
        """リール描画

        Parameters
        ----------
        reel_image_surface : pygame.Surface
            リール画像
        current_coord : float
            現在座標
        reel_draw_offset_x : int
            X方向のオフセット
        """
        reel_height = GameData.REEL_HEIGHT

        common_offset_X = GameData.REEL_DRAW_COMMON_OFFSET_X
        common_offset_Y = GameData.REEL_DRAW_COMMON_OFFSET_Y
        reel_frame_top = GameData.REEL_FRAME_TOP
        reel_frame_bottom = GameData.REEL_FRAME_BOTTOM

        if 0 <= current_coord <= reel_frame_bottom:
            self._screen.blit(
                reel_image_surface,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + current_coord - reel_height * 1,
                ),
            )
            self._screen.blit(
                reel_image_surface,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + current_coord - reel_height * 0,
                ),
            )
        elif reel_frame_bottom < current_coord <= reel_frame_top:
            self._screen.blit(
                reel_image_surface,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + current_coord - reel_height * 1,
                ),
            )
        else:
            self._screen.blit(
                reel_image_surface,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + current_coord - reel_height * 2,
                ),
            )
            self._screen.blit(
                reel_image_surface,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + current_coord - reel_height * 1,
                ),
            )

    def _left_reel_draw(self) -> None:
        """左リールを描画する"""
        self._draw_reel(
            self._left_reel_image,
            self._slot.reel[0].current_coord,
            GameData.REEL_DRAW_LEFT_OFFSET_X,
        )

    def _center_reel_draw(self) -> None:
        """中リールを描画する"""
        self._draw_reel(
            self._center_reel_image,
            self._slot.reel[1].current_coord,
            GameData.REEL_DRAW_CENTER_OFFSET_X,
        )

    def _right_reel_draw(self) -> None:
        """右リールを描画する"""
        self._draw_reel(
            self._right_reel_image,
            self._slot.reel[2].current_coord,
            GameData.REEL_DRAW_RIGHT_OFFSET_X,
        )

    def _upper_reelcover_draw(self) -> None:
        """リール上側を黒塗りする"""
        pygame.draw.rect(
            self._screen,
            GameData.COLORS["BLACK"],
            (
                0,
                0,
                GameData.SCREEN_WIDTH,
                int(
                    GameData.SCREEN_HEIGHT / 2
                    - GameData.SYMBOL_HEIGHT * 3 / 2
                    - GameData.REEL_OUTSIDE_DRAW_RANGE
                ),
            ),
        )

    def _lower_reelcover_draw(self):
        """リール下側を黒塗りする"""
        pygame.draw.rect(
            self._screen,
            GameData.COLORS["BLACK"],
            (
                0,
                int(
                    GameData.SCREEN_HEIGHT / 2
                    + GameData.SYMBOL_HEIGHT * 3 / 2
                    + GameData.REEL_OUTSIDE_DRAW_RANGE
                ),
                GameData.SCREEN_WIDTH,
                GameData.SCREEN_HEIGHT,
            ),
        )

    def _screen_reel_draw(self) -> None:
        """リールを描画する"""
        # 左リールを描画
        self._left_reel_draw()
        # 中リールを描画
        self._center_reel_draw()
        # 右リールを描画
        self._right_reel_draw()
        # リール上側を黒塗りする
        self._upper_reelcover_draw()
        # リール下側を黒塗りする
        self._lower_reelcover_draw()

    def _screen_ui_draw(self):
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
        reeldraw_const_a = GameData.REEL_SPACE_BETWEEN_REELS

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
        reeldraw_const_a = GameData.REEL_SPACE_BETWEEN_REELS

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

    def _display_update(self):
        """displayオブジェクトを更新する"""
        pygame.display.update()

    def main_loop(self):
        """メインループ"""
        while True:
            # イベントを検知し更新する
            self._gameevent_update()

            # ゲーム状態を更新する
            self._game_update()

            # Surfaceオブジェクトを更新する
            self._screen_update()

            # displayオブジェクトを更新する
            self._display_update()

            # clockオブジェクトを更新する
            self._clock_update()

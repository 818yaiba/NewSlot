import sys

import GameData
import pygame
import Utility
from Slot import Slot
from Symbol import Symbol


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

        pygame.init()
        self._screen = pygame.display.set_mode(
            (GameData.SCREEN_WIDTH, GameData.SCREEN_HEIGHT)
        )
        pygame.display.set_caption(self._name)
        self._clock = pygame.time.Clock()

        self._system_font = pygame.font.Font(
            GameData.FONT_MPLUS1_FILE_PATH, 16
        )

        self._framerate_limit: int | None = GameData.FRAMERATE_LIMIT

        # slot
        self._slot = Slot()

        # リール描画用リール画像 (OpenCV → pygame)
        self._left_reel_image = Utility.cv2_to_pygame_surface(
            self._slot.reel[0].reel_image
        )
        self._center_reel_image = Utility.cv2_to_pygame_surface(
            self._slot.reel[1].reel_image
        )
        self._right_reel_image = Utility.cv2_to_pygame_surface(
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

    def _screen_update(self) -> None:
        """Surfaceオブジェクトを更新する"""
        self._screen_fill_black(screen=self._screen)
        self._screen_draw_reel(
            screen=self._screen,
            left_reel_image=self._left_reel_image,
            center_reel_image=self._center_reel_image,
            right_reel_image=self._right_reel_image,
        )
        self._screen_draw_ui(screen=self._screen)

    def _screen_fill_black(self, screen: pygame.Surface) -> None:
        """画面を黒で塗りつぶす

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        """
        screen.fill(color=GameData.Color.black)

    def _draw_reel(
        self,
        screen: pygame.Surface,
        reel_image: pygame.Surface,
        cur_coord: float,
        reel_draw_offset_x: int,
    ) -> None:
        """リール描画

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        reel_image : pygame.Surface
            リール画像
        cur_coord : float
            現在座標
        reel_draw_offset_x : int
            X方向のオフセット
        """
        reel_height = GameData.REEL_HEIGHT
        common_offset_X = GameData.REEL_DRAW_COMMON_OFFSET_X
        common_offset_Y = GameData.REEL_DRAW_COMMON_OFFSET_Y

        if 0 <= cur_coord <= GameData.REEL_FRAME_BOTTOM:
            screen.blit(
                reel_image,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + cur_coord - reel_height * 1,
                ),
            )
            screen.blit(
                reel_image,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + cur_coord - reel_height * 0,
                ),
            )
        elif GameData.REEL_FRAME_BOTTOM < cur_coord <= GameData.REEL_FRAME_TOP:
            # この場合は1枚のリール画像のみでよい
            screen.blit(
                reel_image,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + cur_coord - reel_height * 1,
                ),
            )
        else:
            screen.blit(
                reel_image,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + cur_coord - reel_height * 2,
                ),
            )
            screen.blit(
                reel_image,
                (
                    common_offset_X + reel_draw_offset_x,
                    common_offset_Y + cur_coord - reel_height * 1,
                ),
            )

    def _screen_draw_left_reel(
        self, screen: pygame.Surface, left_reel_image: pygame.Surface
    ) -> None:
        """左リールを描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        left_reel_image : pygame.Surface
            左リール画像
        """
        self._draw_reel(
            screen=screen,
            reel_image=left_reel_image,
            cur_coord=self._slot.reel[0].current_coord,
            reel_draw_offset_x=GameData.REEL_DRAW_LEFT_OFFSET_X,
        )

    def _screen_draw_center_reel(
        self, screen: pygame.Surface, center_reel_image: pygame.Surface
    ) -> None:
        """中リールを描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        center_reel_image : pygame.Surface
            中リール画像
        """
        self._draw_reel(
            screen=screen,
            reel_image=center_reel_image,
            cur_coord=self._slot.reel[1].current_coord,
            reel_draw_offset_x=GameData.REEL_DRAW_CENTER_OFFSET_X,
        )

    def _screen_draw_right_reel(
        self, screen: pygame.Surface, right_reel_image: pygame.Surface
    ) -> None:
        """右リールを描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        right_reel_image : pygame.Surface
            右リール画像
        """
        self._draw_reel(
            screen=screen,
            reel_image=right_reel_image,
            cur_coord=self._slot.reel[2].current_coord,
            reel_draw_offset_x=GameData.REEL_DRAW_RIGHT_OFFSET_X,
        )

    def _screen_draw_upper_reelcover(self, screen: pygame.Surface) -> None:
        """リール上側を黒で塗りつぶす

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        """
        pygame.draw.rect(
            screen,
            GameData.Color.black,
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

    def _screen_draw_lower_reelcover(self, screen: pygame.Surface) -> None:
        """リール下側を黒で塗りつぶす

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        """
        pygame.draw.rect(
            screen,
            GameData.Color.black,
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

    def _screen_draw_reel(
        self,
        screen: pygame.Surface,
        left_reel_image: pygame.Surface,
        center_reel_image: pygame.Surface,
        right_reel_image: pygame.Surface,
    ) -> None:
        """リールを描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        left_reel_image : pygame.Surface
            左リール画像
        center_reel_image : pygame.Surface
            中リール画像
        right_reel_image : pygame.Surface
            右リール画像
        """
        self._screen_draw_left_reel(
            screen=screen, left_reel_image=left_reel_image
        )
        self._screen_draw_center_reel(
            screen=screen, center_reel_image=center_reel_image
        )
        self._screen_draw_right_reel(
            screen=screen, right_reel_image=right_reel_image
        )
        self._screen_draw_upper_reelcover(screen=screen)
        self._screen_draw_lower_reelcover(screen=screen)

    def _screen_draw_ui(self, screen: pygame.Surface):
        """UIを描画する"""
        self._screen_draw_ui_credit(screen=screen, credit=self._slot.credit)
        self._screen_draw_ui_payout(screen=screen, payout=self._slot.payout)

        self._screen_draw_ui_reelinfo(
            screen=screen,
            font=self._system_font,
            left_reel_cur_symbol=self._slot.reel[0].current_symbol,
            center_reel_cur_symbol=self._slot.reel[1].current_symbol,
            right_reel_cur_symbol=self._slot.reel[2].current_symbol,
        )

    # self._screen_draw_ui_replay(screen=screen)
    # self._screen_draw_ui_bet(screen=screen)
    # self._screen_draw_ui_start(screen=screen)
    # self._screen_draw_ui_wait(screen=screen)

    def _screen_draw_ui_credit(self, screen: pygame.Surface, credit: int):
        """CREDIT表示を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        credit : int
            現在のCREDIT値
        """
        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH

        text = self._system_font.render("CREDIT: ", True, GameData.Color.white)
        text_rect = text.get_rect(topright=(screen_width - 80, 10))
        screen.blit(text, text_rect)
        text = self._system_font.render(
            str(credit), True, GameData.Color.white
        )
        text_rect = text.get_rect(topright=(screen_width - 10, 10))
        screen.blit(text, text_rect)

    def _screen_draw_ui_payout(self, screen: pygame.Surface, payout: int):
        """PAYOUT表示を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        payout : int
            現在のPAYOUT値
        """
        # ゲーム画面幅
        screen_width = GameData.SCREEN_WIDTH

        text = self._system_font.render("PAY: ", True, GameData.Color.white)
        text_rect = text.get_rect(topright=(screen_width - 80, 35))
        screen.blit(text, text_rect)
        text = self._system_font.render(
            str(payout), True, GameData.Color.white
        )
        text_rect = text.get_rect(topright=(screen_width - 10, 35))
        screen.blit(text, text_rect)

    def _screen_draw_ui_reelinfo(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        left_reel_cur_symbol: list[Symbol],
        center_reel_cur_symbol: list[Symbol],
        right_reel_cur_symbol: list[Symbol],
    ) -> None:
        """リール情報を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        font : pygame.font.Font
            描画に使用するフォントオブジェクト
        left_reel_cur_symbol : list[Symbol]
            現在の左リールの図柄
        center_reel_cur_symbol : list[Symbol]
            現在の中リールの図柄
        right_reel_cur_symbol : list[Symbol]
            現在の右リールの図柄
        """
        # 最終的な描画イメージ
        # -----
        # 1 0 1
        # 0 1 0
        # 2 4 3
        # -----

        # 左リール情報を描画
        self._screen_draw_ui_reft_reelinfo(
            screen=screen, font=font, left_reel_cur_symbol=left_reel_cur_symbol
        )
        # 中リール情報を描画
        self._screen_draw_ui_center_reelinfo(
            screen=screen,
            font=font,
            center_reel_cur_symbol=center_reel_cur_symbol,
        )
        # 右リール情報を描画
        self._screen_draw_ui_right_reelinfo(
            screen=screen,
            font=font,
            right_reel_cur_symbol=right_reel_cur_symbol,
        )

    def _screen_draw_ui_reft_reelinfo(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        left_reel_cur_symbol: list[Symbol],
    ) -> None:
        """左リール情報を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        font : pygame.font.Font
            描画に使用するフォントオブジェクト
        left_reel_cur_symbol : list[Symbol]
            現在の左リールの図柄
        """
        self._draw_reelinfo(
            screen=screen,
            font=font,
            current_symbol=left_reel_cur_symbol,
            reelinfo_draw_offset_x=30,
        )

    def _screen_draw_ui_center_reelinfo(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        center_reel_cur_symbol: list[Symbol],
    ) -> None:
        """中リール情報を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        font : pygame.font.Font
            描画に使用するフォントオブジェクト
        center_reel_cur_symbol : list[Symbol]
            現在の中リールの図柄
        """
        self._draw_reelinfo(
            screen=screen,
            font=font,
            current_symbol=center_reel_cur_symbol,
            reelinfo_draw_offset_x=75,
        )

    def _screen_draw_ui_right_reelinfo(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        right_reel_cur_symbol: list[Symbol],
    ) -> None:
        """右リール情報を描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        font : pygame.font.Font
            描画に使用するフォントオブジェクト
        right_reel_cur_symbol : list[Symbol]
            現在の右リールの図柄
        """
        self._draw_reelinfo(
            screen=screen,
            font=font,
            current_symbol=right_reel_cur_symbol,
            reelinfo_draw_offset_x=120,
        )

    def _draw_reelinfo(
        self,
        screen: pygame.Surface,
        font: pygame.font.Font,
        current_symbol: list[Symbol],
        reelinfo_draw_offset_x: int,
    ) -> None:
        """リール情報を描画する
        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        current_symbol : list[Symbol]
            現在のリールの図柄
        reelinfo_draw_offset_x : int
            リール情報の描画オフセットX座標
        font : pygame.font.Font
            描画に使用するフォントオブジェクト
        """
        # ゲーム画面高さ
        screen_height = GameData.SCREEN_HEIGHT
        # リール画像(全体)の幅
        symbol_height = GameData.SYMBOL_HEIGHT

        top_symbolid_text = font.render(
            str(current_symbol[0].id), True, GameData.Color.white
        )
        middle_symbolid_text = font.render(
            str(current_symbol[1].id), True, GameData.Color.white
        )
        bottom_symbolid_text = font.render(
            str(current_symbol[2].id), True, GameData.Color.white
        )
        screen.blit(
            top_symbolid_text,
            top_symbolid_text.get_rect(
                center=(
                    reelinfo_draw_offset_x,
                    screen_height / 2
                    - symbol_height * 2
                    + symbol_height / 2
                    + 24 * 0,  # フォントの高さを考慮して調整,
                )
            ),
        )
        screen.blit(
            middle_symbolid_text,
            middle_symbolid_text.get_rect(
                center=(
                    reelinfo_draw_offset_x,
                    screen_height / 2
                    - symbol_height * 2
                    + symbol_height / 2
                    + 24 * 1,  # フォントの高さを考慮して調整,
                )
            ),
        )
        screen.blit(
            bottom_symbolid_text,
            bottom_symbolid_text.get_rect(
                center=(
                    reelinfo_draw_offset_x,
                    screen_height / 2
                    - symbol_height * 2
                    + symbol_height / 2
                    + 24 * 2,  # フォントの高さを考慮して調整,
                )
            ),
        )

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
            replay_font_color = GameData.Color.white
        else:
            replay_font_color = GameData.Color.gray
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

    def _screen_draw_ui_wait(self, screen: pygame.Surface):
        """WAITランプを描画する

        Parameters
        ----------
        screen : pygame.Surface
            描画対象のSurfaceオブジェクト
        """
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
            wait_font_color = GameData.Color.white
        else:
            wait_font_color = GameData.Color.gray
        text = self._system_font.render("WAIT", True, wait_font_color)
        screen.blit(
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
            start_font_color = GameData.Color.white
        else:
            start_font_color = GameData.Color.gray
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
            bet3_font_color = GameData.Color.gray
            bet2_font_color = GameData.Color.gray
            bet1_font_color = GameData.Color.white
        elif bet == 2:
            bet3_font_color = GameData.Color.gray
            bet2_font_color = GameData.Color.white
            bet1_font_color = GameData.Color.white
        elif bet == 3:
            bet3_font_color = GameData.Color.white
            bet2_font_color = GameData.Color.white
            bet1_font_color = GameData.Color.white
        else:
            bet3_font_color = GameData.Color.gray
            bet2_font_color = GameData.Color.gray
            bet1_font_color = GameData.Color.gray
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

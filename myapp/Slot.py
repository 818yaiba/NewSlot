import time

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
            self._reel[0].reel_start()
            self._reel[1].reel_start()
            self._reel[2].reel_start()
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

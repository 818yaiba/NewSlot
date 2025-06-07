import cv2
import GameData
from cv2.typing import MatLike
from Symbol import Symbol


class Reel:
    """リール

    Attributes
    ----------
    id : int
        リールID
    reel_symbol : list[Symbol]
        リール配列
    reel_image : MatLike
        リール画像
    current_coord : float
        リール現在座標
    current_symbol : list[Symbol]
        現在表示中の図柄
    target_symbol : list[Symbol]
        目標図柄
    spinning : bool
        リール回転状態
    stop_request : bool
        リール停止指示状態
    """

    _Id: int = 0

    def __init__(self, reel_symbol: list[Symbol]) -> None:
        """
        Parameters
        ----------
        reel_symbol: list[Symbol]
            リール配列
        """
        self._id: int = Reel._Id
        Reel._Id += 1

        if len(reel_symbol) != GameData.REEL_SYMBOL_LENGTH:
            raise ValueError(
                "指定されたリール配列の図柄数が既定のリール図柄数と一致しません"
            )
        self._reel_symbol: list[Symbol] = reel_symbol

        self._reel_image: MatLike = self._get_reel_image(self._reel_symbol)
        if self._reel_image.shape[1] != GameData.REEL_WIDTH:
            raise ValueError("リール画像の幅が既定値と一致しません")
        if self._reel_image.shape[0] != GameData.REEL_HEIGHT:
            raise ValueError("リール画像の高さが既定値と一致しません")

        self._current_coord: float = 600.0
        self._current_symbol: list[Symbol] = self._get_current_symbol()

        self._target_symbol: list[Symbol] | list[None] = [None, None, None]

        self._spinning: bool = False
        self._stop_request: bool = True

    def _get_reel_image(self, symbols: list["Symbol"]) -> MatLike:
        """リール画像を生成して返す

        Parameters
        ----------
        symbol_array: list[Symbol]
            リール配列

        Returns
        -------
        reel_image: MatLike
            リール画像
        """
        # 画像サイズチェック
        base_shape = symbols[0].image.shape
        for symbol in symbols:
            if symbol.image.shape != base_shape:
                raise ValueError("リール画像のサイズが一致しません")
            if symbol.image.shape[1] != GameData.REEL_WIDTH:
                raise ValueError("リール画像の幅が不正です")
            if symbol.image.shape[0] != GameData.SYMBOL_HEIGHT:
                raise ValueError("リール画像の高さが不正です")
        # 画像を縦に連結
        reel_image_tmp = symbols[0].image
        for symbol in symbols[1:]:
            reel_image_tmp = cv2.vconcat([reel_image_tmp, symbol.image])
        return reel_image_tmp

    def _get_current_symbol(self) -> list[Symbol]:
        """現在リール上にある図柄を取得し、現在表示中の図柄として返す

        Returns
        -------
        current_symbol : list[Symbol]
            現在表示中の図柄
        """
        # 図柄1つ分の高さ
        symbol_height = GameData.SYMBOL_HEIGHT

        # 上段/中段/下段に表示されている図柄のインデックスを算出
        current_symbol_index_top = int(self._current_coord / symbol_height) - 1
        current_symbol_index_middle = current_symbol_index_top + 1
        current_symbol_index_bottom = current_symbol_index_middle + 1

        # リール図柄数
        reel_symbol_length = GameData.REEL_SYMBOL_LENGTH
        # 1周分の補正
        current_symbol_index_top %= reel_symbol_length
        current_symbol_index_middle %= reel_symbol_length
        current_symbol_index_bottom %= reel_symbol_length

        # 図柄のインデックスからオブジェクト取得
        current_symbol: list[Symbol] = [
            self._reel_symbol[current_symbol_index_top],
            self._reel_symbol[current_symbol_index_middle],
            self._reel_symbol[current_symbol_index_bottom],
        ]

        return current_symbol

    def get_n_ahead_symbol(self, n: int) -> list[Symbol]:
        """現在位置からn個先の図柄を取得

        Parameters
        ----------
        n : int
            取得先までの図柄数
        """
        if n < 0:
            raise ValueError("nに負の値は指定できません")

        target_symbol_index_top = (
            self._reel_symbol.index(
                self._current_symbol[GameData.REEL_POSITION_TOP]
            )
            - n
        )
        target_symbol_index_middle = target_symbol_index_top + 1
        target_symbol_index_bottom = target_symbol_index_middle + 1

        # リール図柄数
        reel_symbol_length = GameData.REEL_SYMBOL_LENGTH

        # 1周分の補正
        target_symbol_index_top %= reel_symbol_length
        target_symbol_index_middle %= reel_symbol_length
        target_symbol_index_bottom %= reel_symbol_length

        # 図柄のインデックスからオブジェクト取得
        target_symbol: list[Symbol] = [
            self._reel_symbol[target_symbol_index_top],
            self._reel_symbol[target_symbol_index_middle],
            self._reel_symbol[target_symbol_index_bottom],
        ]

        return target_symbol

    def _get_target_symbol(
        self, target_symbol_index: int, target_stop_position: int
    ) -> list[Symbol]:
        """リール目標表示図柄を設定

        Parameters
        ----------
        target_symbol_index : int
            目標図柄のインデックス
        target_stop_position : int
            目標停止位置
        """
        if target_symbol_index < 0:
            raise ValueError("目標図柄のインデックスに負の値は指定できません")
        if GameData.REEL_SYMBOL_LENGTH < target_symbol_index:
            raise ValueError(
                "目標図柄のインデックスがリール配列の図柄数を超えています"
            )
        if target_stop_position == GameData.REEL_POSITION_TOP:
            target_symbol_index_top = target_symbol_index
            target_symbol_index_middle = target_symbol_index_top - 1
            target_symbol_index_bottom = target_symbol_index_middle - 1
        elif target_stop_position == GameData.REEL_POSITION_MIDDLE:
            target_symbol_index_middle = target_symbol_index
            target_symbol_index_top = target_symbol_index_middle + 1
            target_symbol_index_bottom = target_symbol_index_middle - 1
        elif target_stop_position == GameData.REEL_POSITION_BOTTOM:
            target_symbol_index_bottom = target_symbol_index
            target_symbol_index_top = target_symbol_index_bottom + 2
            target_symbol_index_middle = target_symbol_index_top - 1
        else:
            raise ValueError("目標停止位置の値が不正です")

        # リール図柄数
        reel_symbol_length = GameData.REEL_SYMBOL_LENGTH

        # 1周分の補正
        target_symbol_index_top %= reel_symbol_length
        target_symbol_index_middle %= reel_symbol_length
        target_symbol_index_bottom %= reel_symbol_length

        # 図柄のインデックスからオブジェクト取得
        target_symbol: list[Symbol] = [
            self._reel_symbol[target_symbol_index_top],
            self._reel_symbol[target_symbol_index_middle],
            self._reel_symbol[target_symbol_index_bottom],
        ]

        return target_symbol

    def reel_start(self) -> None:
        """リールの回転を開始する"""
        self._targetsymbol = [None, None, None]
        self._spinning = True
        self._stop_request = False

    def stop_spin(
        self, target_symbol_index: int, target_stop_position: int
    ) -> None:
        """リール停止指示を行う

        Parameters
        ----------
        target_symbol_index : int
            目標図柄のインデックス
        target_stop_position : int
            目標停止位置
        """
        # リール目標表示図柄を設定
        self._target_symbol = self._get_target_symbol(
            target_symbol_index, target_stop_position
        )

        # リール停止指示
        self._stop_request = True

    def update(self, dt: float):
        """リール状態を更新する

        Parameters
        ----------
        dt: float
            前回からの経過時間
        """

        # 回転中の場合
        if self._spinning:
            # リール座標を更新する
            self._current_coord = self._get_updated_current_coord(
                self._current_coord, dt
            )

            # 現在表示中の図柄を取得
            self._current_symbol = self._get_current_symbol()

            # 停止指示がある場合
            if self._stop_request:
                # 現在表示中の図柄 = 停止目標図柄であれば回転停止
                if self._current_symbol == self._targetsymbol:
                    self._spinning = False

    def _get_updated_current_coord(
        self, current_coord: float, dt: float
    ) -> float:
        """リールの現在座標を更新する

        Parameters
        ----------
        dt: float
            前回からの経過時間
        current_coord: float
            現在座標

        Returns
        -------
        current_coord: float
            更新後のリール現在座標
        """
        # リール画像高さ
        reel_height = GameData.REEL_HEIGHT

        # 前回からの経過時間から現在座標を計算
        current_coord += (reel_height / GameData.REEL_SPEED) * dt

        # 現在座標がリール端を超えている場合、補正する
        if current_coord >= reel_height:
            current_coord %= reel_height

        return current_coord

    @property
    def id(self) -> int:
        return self._id

    @property
    def reel_symbol(self) -> list[Symbol]:
        return self._reel_symbol

    @property
    def reel_image(self) -> MatLike:
        return self._reel_image

    @property
    def current_coord(self) -> float:
        return self._current_coord

    @property
    def current_symbol(self) -> list[Symbol]:
        return self._current_symbol

    @property
    def target_symbol(self) -> list[Symbol] | list[None]:
        return self._target_symbol

    @property
    def spinning(self) -> bool:
        return self._spinning

    @property
    def stop_request(self) -> bool:
        return self._stop_request

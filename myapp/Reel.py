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
    name : str
        リール名
    symbolarray : list[Symbol]
        リール配列
    reelimage : MatLike
        リール画像
    currentcoord : float
        リール現在座標
    currentsymbol : list[Symbol]
        現在表示中の図柄
    targetsymbol : list[Symbol]
        目標表示図柄
    rotate : bool
        リール回転状態
    stop : bool
        リール停止指示状態
    """

    _Id: int = 0

    def __init__(self, name: str, symbolarray: list[Symbol]):
        """
        Parameters
        ----------
        name : str
            リール名
        symbolarray: list[Symbol]
            リール配列
        """
        self._id: int = Reel._Id
        Reel._Id += 1
        self._name: str = name

        self._symbolarray: list[Symbol] = symbolarray
        if not len(self._symbolarray) == GameData.SYMBOLARRAY_LENGTH:
            raise Exception("リール図柄数が既定値と一致しません")

        self._reelimage: MatLike = self._get_reelimage()

        image_width = self._reelimage.shape[1]
        image_height = self._reelimage.shape[0]
        if not image_width == GameData.REEL_WIDTH:
            raise Exception("リール画像の幅が既定値と一致しません")
        if not image_height == GameData.REEL_HEIGHT:
            raise Exception("リール画像の高さが既定値と一致しません")

        self._currentcoord: float = 0.0
        self._currentsymbol: list[Symbol] = self._get_currentsymbol()
        self._targetsymbol: list[Symbol] | list[None] = [None, None, None]
        self._rotate: bool = False
        self._stop: bool = True

    def _get_reelimage(self) -> MatLike:
        """リール画像を生成して返す

        Parameters
        ----------
        symbolarray: list[Symbol]
            リール配列

        Returns
        -------
        reelimage: MatLike
            リール画像
        """
        if not self._symbolarray:
            raise ValueError("リール配列が空です。画像を生成できません。")

        reelimage_tmp = self._symbolarray[0].image
        for symbol in self._symbolarray[1:]:
            # 図柄画像を縦方向に結合していく
            reelimage_tmp = cv2.vconcat([reelimage_tmp, symbol.image])

        return reelimage_tmp

    def _get_currentsymbol(self) -> list[Symbol]:
        """現在表示中の図柄を取得して返す

        Returns
        -------
        currentsymbol : list[Symbol]
            現在表示中の図柄
        """
        # 図柄1つ分の高さ
        symbol_heighteight = GameData.SYMBOL_HEIGHT
        # リール図柄数
        symbolarray_length = GameData.SYMBOLARRAY_LENGTH

        # 上段/中段/下段に表示されている図柄のインデックスを算出
        currentsymbolindex_upper = int(
            self._currentcoord // symbol_heighteight
        )
        currentsymbolindex_middle = currentsymbolindex_upper - 1
        currentsymbolindex_lower = currentsymbolindex_middle - 1
        # リールの1周分を考慮して補正を行う
        if currentsymbolindex_middle < 0:
            currentsymbolindex_middle += symbolarray_length
        if currentsymbolindex_lower < 0:
            currentsymbolindex_lower += symbolarray_length

        # 図柄のインデックスから図柄オブジェクトを取得
        currentsymbol_upper = self._symbolarray[currentsymbolindex_upper]
        currentsymbol_middle = self._symbolarray[currentsymbolindex_middle]
        currentsymbol_lower = self._symbolarray[currentsymbolindex_lower]

        # 結果返却用リスト
        currentsymbol = [
            currentsymbol_upper,
            currentsymbol_middle,
            currentsymbol_lower,
        ]

        return currentsymbol

    def _set_targetsymbol(self, targetsymbolindex: int, targetposition: int):
        """リール目標表示図柄を設定

        Parameters
        ----------
        targetsymbolindex : int
            目標停止図柄のインデックス
        targetposition : int
            目標停止位置 (0:上段, 1:中段, 2:下段)
        """
        if targetposition == 0:
            # 上段
            targetsymbolindex_upper = targetsymbolindex
            targetsymbolindex_middle = targetsymbolindex_upper - 1
            targetsymbolindex_lower = targetsymbolindex_middle - 1
        elif targetposition == 1:
            # 中段
            targetsymbolindex_middle = targetsymbolindex
            targetsymbolindex_upper = targetsymbolindex_middle + 1
            targetsymbolindex_lower = targetsymbolindex_middle - 1
        elif targetposition == 2:
            # 下段
            targetsymbolindex_lower = targetsymbolindex
            targetsymbolindex_upper = targetsymbolindex_lower + 2
            targetsymbolindex_middle = targetsymbolindex_upper - 1
        else:
            raise ValueError(
                f"targetposition の値が不正です: {targetposition}"
            )

        # リール図柄数
        symbolarray_length = GameData.SYMBOLARRAY_LENGTH

        # 1周分の補正
        targetsymbolindex_upper %= symbolarray_length
        targetsymbolindex_middle %= symbolarray_length
        targetsymbolindex_lower %= symbolarray_length

        # 図柄のインデックスからオブジェクト取得
        targetsymbol = [
            self._symbolarray[targetsymbolindex_upper],
            self._symbolarray[targetsymbolindex_middle],
            self._symbolarray[targetsymbolindex_lower],
        ]

        self._targetsymbol = targetsymbol

    def reelstart(self):
        """リールの回転を開始する"""
        # リール回転状態
        self._rotate = True

        # リール停止指示状態
        self._stop = False

    def reelstop(self, targetsymbolindex: int, targetposition: int):
        """リール停止指示を行う

        Parameters
        ----------
        targetsymbolindex : int
            目標停止図柄のインデックス
        targetposition : int
            目標停止位置 (0:上段, 1:中段, 2:下段)
        """
        if not 0 <= targetsymbolindex:
            raise Exception(
                "目標停止図柄のインデックスが不正です (負の値は指定できません)"
            )
        elif not targetsymbolindex <= GameData.SYMBOLARRAY_LENGTH:
            raise Exception(
                "目標停止図柄のインデックスが不正です (リール配列の範囲外です)"
            )
        else:
            if targetposition not in [0, 1, 2]:
                raise Exception(
                    "目標停止位置が不正です (0:上段, 1:中段, 2:下段)"
                )

        # リール目標表示図柄を設定
        self._set_targetsymbol(targetsymbolindex, targetposition)

        # リール停止指示
        self._stop = True

    def update(self, dt: float):
        """リール状態を更新する

        Parameters
        ----------
        dt: float
            前回からの経過時間
        """
        # 回転中の場合
        if self._rotate:
            # リール画像高さ
            reel_heighteight = GameData.REEL_HEIGHT

            # 前回からの経過時間から現在座標を計算
            self._currentcoord += (reel_heighteight / GameData.REEL_SPEED) * dt

            # 現在座標がリール端を超えている場合、補正する
            if self._currentcoord >= reel_heighteight:
                self._currentcoord %= reel_heighteight

            # 現在表示中の図柄を取得
            self._currentsymbol = self._get_currentsymbol()

            # 停止指示がある場合
            if self._stop:
                # 現在表示中の図柄 = 停止目標図柄であれば回転停止
                if self._currentsymbol == self._targetsymbol:
                    self._rotate = False

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbolarray(self) -> list[Symbol]:
        return self._symbolarray

    @property
    def reelimage(self) -> MatLike:
        return self._reelimage

    @property
    def currentcoord(self) -> float:
        return self._currentcoord

    @property
    def currentsymbol(self) -> list[Symbol]:
        return self._currentsymbol

    @property
    def targetsymbol(self) -> list[Symbol] | list[None]:
        return self._targetsymbol

    @property
    def rotate(self) -> bool:
        return self._rotate

    @property
    def stop(self) -> bool:
        return self._stop

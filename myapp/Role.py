from PayLine import PayLine
from Symbol import Symbol


class PressOrder:
    """
    押し順

    Attributes
    ----------
    id : int
        押し順ID
    pressorder : tuple[list[int], list[int], list[int]]
        押し順 [左リール, 中リール, 右リール]
        (1:第一停止, 2:第二停止, 3:第三停止)
    """

    _Id: int = 0

    def __init__(
        self,
        pressorder: tuple[list[int], list[int], list[int]],
    ):
        """
        Parameters
        ----------
        pressorder : tuple[list[int], list[int], list[int]]
            押し順 [左リール, 中リール, 右リール]
            (1:第一停止, 2:第二停止, 3:第三停止)
        """
        self._id: int = PressOrder._Id
        PressOrder._Id += 1

        if not isinstance(pressorder, tuple):
            raise TypeError("押し順の型が不正です")
        if len(pressorder) != 3:
            raise ValueError("押し順の要素数がリール数と一致しません")

        for p_order in pressorder:
            if not isinstance(p_order, list):
                raise TypeError("押し順指定の型が不正です")
            if len(set(p_order)) != len(p_order):
                raise ValueError("同一の押し順が2つ以上指定されています")
            if len(p_order) > 3:
                raise ValueError("押し順指定の要素数が不正です")
            for p_o in p_order:
                if p_o not in [1, 2, 3]:
                    raise ValueError(
                        "押し順指定が不正です "
                        "(1:第一停止, 2:第二停止, 3:第三停止)"
                    )

        if not self._is_pressorder_possible(pressorder):
            raise Exception("押し順が不正です (正解の押し順がありません)")

        self._pressorder = pressorder

    def _is_pressorder_possible(
        self,
        pressorder: tuple[list[int], list[int], list[int]],
    ) -> bool:
        """
        押し順に正解(1, 2, 3)があるか判定する

        Parameters
        ----------
        pressorder : tuple[list[int], list[int], list[int]]
            押し順 [左リール, 中リール, 右リール]
            (1:第一停止, 2:第二停止, 3:第三停止)

        Returns
        -------
        result : bool
            判定結果
        """
        result: bool = False
        for val_l in pressorder[0]:
            for val_c in pressorder[1]:
                for val_r in pressorder[2]:
                    if [val_l, val_c, val_r].sort() == [1, 2, 3]:
                        result = True

        return result

    @property
    def id(self) -> int:
        return self._id

    @property
    def pressorder(
        self,
    ) -> tuple[int | list[int], int | list[int], int | list[int]]:
        return self._pressorder


class Slip:
    """
    滑り

    Attributes
    ----------
    id : int
        滑りID
    validslip : tuple[list[int], list[int], list[int]]
        滑り [左リール, 中リール, 右リール]
        (0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)
    """

    _Id: int = 0

    def __init__(
        self,
        slip: tuple[list[int], list[int], list[int]],
    ):
        """
        Parameters
        ----------
        validslip : tuple[list[int], list[int], list[int]]
            滑り [左リール, 中リール, 右リール]
            (0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)
        """
        self._id = Slip._Id
        Slip._Id += 1

        if not isinstance(slip, tuple):
            raise TypeError("滑りの型が不正です")
        if len(slip) != 3:
            raise ValueError("滑りの要素数がリール数と一致しません")
        for sl in slip:
            if not isinstance(sl, list):
                raise TypeError("滑り指定の型が不正です")
            if len(set(sl)) != len(sl):
                raise ValueError("同一の滑りが2つ以上指定されています")
            if len(sl) > 5:
                raise ValueError("滑り指定の要素数が不正です")
            for s in sl:
                if s not in [0, 1, 2, 3, 4]:
                    raise ValueError(
                        "滑り指定が不正です "
                        "(0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)"
                    )

        self._slip = slip

    @property
    def id(self) -> int:
        return self._id

    @property
    def validslip(
        self,
    ) -> tuple[list[int], list[int], list[int]]:
        return self._slip


class SymbolCombo:
    """
    図柄組合せ

    Attributes
    ----------
    id : int
        図柄組合せID
    symbolcombo : tuple[list[Symbol], list[Symbol], list[Symbol]]
        図柄組合せ [左リール, 中リール, 右リール]
    """

    _Id: int = 0

    def __init__(
        self,
        symbolcombo: tuple[list[Symbol], list[Symbol], list[Symbol]],
    ):
        """
        Parameters
        ----------
        name : str
            図柄組合せ名
        symbolcombo : tuple[list[Symbol], list[Symbol], list[Symbol]]
            図柄組合せ [左リール, 中リール, 右リール]
        """
        self._id: int = SymbolCombo._Id
        SymbolCombo._Id += 1

        if not isinstance(symbolcombo, tuple):
            raise TypeError("図柄組合せの型が不正です")
        if len(symbolcombo) != 3:
            raise ValueError("図柄組合せの要素数がリール数と一致しません")

        for s_combo in symbolcombo:
            if not isinstance(s_combo, list):
                raise TypeError("図柄指定の型が不正です")
            if len(set(s_combo)) != len(s_combo):
                raise ValueError("同一の図柄が2つ以上指定されています")
            for s_c in s_combo:
                if not isinstance(s_c, Symbol):
                    raise TypeError("図柄の型が不正です")

        self._symbolcombo = symbolcombo

    @property
    def id(self) -> int:
        return self._id

    @property
    def symbolcombo(
        self,
    ) -> tuple[list[Symbol], list[Symbol], list[Symbol]]:
        return self._symbolcombo


class Role:
    """
    役

    Attributes
    ----------
    id : int
        役ID
    name : str
        役名
    payout : int
        払出クレジット数
    symbolcombo : SymbolCombo
        図柄組合せ
    payline : list[PayLine]
        入賞ライン
    slip : Slip
        滑り
    pressorder : PressOrder
        押し順指定
    """

    _Id: int = 0

    def __init__(
        self,
        name: str,
        payout: int,
        symbolcombo: SymbolCombo,
        payline: list[PayLine],
        slip: Slip,
        pressorder: PressOrder,
    ):
        """
        Parameters
        ----------
        name : str
            役名
        payout : int
            払出クレジット数
        symbolcombo : SymbolCombo
            図柄組合せ
        payline : list[PayLine]
            入賞ライン
        slip : Slip
            滑り
        pressorder : PressOrder
            押し順指定
        """
        self._id: int = Role._Id
        Role._Id += 1
        self._name: str = name

        if not isinstance(payout, int):
            raise TypeError("払出クレジット数の型が不正です")
        self._payout = payout

        if not isinstance(symbolcombo, SymbolCombo):
            raise TypeError("図柄組合せの型が不正です")
        self._symbolcombo = symbolcombo

        if not isinstance(payline, list):
            raise TypeError("入賞ラインの型が不正です")
        for pl in payline:
            if not isinstance(pl, PayLine):
                raise TypeError("入賞ライン指定の型が不正です")
        self._payline = payline

        if not isinstance(slip, Slip):
            raise TypeError("滑りの型が不正です")
        self._slip = slip

        if not isinstance(pressorder, PressOrder):
            raise TypeError("押し順指定の型が不正です")
        self._pressorder = pressorder

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def payout(self) -> int:
        return self._payout

    @property
    def symbolcombo(self) -> SymbolCombo:
        return self._symbolcombo

    @property
    def payline(self) -> list[PayLine]:
        return self._payline

    @property
    def slip(self) -> Slip:
        return self._slip

    @property
    def pressorder(self) -> PressOrder:
        return self._pressorder

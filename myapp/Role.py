from PayLine import PayLine
from Symbol import Symbol


class PressOrder:
    """
    押し順指定

    Attributes
    ----------
    id : int
        押し順指定ID
    name : str
        押し順指定名
    pressorder : tuple[int | list[int], int | list[int], int | list[int]]
        押し順指定 [左リール, 中リール, 右リール]
        (1:第一停止, 2:第二停止, 3:第三停止)
    """

    _Id: int = 0

    def __init__(
        self,
        name: str,
        pressorder: tuple[int | list[int], int | list[int], int | list[int]],
    ):
        """
        Parameters
        ----------
        name : str
            押し順指定名
        pressorder : tuple[int | list[int], int | list[int], int | list[int]]
            押し順指定 [左リール, 中リール, 右リール]
            (1:第一停止, 2:第二停止, 3:第三停止)
        """
        self._id: int = PressOrder._Id
        PressOrder._Id += 1
        self._name: str = name

        if len(pressorder) != 3:
            raise ValueError("押し順指定の要素数がリール数と一致しません")
        for p_order in pressorder:
            if type(p_order) is int:
                if p_order not in [1, 2, 3]:
                    raise ValueError(
                        "押し順指定が不正です "
                        "(1:第一停止, 2:第二停止, 3:第三停止)"
                    )
            elif type(p_order) is list:
                if len(set(p_order)) != len(p_order):
                    raise ValueError("同一の押し順が2つ以上指定されています")
                if 3 < len(p_order):
                    raise ValueError("押し順指定の要素数が不正です")
                for p_o in p_order:
                    if p_o not in [1, 2, 3]:
                        raise ValueError(
                            "押し順指定が不正です "
                            "(1:第一停止, 2:第二停止, 3:第三停止)"
                        )
            else:
                raise TypeError("押し順指定の型が不正です")

        if not (self._is_pressorder_possible(pressorder)):
            raise Exception("押し順指定が不正です (正解の押し順がありません)")

        self._pressorder: tuple[
            int | list[int], int | list[int], int | list[int]
        ] = pressorder

    def _is_pressorder_possible(
        self,
        pressorder: tuple[int | list[int], int | list[int], int | list[int]],
    ) -> bool:
        """
        押し順指定に正解(1, 2, 3)があるか判定する

        Parameters
        ----------
        pressorder : tuple[int | list[int], int | list[int], int | list[int]]
            押し順指定 [左リール, 中リール, 右リール]
            (1:第一停止, 2:第二停止, 3:第三停止)

        Returns
        -------
        result : bool
            判定結果
        """

        leftreel_value = (
            pressorder[0]
            if isinstance(pressorder[0], (tuple, list, set))
            else (pressorder[0],)
        )
        centerreel_value = (
            pressorder[1]
            if isinstance(pressorder[1], (tuple, list, set))
            else (pressorder[1],)
        )
        rightreel_value = (
            pressorder[2]
            if isinstance(pressorder[2], (tuple, list, set))
            else (pressorder[2],)
        )

        result: bool = False
        for val_l in leftreel_value:
            for val_c in centerreel_value:
                for val_r in rightreel_value:
                    if sorted([val_l, val_c, val_r]) == [1, 2, 3]:
                        result = True

        return result

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def pressorder(
        self,
    ) -> tuple[int | list[int], int | list[int], int | list[int]]:
        return self._pressorder


class ValidSlip:
    """
    有効滑り

    Attributes
    ----------
    id : int
        有効滑りID
    name : str
        有効滑り名
    validslip : tuple[int | list[int], int | list[int], int | list[int]]
        有効滑り [左リール, 中リール, 右リール]
        (0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)
    """

    _Id: int = 0

    def __init__(
        self,
        name: str,
        validslip: tuple[int | list[int], int | list[int], int | list[int]],
    ):
        """
        Parameters
        ----------
        name : str
            滑り名
        validslip : tuple[int | list[int], int | list[int], int | list[int]]
            有効滑り [左リール, 中リール, 右リール]
            (0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)
        """
        self._id = ValidSlip._Id
        ValidSlip._Id += 1
        self._name = name

        if len(validslip) != 3:
            raise ValueError("有効滑り指定の要素数がリール数と一致しません")
        for v_slip in validslip:
            if type(v_slip) is int:
                if v_slip not in [0, 1, 2, 3, 4]:
                    raise ValueError(
                        "有効滑り指定が不正です "
                        "(0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)"
                    )
            elif type(v_slip) is list:
                if len(set(v_slip)) != len(v_slip):
                    raise ValueError("同一の有効滑りが2つ以上指定されています")
                if 5 < len(v_slip):
                    raise ValueError("有効滑り指定の要素数が不正です")
                for v_s in v_slip:
                    if v_s not in [0, 1, 2, 3, 4]:
                        raise ValueError(
                            "有効滑り指定が不正です "
                            "(0: ビタ, 1: 1滑り, 2: 2滑り, 3: 3滑り, 4: 4滑り)"
                        )
            else:
                raise TypeError("有効滑り指定の型が不正です")

        self._validslip: tuple[
            int | list[int], int | list[int], int | list[int]
        ] = validslip

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def validslip(
        self,
    ) -> tuple[int | list[int], int | list[int], int | list[int]]:
        return self._validslip


class SymbolCombo:
    """
    図柄組合せ

    Attributes
    ----------
    id : int
        図柄組合せID
    name : str
        図柄組合せ名
    symbolcombo : tuple[
                    Symbol | list[Symbol],
                    Symbol | list[Symbol],
                    Symbol | list[Symbol]
                    ]
        図柄組合せ [左リール, 中リール, 右リール]
    """

    _Id: int = 0

    def __init__(
        self,
        name: str,
        symbolcombo: tuple[
            Symbol | list[Symbol], Symbol | list[Symbol], Symbol | list[Symbol]
        ],
    ):
        """
        Parameters
        ----------
        name : str
            滑り名
        symbolcombo : tuple[
                        Symbol | list[Symbol],
                        Symbol | list[Symbol],
                        Symbol | list[Symbol]
                        ]
            図柄組合せ [左リール, 中リール, 右リール]
        """
        self._id: int = SymbolCombo._Id
        SymbolCombo._Id += 1
        self._name: str = name

        if len(symbolcombo) != 3:
            raise ValueError("図柄組合せ指定の要素数がリール数と一致しません")
        for s_combo in symbolcombo:
            if type(s_combo) is list:
                if len(set(s_combo)) != len(s_combo):
                    raise ValueError("同一の図柄が2つ以上指定されています")
                for s_c in s_combo:
                    if not isinstance(s_c, Symbol):
                        raise TypeError("図柄の型が不正です")
            elif not isinstance(s_combo, Symbol):
                raise TypeError("図柄の型が不正です")

        self._symbolcombo: tuple[
            Symbol | list[Symbol], Symbol | list[Symbol], Symbol | list[Symbol]
        ] = symbolcombo

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def symbolcombo(
        self,
    ) -> tuple[
        Symbol | list[Symbol], Symbol | list[Symbol], Symbol | list[Symbol]
    ]:
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
    symbolcombo : tuple[
                    Symbol | list[Symbol],
                    Symbol | list[Symbol],
                    Symbol | list[Symbol]
                    ]
        図柄組合せ [左リール, 中リール, 右リール]
    validpayline : PayLine | list[PayLine, ...]
        有効入賞ライン [左リール, 中リール, 右リール]
    validslip : ValidSlip
        有効滑り
    pressorder : PressOrder
        押し順指定
    """

    _Id: int = 0

    def __init__(
        self,
        name: str,
        payout: int,
        symbolcombo: tuple[
            Symbol | list[Symbol], Symbol | list[Symbol], Symbol | list[Symbol]
        ],
        validpayline: PayLine | list[PayLine],
        validslip: ValidSlip,
        pressorder: PressOrder,
    ):
        """
        Parameters
        ----------
        name : str
            役名
        payout : int
            払出クレジット数
        symbolcombo : tuple[
                        Symbol | list[Symbol],
                        Symbol | list[Symbol],
                        Symbol | list[Symbol]
                        ]
            図柄組合せ [左リール, 中リール, 右リール]
        validpayline : PayLine | list[PayLine, ...]
            有効入賞ライン [左リール, 中リール, 右リール]
        validslip : ValidSlip
            有効滑り
        pressorder : PressOrder
            押し順指定
        """
        self._id: int = Role._Id
        Role._Id += 1
        self._name: str = name
        self._payout: int = payout

        if len(symbolcombo) != 3:
            raise ValueError("図柄組合せ指定の要素数がリール数と一致しません")
        for s_combo in symbolcombo:
            if type(s_combo) is list:
                if len(set(s_combo)) != len(s_combo):
                    raise ValueError("同一の図柄が2つ以上指定されています")
                for s_c in s_combo:
                    if not isinstance(s_c, Symbol):
                        raise TypeError("図柄の型が不正です")
            elif not isinstance(s_combo, Symbol):
                raise TypeError("図柄の型が不正です")

        self._symbolcombo: tuple[
            Symbol | list[Symbol], Symbol | list[Symbol], Symbol | list[Symbol]
        ] = symbolcombo

        if type(validpayline) is list:
            if len(set(validpayline)) != len(validpayline):
                raise ValueError("同一の有効ラインが2つ以上指定されています")
            for v_payline in validpayline:
                if not isinstance(v_payline, PayLine):
                    raise TypeError("有効ラインの型が不正です")
        elif not isinstance(validpayline, PayLine):
            raise TypeError("有効ラインの型が不正です")
        self._validpayline: PayLine | list[PayLine] = validpayline

        if not isinstance(validslip, ValidSlip):
            raise TypeError("有効滑りの型が不正です")
        self._validslip: ValidSlip = validslip

        if not isinstance(pressorder, PressOrder):
            raise TypeError("押し順指定の型が不正です")
        self._pressorder: PressOrder = pressorder

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
    def validpayline(self) -> PayLine | list[PayLine]:
        return self._validpayline

    @property
    def validslip(self) -> ValidSlip:
        return self._validslip

    @property
    def pressorder(self) -> PressOrder:
        return self._pressorder

import GameData


class PayLine:
    """入賞ライン

    Attributes
    ----------
    id : int
        入賞ラインID
    payline : tuple[int, int, int]
        入賞ライン [左リール, 中リール, 右リール]
        (0:上段, 1:中段, 2:下段)
    """

    _Id: int = 0

    def __init__(self, payline: tuple[int, int, int]) -> None:
        """
        Parameters
        ----------
        payline : tuple[int, int, int]
            入賞ライン [左リール, 中リール, 右リール]
        """
        self._id: int = PayLine._Id
        PayLine._Id += 1

        if not isinstance(payline, tuple):
            raise TypeError("入賞ラインの型が不正です")
        if len(payline) != 3:
            raise ValueError("入賞ラインの要素数がリール数と一致しません")
        for paypos in payline:
            if not isinstance(paypos, int):
                raise TypeError("入賞位置の型が不正です")
            if paypos not in [
                GameData.REEL_POSITION_TOP,
                GameData.REEL_POSITION_MIDDLE,
                GameData.REEL_POSITION_BOTTOM,
            ]:
                raise ValueError("入賞位置の値が不正です")
        self._payline = payline

    @property
    def id(self) -> int:
        return self._id

    @property
    def payline(self) -> tuple[int, int, int]:
        return self._payline

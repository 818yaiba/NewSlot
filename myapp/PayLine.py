import GameData


class PayLine:
    """入賞ライン

    Attributes
    ----------
    id : int
        ID
    payline : tuple[int, int, int]
        ライン [左リール, 中リール, 右リール]
        (0:上段, 1:中段, 2:下段)
    """

    _Id: int = 0

    def __init__(self, line: tuple[int, int, int]) -> None:
        """
        Parameters
        ----------
        line : tuple[int, int, int]
            ライン [左リール, 中リール, 右リール]
        """
        self._id: int = PayLine._Id
        PayLine._Id += 1

        if not isinstance(line, tuple):
            raise TypeError("入賞ラインの型が不正です")
        if len(line) != 3:
            raise ValueError("入賞ラインの要素数がリール数と一致しません")
        for reel_pos in line:
            if not isinstance(reel_pos, int):
                raise TypeError("入賞位置の型が不正です")
            if reel_pos not in [
                GameData.REEL_POSITION_TOP,
                GameData.REEL_POSITION_MIDDLE,
                GameData.REEL_POSITION_BOTTOM,
            ]:
                raise ValueError("入賞位置の値が不正です")
        self._payline = line

    @property
    def id(self) -> int:
        return self._id

    @property
    def line(self) -> tuple[int, int, int]:
        return self._payline

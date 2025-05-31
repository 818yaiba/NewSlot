import os

import cv2
import GameData
from cv2.typing import MatLike


class Symbol:
    """
    図柄

    Attributes
    ----------
    id : int
        図柄ID
    name : str
        図柄名
    filename : str
        図柄画像ファイル名
    imagefile_path : str
        図柄画像ファイルのパス
    image : MatLike
        図柄画像
    """

    _Id = 0

    def __init__(self, name: str, filename: str) -> None:
        """
        Parameters
        ----------
        name : str
            図柄名
        filename : str
            図柄画像ファイル名
        """
        self._id = Symbol._Id
        Symbol._Id += 1
        self._name = name

        # 図柄画像読み込み
        imagefile_path = os.path.join(GameData.IMAGE_DIRECTORY, filename)
        self._image = cv2.imread(imagefile_path)

        if self._image is None:  # 画像が読み込めなかった場合
            raise FileNotFoundError(
                f"図柄画像ファイルが見つかりません: {imagefile_path}"
            )

        # 図柄画像チェック
        if self._image.shape[1] != GameData.SYMBOL_WIDTH:
            raise ValueError("図柄画像の幅が既定値と一致しません")
        if self._image.shape[0] != GameData.SYMBOL_HEIGHT:
            raise ValueError("図柄画像の高さが既定値と一致しません")

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def image(self) -> MatLike:
        return self._image

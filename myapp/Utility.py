import cv2
import pygame
from cv2.typing import MatLike


def cv2_to_pygame_surface(cv2_image: MatLike) -> pygame.Surface:
    """
    OpenCV (BGR) 画像を Pygame Surface に変換する

    Parameters
    ----------
    cv2_image : MatLike
        OpenCVで扱うBGR形式の画像

    Returns
    -------
    surface: pygame.Surface
        Pygameで描画可能なPygame.Surfaceオブジェクト
    """
    # BGR → RGB に変換
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)

    # numpy配列 → Pygame Surface に変換
    surface = pygame.image.frombuffer(
        rgb_image.tobytes(), rgb_image.shape[1::-1], "RGB"
    )

    return surface

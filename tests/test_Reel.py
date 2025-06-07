import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest

import numpy as np

from myapp import GameData
from myapp.Reel import Reel
from myapp.Symbol import Symbol


class DummySymbol(Symbol):
    def __init__(self, id, name):
        # ダミー画像としてnumpy配列を使用
        self._id = id
        self._name = name
        self._image = np.zeros(
            (GameData.SYMBOL_HEIGHT, GameData.REEL_WIDTH, 3), dtype=np.uint8
        )

    @property
    def image(self):
        return self._image


class TestReel(unittest.TestCase):
    def setUp(self):
        Reel._Id = 0  # クラス変数をリセット
        # ダミーシンボルをリール図柄数分用意
        self.symbols = [
            DummySymbol(i, f"symbol{i}")
            for i in range(GameData.REEL_SYMBOL_LENGTH)
        ]
        self.reel = Reel(self.symbols)

    def test_initialization(self):
        self.assertEqual(self.reel.id, 0)
        self.assertEqual(
            len(self.reel.reel_symbol), GameData.REEL_SYMBOL_LENGTH
        )
        self.assertEqual(self.reel.reel_image.shape[1], GameData.REEL_WIDTH)
        self.assertEqual(self.reel.reel_image.shape[0], GameData.REEL_HEIGHT)
        self.assertIsInstance(self.reel.current_symbol, list)
        self.assertIsInstance(self.reel.target_symbol, list)
        self.assertFalse(self.reel.spinning)
        self.assertTrue(self.reel.stop_request)

    def test_get_n_ahead_symbol(self):
        n = 1
        result = self.reel.get_n_ahead_symbol(n)
        self.assertEqual(len(result), 3)
        self.assertIsInstance(result[0], Symbol)

    def test_reel_start_and_stop(self):
        self.reel.reel_start()
        self.assertTrue(self.reel.spinning)
        self.assertFalse(self.reel.stop_request)
        # 停止指示
        self.reel.stop_spin(0, GameData.REEL_POSITION_TOP)
        self.assertTrue(self.reel.stop_request)
        self.assertIsInstance(self.reel.target_symbol, list)

    def test_get_updated_current_coord(self):
        current = 0.0
        dt = 1.0
        updated = self.reel._get_updated_current_coord(current, dt)
        self.assertTrue(0 <= updated < GameData.REEL_HEIGHT)

    def test_get_reel_image(self):
        image = self.reel._get_reel_image(self.symbols)
        self.assertEqual(image.shape[1], GameData.REEL_WIDTH)
        self.assertEqual(image.shape[0], GameData.REEL_HEIGHT)

    def test_invalid_reel_symbol_length(self):
        with self.assertRaises(ValueError):
            Reel(self.symbols[:2])

    def test_invalid_reel_image_size(self):
        invalid_symbols = [
            DummySymbol(i, f"symbol{i}")
            for i in range(GameData.REEL_SYMBOL_LENGTH)
        ]
        invalid_symbols[0]._image = np.zeros(
            (100, GameData.REEL_WIDTH, 3), dtype=np.uint8
        )
        with self.assertRaises(ValueError):
            Reel(invalid_symbols)

    def test_invalid_reel_image_height(self):
        invalid_symbols = [
            DummySymbol(i, f"symbol{i}")
            for i in range(GameData.REEL_SYMBOL_LENGTH)
        ]
        invalid_symbols[0]._image = np.zeros(
            (GameData.SYMBOL_HEIGHT, 100, 3), dtype=np.uint8
        )
        with self.assertRaises(ValueError):
            Reel(invalid_symbols)

    def test_invalid_reel_image_width(self):
        invalid_symbols = [
            DummySymbol(i, f"symbol{i}")
            for i in range(GameData.REEL_SYMBOL_LENGTH)
        ]
        invalid_symbols[0]._image = np.zeros(
            (GameData.SYMBOL_HEIGHT, 100, 3), dtype=np.uint8
        )
        with self.assertRaises(ValueError):
            Reel(invalid_symbols)


if __name__ == "__main__":
    unittest.main()

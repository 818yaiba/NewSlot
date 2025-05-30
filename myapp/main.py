# MIT License
# Copyright (c) 2025 818yaiba
#
# This file is part of NewSlot and is released under the MIT License.
# See LICENSE file in the root directory for full license text.

import GameData
from Game import Game


def main():
    game = Game(GameData.GAME_TITLE)
    game.main_loop()


if __name__ == "__main__":
    main()

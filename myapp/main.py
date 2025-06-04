# MIT License
# Copyright (c) 2025 818yaiba
#
# This file is part of NewSlot and is released under the MIT License.
# See LICENSE file in the root directory for full license text.

import GameData
import Logger
from Game import Game

Logger.setup_logging()
log = Logger.get_logger(__name__)


def main() -> None:
    log.info("game start")
    game = Game(name=GameData.GAME_TITLE)
    game.main_loop()


if __name__ == "__main__":
    main()

import logging

import config


class Logger:
    """カスタムロガークラス
    Attributes:
    ----------
    name : str
        ロガーの名前
    level : int
        ログレベル（デフォルトはINFO）
    filename : str | None
        ログファイル名（指定しない場合は標準出力のみ）
    """

    def __init__(self, name, level=config.LOG_LEVEL, filename=None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

        # 既存のハンドラをクリア（多重出力防止）
        if self.logger.hasHandlers():
            self.logger.handlers.clear()

        # 標準出力
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # ファイル出力が必要な場合
        if filename:
            file_handler = logging.FileHandler(filename)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

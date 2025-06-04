import logging
import os
from datetime import datetime

import config

# ログ設定が一度だけ行われるようにフラグを用意
_is_configured = False


def setup_logging():
    global _is_configured
    if _is_configured:
        return  # すでに設定済みなら何もしない

    os.makedirs(config.LOG_DIR, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(config.LOG_DIR, f"log_{now}.log")

    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        handlers=[logging.StreamHandler(), logging.FileHandler(log_file)],
    )
    _is_configured = True


def get_logger(name: str):
    return logging.getLogger(name)

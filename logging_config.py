import os
import logging
from logging.handlers import RotatingFileHandler


def setup_logging(
    log_dir: str = "logs",
    log_file: str = "app.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 單個檔案最大 10MB
    backup_count: int = 5,  # 保留最近 5 個備份檔案
) -> None:
    """
    初始化日誌設定。

    :param log_dir: 日誌存放目錄
    :param log_file: 日誌檔案名稱
    :param level: 日誌記錄的層級
    :param max_bytes: 日誌檔案大小限制)
    :param backup_count: 保留的舊日誌檔案數量
    """
    # 建立日誌目錄
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, log_file)

    # 定義日誌格式
    # %(asctime)s  : 輸出時間
    # %(levelname)s: 日誌層級
    # %(filename)s : 觸發日誌的檔名
    # %(lineno)d   : 觸發日誌的行號
    # %(message)s  : 日誌內容
    log_format = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    # 取得 Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 避免重複添加 Handler
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # 1. 輸出到控制台的 Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    console_handler.setLevel(level)
    root_logger.addHandler(console_handler)

    # 2. 輸出到檔案並支援自動輪替的 Handler
    file_handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backup_count, encoding="utf-8")
    file_handler.setFormatter(log_format)
    file_handler.setLevel(level)
    root_logger.addHandler(file_handler)

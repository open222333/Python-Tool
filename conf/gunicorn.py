# gunicorn_config.py
import logging
from logging.handlers import RotatingFileHandler


bind = '127.0.0.1:8000'  # 監聽的 IP 和 Port
workers = 4              # Worker 的數量
timeout = 120            # 超時時間，單位為秒
# loglevel = 'info'        # 設定日誌級別，可選值：debug, info, warning, error, critical
# accesslog = '-'          # 設定存放訪問日誌的文件路徑，'-' 表示輸出到標準輸出
# errorlog = '-'           # 設定存放錯誤日誌的文件路徑，'-' 表示輸出到標準輸出

# Set the log file path
log_file = 'logs/gunicorn.log'

# Set the log level
log_level = 'info'

# Set the log file size limit to 100MB
log_file_max_size = 100 * 1024 * 1024

# Set the number of backup log files
log_file_backup_count = 5

# Logging configuration
accesslog = '/path/to/gunicorn/logs/access.log'
errorlog = '/path/to/gunicorn/logs/error.log'

# Configure the logger with a RotatingFileHandler
logger = logging.getLogger()
logger.setLevel(logging.getLevelName(log_level.upper()))
handler = RotatingFileHandler(
    log_file,
    maxBytes=log_file_max_size,
    backupCount=log_file_backup_count
)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

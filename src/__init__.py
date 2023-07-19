from configparser import ConfigParser
import logging
import json
import os


conf = ConfigParser()
conf.read('.conf/config.ini', encoding='utf-8')


# logs相關參數
# 關閉log功能 輸入選項 (true, True, 1) 預設 不關閉
LOG_DISABLE = conf.getboolean('LOG', 'LOG_DISABLE', fallback=False)
# logs路徑 預設 logs
LOG_PATH = conf.get('LOG', 'LOG_PATH', fallback='logs')
# 設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING
LOG_LEVEL = conf.get('LOG', 'LOG_LEVEL', fallback='WARNING')
# 關閉紀錄log檔案 輸入選項 (true, True, 1)  預設 關閉
LOG_FILE_DISABLE = conf.getboolean('LOG', 'LOG_FILE_DISABLE', fallback=True)

if LOG_DISABLE:
    logging.disable()

# 設定資料的json路徑 預設值 .conf/domains.json
DOMAINS_JSON_PATH = conf.get('SETTING', 'DOMAINS_JSON_PATH', fallback='.conf/domains.json')
with open(DOMAINS_JSON_PATH, 'r') as f:
    DOMAINS_INFO = json.loads(f.read())

#  設定指令輸出txt路徑 預設值 output/command.txt
OUTPUT_PATH = conf.get('SETTING', 'OUTPUT_PATH', fallback='output')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# 設定輸入資料的txt路徑 預設值 target.txt
TXT_PATH = conf.get('SETTING', 'TXT_PATH', fallback='target.txt')

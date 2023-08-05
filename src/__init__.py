from configparser import ConfigParser
import logging
import json
import os


conf = ConfigParser()
conf.read('conf/config.ini', encoding='utf-8')


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

# 設定域名資料的json檔路徑 預設值 conf/domains.json
DOMAINS_JSON_PATH = conf.get('SETTING', 'DOMAINS_JSON_PATH', fallback='conf/domains.json')
with open(DOMAINS_JSON_PATH, 'r') as f:
    DOMAINS_INFO = json.loads(f.read())

# 設定輸出路徑 預設值 output
OUTPUT_PATH = conf.get('SETTING', 'OUTPUT_PATH', fallback='output')
if not os.path.exists(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH)

# 設定輸入資料的txt路徑 預設值 target.txt
TXT_PATH = conf.get('SETTING', 'TXT_PATH', fallback='target.txt')

NGINX_DIR = conf.get('SETTING', 'NGINX_DIR', fallback='/etc/nginx')
# 設定nameserver資料的json檔路徑 預設值 conf/ns_info.json
NS_JSON_PATH = conf.get('SETTING', 'NS_JSON_PATH', fallback='conf/ns_info.json')
with open(NS_JSON_PATH, 'r') as f:
    NS_INFO = json.loads(f.read())

# 設定主機資訊json檔路徑 預設值 conf/host.json
HOST_JSON_PATH = conf.get('SETTING', 'HOST_JSON_PATH', fallback='conf/host.json')
with open(NS_JSON_PATH, 'r') as f:
    HOST_INFO = json.loads(f.read())

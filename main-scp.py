import os
from src.logger import Log
from src import HOST_INFO
from argparse import ArgumentParser

parser = ArgumentParser(description='批量傳送檔案')
parser.add_argument('-l', '--log_level', type=str, default='WARNING', help='設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING')
parser.add_argument('-t', '--test', type=bool, default=False, help='是否為測試')
argv = parser.parse_args()

logger = Log(__name__)
logger.set_msg_handler()
logger.set_level(argv.log_level)

if __name__ == '__main__':
    try:
        for host_info in HOST_INFO:
            if host_info['execute']:
                if os.path.isdir(host_info["local_path"]):
                    command = f'sshpass -p {host_info["password"]} scp -r {host_info["local_path"]} {host_info["username"]}@{host_info["host"]}:{host_info["remote_path"]}'
                else:
                    command = f'sshpass -p {host_info["password"]} scp {host_info["local_path"]} {host_info["username"]}@{host_info["host"]}:{host_info["remote_path"]}'
                logger.debug(command)
                if not argv.test:
                    os.system(command)
    except Exception as err:
        logger.error(msg=err, exc_info=True)

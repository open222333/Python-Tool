from argparse import ArgumentParser
from datetime import datetime
from src import TXT_PATH, OUTPUT_PATH, LOG_LEVEL, LOG_FILE_DISABLE, LOG_PATH, CLOUDFLARE_CLI_INFO
from src.logger import Log
from src.nginx import SSLNginxCommand
from src.tool import generate_txt, print_command, get_domain_list_from_email, get_all_files
import os

parser = ArgumentParser(description='根據txt檔，解析郵件格式並生成域名證書相關指令')
group = parser.add_argument_group('生成command功能')
group.add_argument('--cli', choices=CLOUDFLARE_CLI_INFO,
                   help='指定cli檔', default=None, required=False)
group.add_argument('-d', '--txt_dir_path', type=str,
                   default='txt_dir', help='指定cli檔')
show_group = parser.add_argument_group('顯示command功能')
show_group.add_argument(
    '-m', '--print_command', action='store_true',
    help='終端機印出指令'
)
show_group.add_argument(
    '-t', '--generate_txt', action='store_true',
    help='產生txt檔記錄指令'
)
show_group.add_argument(
    '-l', '--log_level', type=str, help='設定紀錄log等級 DEBUG,INFO,WARNING,ERROR,CRITICAL 預設WARNING',
    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], default=None
)
args = parser.parse_args()

txt_logger = Log()
if args.log_level:
    txt_logger.set_level(args.log_level)
else:
    txt_logger.set_level(LOG_LEVEL)
if LOG_PATH != 'logs':
    txt_logger.set_log_path(LOG_PATH)
if not LOG_FILE_DISABLE:
    txt_logger.set_file_handler()
txt_logger.set_msg_handler()

if __name__ == "__main__":

    os.makedirs(args.txt_dir_path, exist_ok=True)
    files = get_all_files(args.txt_dir_path, extensions=[
                          'txt'], add_abspath=True)

    for file in files:

        if args.cli != None:
            if args.cli != filename:
                continue

        commands = {}

        filename = os.path.basename(file)
        commands[f'================{filename}================'] = ''
        domain_list = get_domain_list_from_email(file)

        if len(domain_list[0]) == 0:
            continue

        slc = SSLNginxCommand(
            domains=domain_list[0],
            cli_ini=f'cli-{args.cli}.ini',
            refer_domain="",
            logger=txt_logger
        )

        command_txt_path = f'{OUTPUT_PATH}/commands-{datetime.now().__format__("%Y%m%d")}.txt'

        commands['刷新證書 certbot 指令'] = slc.renew_ssl_command()

        for title in commands.keys():
            if args.print_command:
                print(title)
                print(domain_list[1])
                print_command(commands[title])
            if args.generate_txt:
                generate_txt(command_txt_path, commands[title], title)

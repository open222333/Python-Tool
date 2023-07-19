from argparse import ArgumentParser
from datetime import datetime
from src.nginx import SSLNginxCommand
from src.logger import Log
from src.tool import generate_txt, print_command, get_domain_list
from src import TXT_PATH, OUTPUT_PATH, LOG_LEVEL, LOG_FILE_DISABLE, LOG_PATH

parser = ArgumentParser()
group = parser.add_argument_group('生成command功能')
group.add_argument('--cli', type=str, help='指定cli檔', required=True)
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

    slc = SSLNginxCommand(
        domains=get_domain_list(TXT_PATH),
        cli_ini=args.cli,
        refer_domain="",
        logger=txt_logger
    )
    
    command_txt_path = f'{OUTPUT_PATH}/commands-{datetime.now().__format__("%Y%m%d")}.txt'
    commands = {}

    commands['刷新證書 certbot 指令'] = slc.renew_ssl_command()

    for title in commands.keys():
        if args.print_command:
            print_command(commands[title])
        if args.generate_txt:
            generate_txt(command_txt_path, commands[title], title)

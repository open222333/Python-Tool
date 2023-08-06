from argparse import ArgumentParser
from datetime import datetime
from src.nginx import SSLNginxCommand
from src.logger import Log
from src.tool import generate_txt, print_command
from src import DOMAINS_INFO, OUTPUT_PATH, LOG_LEVEL, LOG_FILE_DISABLE, LOG_PATH


parser = ArgumentParser(description='根據json檔，生成指令')
group = parser.add_argument_group('生成command功能')
group.add_argument(
    '-d', '--dig_check_command', action='append', type=str,
    help='生成 產生dig檢查record 類型指令串列',
    choices=['SOA', 'NS', 'A', 'AAAA', 'PTR', 'CNAME', 'MX']
)
group.add_argument(
    '-c', '--create_ssl_command', action='store_true',
    help='生成 產生新證書certbot指令串列'
)
group.add_argument(
    '-r', '--renew_ssl_command', action='store_true',
    help='生成 刷新證書certbot指令串列'
)
group.add_argument(
    '-R', '--revoke_ssl_command', action='store_true',
    help='生成 註銷證書certbot指令串列'
)
group.add_argument(
    '-C', '--cp_nginx_config_command', action='store_true',
    help='生成 複製 nginx conf 指令串列'
)
group.add_argument(
    '-e', '--remove_conf_command', action='store_true',
    help='生成 刪除 nginx config 指令串列'
)
group.add_argument(
    '-s', '--show_ssl_certificates_command', action='store_true',
    help='生成 顯示證書資料夾指令串列'
)
group.add_argument(
    '-S', '--show_nginx_configs_command', action='store_true',
    help='生成 查找 nginx config指令串列'
)
group.add_argument(
    '-T', '--create_test_url', action='store_true',
    help='生成 測試網址'
)
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

nginx_logger = Log()
if args.log_level:
    nginx_logger.set_level(args.log_level)
else:
    nginx_logger.set_level(LOG_LEVEL)
if LOG_PATH != 'logs':
    nginx_logger.set_log_path(LOG_PATH)
if not LOG_FILE_DISABLE:
    nginx_logger.set_file_handler()
nginx_logger.set_msg_handler()


if __name__ == "__main__":

    for info in DOMAINS_INFO:
        if info['execute']:
            slc = SSLNginxCommand(
                domains=str(info['domains']).split(','),
                cli_ini=info['cloudflare_cli'],
                refer_domain=info['refer_domain'],
                logger=nginx_logger
            )

            command_txt_path = f'{OUTPUT_PATH}/commands-{datetime.now().__format__("%Y%m%d")}.txt'
            commands = {}

            if args.dig_check_command:
                for dig_type in args.dig_check_command:
                    commands[f'檢查 record-{dig_type} 指令'] = slc.dig_check_command(dig_type)
            if args.create_ssl_command:
                commands['新證書 certbot 指令'] = slc.create_ssl_command()
                commands['檢查證書是否生成 指令'] = slc.create_check_ssl_command()
            if args.renew_ssl_command:
                commands['刷新證書 certbot 指令'] = slc.renew_ssl_command()
            if args.revoke_ssl_command:
                commands['註銷證書 certbot 指令'] = slc.revoke_ssl_command()
            if args.cp_nginx_config_command:
                commands['複製 nginx conf 指令'] = slc.cp_nginx_config_command()
            if args.remove_conf_command:
                commands['刪除 nginx config 指令'] = slc.remove_conf_command()
            if args.show_ssl_certificates_command:
                commands['顯示證書資料夾指令'] = slc.show_ssl_certificates_command()
            if args.show_nginx_configs_command:
                commands['查找 nginx config 指令'] = slc.show_nginx_configs_command()
            if args.create_test_url:
                commands['生成 測試網址'] = slc.create_test_url()

            for title in commands.keys():
                if args.print_command:
                    print(title)
                    print_command(commands[title])
                if args.generate_txt:
                    generate_txt(command_txt_path, commands[title], title)

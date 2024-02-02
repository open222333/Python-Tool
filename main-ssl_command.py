from argparse import ArgumentParser
from datetime import datetime
import subprocess
import os

from src.nginx import SSLNginxCommand, DownloadLink, WebLink, SSLCertificate
from src.logger import Log
from src.tool import generate_txt, print_command, is_punycode, domain_decode
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
group.add_argument(
    '-D', '--create_download_url', action='store_true',
    help='生成 下載包網址'
)
group.add_argument(
    '-w', '--create_web_url', action='store_true',
    help='生成 網站服務網址'
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
show_group.add_argument(
    '--commonly', action='store_true',
    help='常用指令 產生新證書certbot指令串列 複製 nginx conf 指令串列 測試網址'
)
show_group.add_argument(
    '--check_ssl_days', action='store_true',
    help='常用指令 域名的 SSL 證書剩餘有效期的天數'
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
        if info.get('execute'):
            slc = SSLNginxCommand(
                domains=str(info['domains']).split(','),
                cli_ini=info['cloudflare_cli'],
                refer_domain=info['refer_domain'],
                logger=nginx_logger
            )

            command_txt_path = f'{OUTPUT_PATH}/commands-{datetime.now().__format__("%Y%m%d")}.txt'
            commands = {}

            # 將 note 當成分隔線
            commands[f'{str(info.get("note")).center(100, "=")}'] = ''

            if args.dig_check_command:
                for dig_type in args.dig_check_command:
                    dig_check_commands = slc.dig_check_command(dig_type)
                    # commands[f'檢查 record-{dig_type} 指令'] = dig_check_commands
                results = []
                for domain, dig_check_command in dig_check_commands.items():
                    result = subprocess.run(dig_check_command, shell=True, capture_output=True, text=True)
                    # result = os.system(dig_check_command)
                    msg = f'{dig_check_command}'
                    if is_punycode(domain):
                        msg = f'{msg} ({domain_decode(domain)})'
                    msg = f'{msg} 結果:\n{result}'
                    results.append(msg)
                commands[f'檢查 record-{dig_type} 結果'] = results

            if args.create_ssl_command:
                commands['新證書 certbot 指令'] = slc.create_ssl_command()
                commands['檢查證書是否生成 指令'] = slc.create_check_ssl_command()
                commands['git 指令'] = ['git add .', 'git commit -m 新增證書', 'git push']
            if args.renew_ssl_command:
                commands['刷新證書 certbot 指令'] = slc.renew_ssl_command()
                commands['git 指令'] = ['git add .', 'git commit -m 刷新證書', 'git push']
            if args.revoke_ssl_command:
                commands['註銷證書 certbot 指令'] = slc.revoke_ssl_command()
            if args.cp_nginx_config_command:
                commands['複製 nginx conf 指令'] = slc.cp_nginx_config_command()
                commands['複製 nginx conf 指令(強制覆蓋)'] = slc.cp_nginx_config_command(force=True)
            if args.remove_conf_command:
                commands['刪除 nginx config 指令'] = slc.remove_conf_command()
            if args.show_ssl_certificates_command:
                commands['顯示證書資料夾指令'] = slc.show_ssl_certificates_command()
            if args.show_nginx_configs_command:
                commands['查找 nginx config 指令'] = slc.show_nginx_configs_command()
            if args.create_test_url:
                commands['生成 測試網址'] = slc.create_test_url()
            if args.commonly:
                commands['新證書 certbot 指令'] = slc.create_ssl_command()
                commands['檢查證書是否生成 指令'] = slc.create_check_ssl_command()
                commands['git 指令'] = ['git add .', 'git commit -m 新增證書', 'git push']
                commands['複製 nginx conf 指令'] = slc.cp_nginx_config_command()
                commands['生成 測試網址'] = slc.create_test_url()
            if args.create_download_url:
                dl = DownloadLink(
                    domains=str(info['domains']).split(','),
                    cli_ini=info['cloudflare_cli'],
                    refer_domain=info['refer_domain'],
                    logger=nginx_logger
                )
                
                dl.sub_domains = []
                if dl.cli_ini == 'cli-domainame99.ini':
                    dl.add_sub_domains('badl', 'ba9', 'bajk', 'bain', 'ba988')
                elif dl.cli_ini == 'cli-tv9999.ini':
                    dl.add_sub_domains('batv', 'baduck', 'bahy')

                commands['下載包域名 依照主域名排序'] = dl.create_link_sort_by_main()
                commands['下載包域名 依照子域名排序'] = dl.create_link_sort_by_sub()
                commands['新證書 certbot 指令'] = dl.create_ssl_command()
                commands['檢查證書是否生成 指令'] = dl.create_check_ssl_command()
                commands['git 指令'] = ['git add .', 'git commit -m 新增證書', 'git push']
                commands['下載包域名 測試網址'] = dl.create_test_url()

                import_cloudflare_txts = []
                for domain in dl.domains:
                    import_cloudflare_txt = ';; CNAME Records\n'
                    for sub_domain in dl.sub_domains:
                        import_cloudflare_txt += f'{sub_domain}\t1\tIN\tCNAME\t{sub_domain}.{domain}.cdn_domain.\n'

                    import_cloudflare_txts.append(import_cloudflare_txt)

                commands['匯入 cloudflare 用 (需替換 cdn_domain)'] = import_cloudflare_txts

                # 子域名 dig 指令
                # for dig_type in args.dig_check_command:
                #     dig_check_commands = dl.dig_check_command(dig_type)
                #     # commands[f'檢查 record-{dig_type} 指令'] = dig_check_commands
                # results = []
                # for domain, dig_check_command in dig_check_commands.items():
                #     result = subprocess.run(dig_check_command, shell=True, capture_output=True, text=True)
                #     # result = os.system(dig_check_command)
                #     msg = f'{dig_check_command}'
                #     if is_punycode(domain):
                #         msg = f'{msg} ({domain_decode(domain)})'
                #     msg = f'{msg} 結果:\n{result.stdout}'
                #     results.append(msg)
                # commands[f'檢查 record-{dig_type} 結果'] = results

            if args.create_web_url:
                wl = WebLink(
                    domains=str(info['domains']).split(','),
                    cli_ini=info['cloudflare_cli'],
                    refer_domain=info['refer_domain'],
                    logger=nginx_logger
                )
                commands['網站服務域名 依照主域名排序'] = wl.create_link_sort_by_main()
                commands['網站服務域名 依照子域名排序'] = wl.create_link_sort_by_sub()
                commands['新證書 certbot 指令'] = wl.create_ssl_command()
                commands['檢查證書是否生成 指令'] = wl.create_check_ssl_command()
                commands['git 指令'] = ['git add .', 'git commit -m 新增證書', 'git push']
                commands['網站服務域名 JK IN 測試網址'] = wl.create_test_url(web='jk')
                commands['網站服務域名 AV9 測試網址'] = wl.create_test_url(web='av9')
                commands['網站服務域名 PTV DUCK KISSME 測試網址'] = wl.create_test_url(web='ptv')

            if args.check_ssl_days:
                sslc = SSLCertificate(
                    domains=str(info['domains']).split(','),
                    logger=nginx_logger
                )
                commands['域名的 SSL 證書剩餘有效期的天數'] = sslc.get_ssl_certificate_expiration_date()

            for title in commands.keys():
                if args.print_command:
                    print(title)
                    print_command(commands[title])
                if args.generate_txt:
                    generate_txt(command_txt_path, commands[title], title)

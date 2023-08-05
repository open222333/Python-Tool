from src import NGINX_DIR, NS_INFO
from src.nameserver import NameServerTool
from src.tool import ProgressBar, get_all_files, get_domain_from_nginx_config
from argparse import ArgumentParser


parser = ArgumentParser(description='根據 nginx conf 設定檔名, 取得 domain')
parser.add_argument('-o', '--output_filename', help='輸出檔名稱', default='check_nginx_nameserver_result.txt')
args = parser.parse_args()


if __name__ == " __main__":
    count = 0
    with open(args.output_filename, 'w') as f:
        p = ProgressBar()
        files = get_all_files(dir_path=NGINX_DIR, extensions=['conf'])
        for conf in files:
            count += 1
            p(len(files), in_loop=True)
            file_name = get_domain_from_nginx_config(conf)
            nst = NameServerTool(domain=file_name)
            if nst.is_domain():
                for ns in NS_INFO:
                    if ns['execute']:
                        nst.set_nameservers(ns['ns'])
                        if not nst.is_ns_match():
                            f.write(f'{file_name}: {ns["name"]}\n')

from src.tool import domain_encode
from src import TXT_PATH
from argparse import ArgumentParser


parser = ArgumentParser(description='批量域名轉碼（編碼） punycode格式')
parser.add_argument('-f', '--file_path', help='指定解析txt檔路徑', default=TXT_PATH)
parser.add_argument('-d', '--output', help='指定輸出結果文檔路徑', default='output/domain_encode.txt')
args = parser.parse_args()

if __name__ == "__main__":
    with open(args.file_path, 'r') as f:
        domains = f.read().split('\n')

    with open(args.output, 'a') as f:
        for domain in domains:
            encode_domain = domain_encode(domain)
            f.write(f'{domain} {encode_domain}\n')

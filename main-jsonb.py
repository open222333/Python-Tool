from src import CONVERT_JSON_TO_JSONB_DIR_PATH
from src.tool import get_all_files
from src.crypto import convert_str_to_base64, convert_base64_to_str
from argparse import ArgumentParser
import os

parser = ArgumentParser()
parser.add_argument('--convert_to_base64', action='store_true', help='轉換 json 成 jsonb')
parser.add_argument('--convert_to_json', action='store_true', help='轉換 jsonb 成 json')
parser.add_argument('--output', type=str, help='輸出資料夾', default='output')
args = parser.parse_args()

if __name__ == "__main__":

        if args.convert_to_base64:
            files = get_all_files(
                dir_path=CONVERT_JSON_TO_JSONB_DIR_PATH,
                extensions=['json'],
                add_abspath=True
            )

        if args.convert_to_json:
            files = get_all_files(
                dir_path=CONVERT_JSON_TO_JSONB_DIR_PATH,
                extensions=['jsonb'],
                add_abspath=True
            )

        # print(files)

        for file in files:
            subdir = os.path.dirname(file)
            basename = os.path.basename(file)

            with open(file, 'r') as f:
                content = f.read()

            outdirname = os.path.join(subdir, f'{os.path.basename(subdir)}_{args.output}')
            os.makedirs(outdirname, exist_ok=True)

            if args.convert_to_base64:
                with open(os.path.join(outdirname, f'{basename}b'), 'w') as f:
                    f.write(convert_str_to_base64(content))
            if args.convert_to_json:
                with open(os.path.join(outdirname, f'{basename.replace("jsonb", "json")}'), 'w') as f:
                    f.write(convert_base64_to_str(content))

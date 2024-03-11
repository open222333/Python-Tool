from src import CONVERT_JSON_TO_JSONB_DIR_PATH
from src.tool import get_all_files
from src.crypto import convert_str_to_base64
import os

if __name__ == "__main__":
    files = get_all_files(CONVERT_JSON_TO_JSONB_DIR_PATH, ['json'])
    for file in files:
        with open(os.path.join(CONVERT_JSON_TO_JSONB_DIR_PATH, file), 'r') as f:
            content = f.read()
        os.makedirs(os.path.join(CONVERT_JSON_TO_JSONB_DIR_PATH, 'output'), exist_ok=True)
        with open(os.path.join(os.path.join(CONVERT_JSON_TO_JSONB_DIR_PATH, 'output'), f'{file}b'), 'w') as f:
            f.write(convert_str_to_base64(content))

import re
import os
import sys
import string
import random
from pathlib import Path
from .logger import Log
from . import LOG_LEVEL

tool_logger = Log('tool')
tool_logger.set_level(LOG_LEVEL)
tool_logger.set_msg_handler()


class ProgressBar():
    '''進度條'''

    def __init__(self, title='Progress', symbol='=', bar_size=50) -> None:
        '''進度表屬性'''
        self.title = title
        self.symbol = symbol
        self.bar_size = bar_size
        self.done = 0  # 迴圈內 使用

    def __call__(self, total: int, done=1, decimal=1, in_loop=False):
        '''
        in_loop: 建立的實體是否在迴圈內使用
        '''
        if in_loop:
            self.done += done
            if self.done >= total:
                self.done = total
            self.__print_progress_bar(self.done, total, decimal)
            if self.done == total:
                self.__done()
        else:
            count = 0
            while True:
                count += done
                if count >= total:
                    count = total
                self.__print_progress_bar(count, total, decimal)
                if count == total:
                    break
            self.__done()

    def __print_progress_bar(self, done, total, decimal):
        '''
        繪製 進度表
        done:完成數
        total:總任務數
        decimal: 百分比顯示到後面幾位
        '''
        # 計算百分比
        precent = float(round(100 * done / total, decimal))
        done_symbol = int(precent / 100 * self.bar_size)
        left = self.symbol * done_symbol
        right = ' ' * (self.bar_size - done_symbol)
        # 顯示進度條
        bar = f"\r{self.title}:[{left}{right}] {format(precent, f'.{decimal}f')}% {done}/{total}"
        sys.stdout.write(bar)
        sys.stdout.flush()

    def __done(self):
        print()


def is_chinese(string: str) -> bool:
    """是否有中文

    Args:
        string (str): _description_

    Returns:
        bool: 是中文 回傳True
    """
    return bool(re.search('[\u4e00-\u9fff]', string))


def is_english(string: str) -> bool:
    """是否為英文

    Args:
        string (str): _description_

    Returns:
        bool: 是英文 回傳True
    """
    return bool(re.search('[a-zA-Z]', string))


def is_punycode(domain: str):
    """是否為punycode

    Args:
        domain (str): _description_

    Returns:
        _type_: _description_
    """
    # import idna
    # try:
    #     idna.decode(domain)
    #     return True
    # except idna.IDNAError:
    #     return False
    punycode_pattern = re.compile(r"xn--")
    return punycode_pattern.search(domain)


def domain_encode(domain: str) -> str:
    """域名轉碼（編碼） punycode格式

    輸入: 例子.com\n
    輸出: xn--fsq33d9b.com\n

    Args:
        domain (str): 中文域名

    Returns:
        str
    """
    import idna
    try:
        if is_chinese(domain):
            punycode = idna.encode(domain).decode('utf-8')
            return punycode
        else:
            return domain
    except Exception as err:
        tool_logger.error(f'域名轉碼（編碼） punycode格式 發生錯誤: {err}')
        return None


def domain_decode(domain: str) -> str:
    """域名轉碼（解碼） punycode格式

    輸入: 例子.com\n
    輸出: xn--fsq33d9b.com\n

    Args:
        domain (str): 中文域名

    Returns:
        str
    """
    import idna
    try:
        punycode = idna.decode(domain)
        return punycode
    except Exception as err:
        return err


def generate_txt(path: str, commands: list, title: str = None):
    """產生 txt檔 記錄指令

    Args:
        path (str): 輸出路徑
        commands (list): 指令串列
        title (str, optional): 輸入標題. Defaults to None.
    """
    with open(path, 'a') as f:
        if title:
            f.write(f'{title}:\n')
        for command in commands:
            f.write(f'{command}\n')
        f.write('\n')


def print_command(commands: list):
    """終端機印出指令

    Args:
        commands (list): 指令串列
    """
    print()
    for command in commands:
        print(f'{command}')
    print()


def parse_domain(domain: str):
    if len(domain.split('.')) > 2:
        match = re.match(
            r'^(?P<subdomain>[^.]+)\.(?P<main_domain>.+\..+)$', domain)
        if match:
            return match.group('subdomain'), match.group('main_domain')
    else:
        return None, domain


def get_domain_list_from_email(path: str = None, show_msg=True, sld=True) -> set[list, str]:
    """解析郵件訊息 取得 域名

    Args:
        path (_type_, optional): 需解析txt路徑. Defaults to None.
        show_msg (bool, optional): 顯示結果. Defaults to True.
        sld (bool, optional): 回傳二級域名. Defaults to True.

    Returns:
        set[list, str]: _description_
    """
    domain_list = []
    domain_dict = {}

    count = 0
    msg = ''

    if not os.path.exists(path):
        tool_logger.error(f'{path} 不存在')

    with open(path, 'r') as f:
        content = f.read().splitlines()

    pattern = r'- name:'
    for domain in content:
        if re.match(pattern, domain):
            count += 1
            domain = re.sub(pattern, ' ', domain).replace(' ', '')
            sub_domain = re.findall(r'www\.(.*)', domain)
            if sub_domain:
                if not sub_domain[0] in domain_list:
                    domain_list.append(domain)
            else:
                domain_list.append(domain)

    if show_msg:
        msg += f'\n總筆數 共{count}個 去除www後共{len(domain_list)}個\n'
        tool_logger.info(f'\n總筆數 共{count}個 去除www後共{len(domain_list)}個\n')
        for d in domain_list:
            msg += f'{d}\n'
            tool_logger.info(d)

    if sld:
        for domain in domain_list:

            subdomain, main_domain = parse_domain(domain)
            if main_domain not in domain_dict.keys():
                if subdomain != None:
                    domain_dict[main_domain] = [subdomain]
                else:
                    domain_dict[main_domain] = []
            else:
                if subdomain != None:
                    domain_dict[main_domain].append(subdomain)

        if show_msg:
            msg += f'\n二級域名 共{len(domain_dict.values()) + len(domain_dict.keys())}個\n'
            tool_logger.info(
                f'\n二級域名 共{len(domain_dict.values()) + len(domain_dict.keys())}個\n\n')
            for main_domain in domain_dict.keys():
                for sub in domain_dict[main_domain]:

                    msg += f'{sub}.{main_domain}\n'
                    tool_logger.info(f'{sub}.{main_domain}')
                msg += '\n'

            msg += f'\n需手動更新 共{len(domain_dict.keys())}個\n'
            tool_logger.info(f'\n需手動更新 共{len(domain_dict.keys())}個\n')
            for main_domain in domain_dict.keys():
                msg += f'{main_domain}\n'
                tool_logger.info(main_domain)

        return (domain_dict.keys(), msg)
    return (domain_list, msg)


def get_domain_list_from_email_str(content: str = None, show_msg=True, sld=True) -> set[list, str]:
    """解析郵件訊息 取得 域名

    Args:
        path (_type_, optional): 需解析txt路徑. Defaults to None.
        show_msg (bool, optional): 顯示結果. Defaults to True.
        sld (bool, optional): 回傳二級域名. Defaults to True.

    Returns:
        set[list, str]: _description_
    """
    domain_list = []
    domain_dict = {}

    count = 0
    msg = ''

    content = content.splitlines()

    pattern = r'- name:'
    for domain in content:
        if re.match(pattern, domain):
            count += 1
            domain = re.sub(pattern, ' ', domain).replace(' ', '')
            sub_domain = re.findall(r'www\.(.*)', domain)
            if sub_domain:
                if not sub_domain[0] in domain_list:
                    domain_list.append(domain)
            else:
                domain_list.append(domain)

    if show_msg:
        msg += f'\n總筆數 共{count}個 去除www後共{len(domain_list)}個\n'
        tool_logger.info(f'\n總筆數 共{count}個 去除www後共{len(domain_list)}個\n')
        for d in domain_list:
            msg += f'{d}\n'
            tool_logger.info(d)

    if sld:
        for domain in domain_list:

            subdomain, main_domain = parse_domain(domain)
            if main_domain not in domain_dict.keys():
                if subdomain != None:
                    domain_dict[main_domain] = [subdomain]
                else:
                    domain_dict[main_domain] = []
            else:
                if subdomain != None:
                    domain_dict[main_domain].append(subdomain)

        if show_msg:
            msg += f'\n二級域名 共{len(domain_dict.values()) + len(domain_dict.keys())}個\n'
            tool_logger.info(
                f'\n二級域名 共{len(domain_dict.values()) + len(domain_dict.keys())}個\n\n')
            for main_domain in domain_dict.keys():
                for sub in domain_dict[main_domain]:

                    msg += f'{sub}.{main_domain}\n'
                    tool_logger.info(f'{sub}.{main_domain}')
                msg += '\n'

            msg += f'\n需手動更新 共{len(domain_dict.keys())}個\n'
            tool_logger.info(f'\n需手動更新 共{len(domain_dict.keys())}個\n')
            for main_domain in domain_dict.keys():
                msg += f'{main_domain}\n'
                tool_logger.info(main_domain)

        return (domain_dict.keys(), msg)
    return (domain_list, msg)


def get_all_files(dir_path: str, extensions: list = None, add_abspath: str = False):
    """取得所有檔案

    Args:
        dir_path (str): 檔案資料夾
        extensions (str, optional): 指定副檔名,若無指定則全部列出. Defaults to None.
        add_abspath (str, optional): 列出 絕對路徑. Defaults to False.

    Returns:
        _type_: _description_
    """
    target_file_path = []
    path = os.path.abspath(dir_path)

    for file in os.listdir(path):

        if add_abspath:
            target_path = f'{path}/{file}'
        else:
            target_path = f'{file}'

        _, file_extension = os.path.splitext(target_path)
        if extensions:
            allow_extension = [f'.{e}' for e in extensions]
            if file_extension in allow_extension:
                target_file_path.append(target_path)
        else:
            target_file_path.append(target_path)

        # 遞迴
        if os.path.isdir(f'{dir_path}/{file}'):
            files = get_all_files(f'{dir_path}/{file}',
                                  extensions, add_abspath)
            for file in files:
                target_file_path.append(file)
    target_file_path.sort()
    return target_file_path


def get_domain_from_nginx_config(conf_name: str):
    """根據 nginx 檔名 取得 domain

    格式 domain.conf

    Args:
        conf_name (str): _description_

    Returns:
        _type_: _description_
    """
    return os.path.splitext(conf_name)[0]


def generate_random_string(length: int = 12, punctuation: bool = True, digits: bool = True, lowercase: bool = True, uppercase: bool = True):
    """產生隨機亂數字串

    Args:
        length (int, optional): 長度. Defaults to 12.
        punctuation (bool, optional): 包含特殊符號. Defaults to True.
        digits (bool, optional): 包含數字. Defaults to True.
        lowercase (bool, optional): 包含字母大寫. Defaults to True.
        uppercase (bool, optional): 包含字母小寫. Defaults to True.

    Returns:
        _type_: _description_
    """
    if lowercase and uppercase:
        characters = string.ascii_letters
    elif lowercase:
        characters = string.ascii_lowercase
    elif uppercase:
        characters = string.ascii_uppercase
    else:
        characters = None

    if punctuation:
        characters += string.punctuation
    if digits:
        characters += string.digits

    password = ''.join(random.choice(characters) for i in range(length))
    return password

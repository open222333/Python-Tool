import re
import os
from .logger import Log
from . import LOG_LEVEL

tool_logger = Log('tool')
tool_logger.set_level(LOG_LEVEL)
tool_logger.set_msg_handler()


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
    punycode = idna.encode(domain).decode('utf-8')
    return punycode


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


def get_domain_list(path: str = None, show_msg=True, sld=True):
    """解析郵件訊息 取得 域名

    Args:
        path (_type_, optional): 需解析txt路徑. Defaults to None.
        show_msg (bool, optional): 顯示結果. Defaults to True.
        sld (bool, optional): 回傳二級域名. Defaults to True.

    Returns:
        _type_: _description_
    """
    domain_list = []
    sld_list = []
    cloud_list = []
    count = 0

    if not os.path.exists(path):
        tool_logger.error(f'{path} 不存在')

    with open(path, 'r') as f:
        content = f.read().splitlines()
    pattern = r'- name:'
    for i in content:
        if re.match(pattern, i):
            count += 1
            i = re.sub(pattern, ' ', i).replace(' ', '')
            sub_domain = re.findall(r'www\.(.*)', i)
            if sub_domain:
                if not sub_domain[0] in domain_list:
                    domain_list.append(i)
            else:
                domain_list.append(i)

    if show_msg:
        for d in domain_list:
            tool_logger.info(d)
        tool_logger.info(f'總筆數 共{count}個\n去除www後共{len(domain_list)}個\n')

    if sld:
        for i in domain_list:
            if len(i.split('.')) > 2:
                cloud_list.append(i)
                sub_domain = re.findall(r'\.(.*)', i)
                if not sub_domain[0] in sld_list:
                    sld_list.append(sub_domain[0])
            else:
                sld_list.append(i)
        if show_msg:
            for d in sld_list:
                tool_logger.info(d)
            tool_logger.info(f'二級域名 共{len(sld_list)}個\n')
            for d in cloud_list:
                tool_logger.info(d)
            tool_logger.info(f'需手動更新 共{len(cloud_list)}個\n')
        return sld_list
    return domain_list

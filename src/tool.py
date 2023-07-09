import re


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

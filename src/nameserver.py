import re
import shlex
import subprocess
from typing import Union


class NameServerTool():

    def __init__(self,  domain: str, nameservers: list = None) -> None:
        """檢查ns

        Args:
            nameservers (list): 指定比對用 nameservers 串列, Default to None.
            domain (str): 指定域名
        """
        self.nameservers = nameservers
        self.domain = domain

    def set_nameservers(self, nameservers: list):
        """指定比對用 nameservers

        Args:
            ns (list): 指定比對用ns
        """
        self.nameservers = nameservers

    def is_domain(self) -> bool:
        """是否為域名格式

        Returns:
            bool: _description_
        """
        if re.match(r'.*\..*', self.domain):
            return True
        else:
            return False

    def is_ns_match(self, nameservers: list = None) -> bool:
        """域名的ns是否匹配

        Returns:
            bool: _description_
        """
        if not nameservers:
            nameservers = self.nameservers

        result = self.get_ns()
        if result[0]:
            for ns in result[1]:
                if ns not in nameservers:
                    return False
            return True
        else:
            return False

    def get_ns(self) -> tuple[bool, Union[list, str]]:
        """取得域名 ns

        Returns:
            tuple[bool, Union[list, str]]: _description_
        """
        command = f'dig -t NS {self.domain} +short'
        # command='dig @ns1.netnames.net www.rac.co.uk +short'
        # command='dig @ns1.netnames.net www.rac.co.uk CNAME'
        proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
        out, err = proc.communicate()  # out, err
        if err:
            return (False, err.decode('utf-8'))
        else:
            r = []
            for i in out.decode('utf-8').split('\n'):
                if i != '':
                    r.append(i[:-1])
            return (True, r)

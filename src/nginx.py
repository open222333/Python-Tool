from .tool import is_chinese, domain_encode
from datetime import datetime
import logging
import re
import socket
import ssl


class Domains():

    sub_domains = []
    test_sub_domains = ['www']

    def __init__(self, domains: list, logger: logging):
        self.domains = []

        for domain in domains:
            domain = domain.strip()
            if is_chinese(domain):
                domain = domain_encode(domain)
            self.domains.append(domain)

        self.logger = logger

    def set_sub_domains(self, *sub_domains: str):
        self.sub_domains = sub_domains

    def add_sub_domains(self, *sub_domains: str):
        for sub_domain in sub_domains:
            self.sub_domains.append(sub_domain)

    def set_test_sub_domains(self, *sub_domains: str):
        self.test_sub_domains = sub_domains

    def add_test_sub_domains(self, *sub_domains: str):
        for sub_domain in sub_domains:
            self.test_sub_domains.append(sub_domain)

    def get_domains(self):
        return self.domains


class SSLNginxCommand(Domains):

    def __init__(self, domains: list, cli_ini: str, refer_domain: str, logger: logging):

        if is_chinese(refer_domain):
            refer_domain = domain_encode(refer_domain)
        self.refer_domain = refer_domain

        self.cli_ini = cli_ini
        super().__init__(domains, logger)

    def dig_check_command(self, dig_type: str = 'A') -> dict:
        """生成 產生 dig 檢查 record 類型指令串列

        Args:
            dig_type (str, optional): 指定 域名指向. Defaults to 'A'.

        Returns:
            dict: 指令串列
        """
        command_dict = {}
        self.logger.info(f'dig_check_command start')
        for domain in self.domains:
            command = f'dig +short {domain} {dig_type}'
            self.logger.debug(f'指令:\n{command}')
            command_dict[domain] = command
        return command_dict

    def create_ssl_command(self):
        """生成 產生新證書 certbot 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'create_ssl_command start')
        for domain in self.domains:
            if is_chinese(domain):
                domain = domain_encode(domain)
            if self.cli_ini:
                command = f"certbot -c {self.cli_ini} certonly --dns-cloudflare --no-autorenew -d {domain} -d *.{domain}"
            else:
                command = f"certbot certonly --dns-cloudflare --no-autorenew -d {domain} -d *.{domain}"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def create_check_ssl_command(self):
        """生成 檢查證書是否生成 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'create_ssl_command start')
        for domain in self.domains:
            if is_chinese(domain):
                domain = domain_encode(domain)
            command = f"ls archive/ | grep {domain}"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def renew_ssl_command(self):
        """生成 刷新證書 certbot 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'renew_ssl_command start')
        for domain in self.domains:
            if self.cli_ini:
                command = f"certbot -c {self.cli_ini} renew --dns-cloudflare --force-renew --no-autorenew --cert-name {domain}"
            else:
                command = f"certbot renew --dns-cloudflare --force-renew --no-autorenew --cert-name {domain}"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def create_link_sort_by_main(self):
        """根據子域名生成域名 依照主域名排序

        Returns:
            _type_: _description_
        """
        try:
            domain_list = []
            if len(self.sub_domains) == 0:
                raise RuntimeError('未設置 sub_domains')
            for sub_domain in self.sub_domains:
                for domain in self.domains:
                    domain_list.append(f'{sub_domain}.{domain}')
            return domain_list
        except Exception as err:
            self.logger.error(f'根據子域名生成域名 依照主域名排序 發生錯誤: {err}')

    def create_link_sort_by_sub(self):
        """根據子域名生成域名 依照子域名排序

        Returns:
            _type_: _description_
        """
        try:
            domain_list = []
            if len(self.sub_domains) == 0:
                raise RuntimeError('未設置 sub_domains')
            for domain in self.domains:
                for sub_domain in self.sub_domains:
                    domain_list.append(f'{sub_domain}.{domain}')
            return domain_list
        except Exception as err:
            self.logger.error(f'根據子域名生成域名 依照子域名排序 發生錯誤: {err}')

    def revoke_ssl_command(self):
        """生成 註銷證書 certbot 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'revoke_ssl_command start')
        for domain in self.domains:
            command = f'certbot revoke --cert-path /etc/letsencrypt/live/{domain}/cert.pem\ncertbot delete --cert-name {domain}'
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def cp_nginx_config_command(self, force=False):
        """生成 複製 nginx conf 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'cp_nginx_config_command start')
        for domain in self.domains:
            if force:
                command = f'yes | cp -f {self.refer_domain}.conf {domain}.conf\nsed -i s/{self.refer_domain}/{domain}/g {domain}.conf'
            else:
                command = f'cp {self.refer_domain}.conf {domain}.conf\nsed -i s/{self.refer_domain}/{domain}/g {domain}.conf'
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def remove_conf_command(self):
        """生成 刪除 nginx config 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'remove_conf_command start')
        for domain in self.domains:
            command = f"rm -f {domain}.conf"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def show_ssl_certificates_command(self):
        """生成 顯示證書資料夾指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'show_ssl_certificates_command start')
        for domain in self.domains:
            command = f"ls archive/ | grep {domain}"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def show_nginx_configs_command(self):
        """生成 查找 nginx config 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'show_nginx_configs_command start')
        for domain in self.domains:
            command = f"ls | grep {domain}.conf"
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def create_test_url(self):
        """生成 測試網址

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        for domain in self.domains:
            command_list.append(f'https://{domain}/')

        for test_sub_domain in self.sub_domains:
            for domain in self.domains:
                command_list.append(f'https://{test_sub_domain}.{domain}/')
        return command_list


class DownloadLink(SSLNginxCommand):

    def get_sub_domains(self):
        domains = []
        for domain in self.domains:
            for sub_domain in self.sub_domains:
                domains.append(f'{sub_domain}.{domain}')
        return domains

    def dig_check_command(self, dig_type: str = 'A') -> dict:
        command_dict = {}
        self.logger.info(f'dig_check_command start')
        for domain in self.domains:
            for sub_domain in self.sub_domains:
                command = f'dig +short {sub_domain}.{domain} {dig_type}'
                self.logger.debug(f'指令:\n{command}')
                command_dict[f'{sub_domain}.{domain}'] = command
        return command_dict

    def create_test_url(self):
        """生成 下載包測試網址

        Returns:
            list[str]: _description_
        """
        domain_list = []
        for domain in self.domains:
            for sub_domain in self.sub_domains:
                domain_list.append(f'https://{sub_domain}.{domain}/monitor.png')
        return domain_list


class WebLink(SSLNginxCommand):

    sub_domains = ['apit', 'cpit', 'rest', 'apiw', 'cpiw', 'resw']

    def is_api(self, sub_domain: str):
        pattern = re.compile(r'.*api.*')
        return bool(re.match(pattern, sub_domain))

    def is_cpi(self, sub_domain: str):
        pattern = re.compile(r'.*cpi.*')
        return bool(re.match(pattern, sub_domain))

    def is_res(self, sub_domain: str):
        pattern = re.compile(r'.*res.*')
        return bool(re.match(pattern, sub_domain))

    def create_test_url(self, web: str = None):
        """生成 測試網址

        Returns:
            list[str]: _description_
        """
        domain_list = []
        for domain in self.domains:
            for sub_domain in self.sub_domains:
                if self.is_api(sub_domain):
                    if web in ['jk', 'in'] or web == None:
                        domain_list.append(f'https://{sub_domain}.{domain}/s1/monitor')
                    if web in ['av9'] or web == None:
                        domain_list.append(f'https://{sub_domain}.{domain}/v3/monitor')
                    if web in ['988', 'duck', 'ptv'] or web == None:
                        domain_list.append(f'https://{sub_domain}.{domain}/json.php?api=version&platform=android&time=123456')
                if self.is_cpi(sub_domain):
                    domain_list.append(f'https://{sub_domain}.{domain}/API/')
                if self.is_res(sub_domain):
                    if web in ['jk', 'in', 'av9'] or web == None:
                        domain_list.append(f'https://{sub_domain}.{domain}/Asset/Landing/ad_landing_img.png')
        return domain_list


class SSLCertificate(Domains):

    def __init__(self, domains: list, logger: logging, port: int = 443):
        """_summary_

        Args:
            domains (list): _description_
            logger (logging): _description_
            port (int, optional): ssl 證書 port. Defaults to 443.
        """
        super().__init__(domains, logger)
        self.port = port

    def get_ssl_certificate_info(self, domain: str):
        """取得指定域名的 SSL 證書資訊

        Returns:
            _type_: _description_
        """
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(socket.socket(), server_hostname=domain) as ssock:
                ssock.connect((domain, self.port))
                cert = ssock.getpeercert()
            return cert
        except Exception as err:
            self.logger.error(f'{domain} {err}')

    def get_ssl_certificate_expiration_date(self) -> dict:
        """取得指定域名的 SSL 證書剩餘有效期的天數

        Returns:
            _type_: {域名:天數}
        """
        info = {}

        for domain in self.domains:
            cert = self.get_ssl_certificate_info(domain)
            not_after = cert['notAfter']
            expiration_date = datetime.strptime(not_after, '%b %d %H:%M:%S %Y %Z')
            days_until_expiry = (expiration_date - datetime.now()).days
            info[domain] = days_until_expiry
        return info

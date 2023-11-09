from .tool import is_chinese, domain_encode
import logging


class SSLNginxCommand():

    def __init__(self, domains: list, cli_ini: str, refer_domain: str, logger: logging):
        self.domains = []
        self.cli_ini = cli_ini

        if is_chinese(refer_domain):
            refer_domain = domain_encode(refer_domain)
        self.refer_domain = refer_domain

        for domain in domains:
            domain = domain.strip()
            if is_chinese(domain):
                domain = domain_encode(domain)
            self.domains.append(domain)

        self.logger = logger

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

    def create_ssl_command(self) -> list[str]:
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

    def create_check_ssl_command(self) -> list[str]:
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

    def renew_ssl_command(self) -> list[str]:
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

    def revoke_ssl_command(self) -> list[str]:
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

    def cp_nginx_config_command(self) -> list[str]:
        """生成 複製 nginx conf 指令串列

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'cp_nginx_config_command start')
        for domain in self.domains:
            command = f'cp {self.refer_domain}.conf {domain}.conf\nsed -i s/{self.refer_domain}/{domain}/g {domain}.conf'
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

    def remove_conf_command(self) -> list[str]:
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

    def show_ssl_certificates_command(self) -> list[str]:
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

    def show_nginx_configs_command(self) -> list[str]:
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

    def create_test_url(self) -> list[str]:
        """生成 測試網址

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        for domain in self.domains:
            command_list.append(f'https://{domain}/')

        for domain in self.domains:
            command_list.append(f'https://www.{domain}/')
        return command_list


class DownloadLink(SSLNginxCommand):

    second_domains = ['badl', 'ba9', 'bajk', 'bain', 'ba988']

    def set_second_domains(self, *second_domains):
        self.second_domains = second_domains

    def create_download_link_main(self):
        """生成 下載包域名 依照主域名排序

        Returns:
            _type_: _description_
        """
        domain_list = []
        for second_domain in self.second_domains:
            for domain in self.domains:
                domain_list.append(f'{second_domain}.{domain}')
        return domain_list

    def create_download_link_sub(self):
        """生成 下載包域名 依照子域名排序

        Returns:
            _type_: _description_
        """
        domain_list = []
        for domain in self.domains:
            for second_domain in self.second_domains:
                domain_list.append(f'{second_domain}.{domain}')
        return domain_list

    def create_test_url(self) -> list[str]:
        """生成 下載包測試網址

        Returns:
            list[str]: _description_
        """
        domain_list = []
        for domain in self.domains:
            for second_domain in self.second_domains:
                domain_list.append(f'https://{second_domain}.{domain}/monitor.png')
        return domain_list

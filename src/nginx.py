from .tool import is_chinese, domain_encode
import logging


class SSLNginxCommand():

    def __init__(self, domains: list, cli_ini: str, refer_domain: str, logger: logging):
        self.domains = []
        self.cli_ini = cli_ini
        self.refer_domain = refer_domain

        for domain in domains:
            if is_chinese(domain):
                domain = domain_encode(domain)
            self.domains.append(domain)
        self.logger = logger

    def dig_check_command(self, dig_type: str = 'A') -> list[str]:
        """生成 產生 dig 檢查 record 類型指令串列

        Args:
            dig_type (str, optional): 指定 域名指向. Defaults to 'A'.

        Returns:
            list[str]: 指令串列
        """
        command_list = []
        self.logger.info(f'dig_check_command start')
        for domain in self.domains:
            command = f'dig +short {domain} {dig_type}'
            self.logger.debug(f'指令:\n{command}')
            command_list.append(command)
        return command_list

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
            command = f"certbot -c {self.cli_ini} certonly --dns-cloudflare --no-autorenew -d {domain} -d *.{domain}"
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
            command = f"certbot -c {self.cli_ini} renew --dns-cloudflare --force-renew --no-autorenew --cert-name {domain}"
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
        return command_list

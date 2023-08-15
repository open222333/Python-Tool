from src import SSH_CONFIG_INFO


if __name__ == "__main__":
    config_str = ''
    for info in SSH_CONFIG_INFO:
        config_str += f"""
        Host {info['host']}
            User {info['user']}
            HostName {info['host_name']}
            Port {info['port']}
            ServerAliveInterval {info['server_alive_interval']}
            IdentityFile {info['identity_file']}\n
        """

    print(config_str)

from flask import Blueprint, jsonify, request
from flasgger import swag_from
from src.icp import ICP
from src.nginx import SSLNginxCommand
from src.tool import domain_encode, get_domain_list_from_email_str
from src.logger import Log
from src import LOG_LEVEL
import os

app_tools = Blueprint(
    name='tools',
    import_name=__name__
)

logger = Log('app_tools')
logger.set_level(LOG_LEVEL)
logger.set_msg_handler()


@app_tools.route('/check_icp/<domain>', methods=['GET', 'POST'])
@swag_from(os.path.join('doc', 'domain.yaml'))
def check_icp(domain):
    """檢查 icp備案

    Args:
        domain (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        icp = ICP()
        result = icp.get_icp_check_result(domain)
        if result:
            return jsonify({
                "success": True,
                "result": result
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": result
            }), 500
    except Exception as err:
        return jsonify({
            "success": False,
            "error": err
        }), 500


@app_tools.route('/domain_encode_punycode/<domain>', methods=['GET', 'POST'])
@swag_from(os.path.join('doc', 'domain.yaml'))
def domain_encode_punycode(domain):
    """中文域名轉換成 punycode

    Args:
        domain (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        encode_domain = domain_encode(domain)
        if encode_domain:
            return jsonify({
                "success": True,
                "result": encode_domain
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": encode_domain
            }), 500
    except Exception as err:
        return jsonify({
            "success": False,
            "error": err
        }), 500


@app_tools.route('/parse_email', methods=['GET', 'POST'])
@swag_from(os.path.join('doc', 'domain.yaml'))
def parse_email():
    """解析郵件內容
    """
    try:
        content = request.args.get(key='content')
        cli_ini = request.args.get(key='cli_ini', default='cli.ini')
        domain_list = get_domain_list_from_email_str(content)

        slc = SSLNginxCommand(
            domains=domain_list[0],
            cli_ini=cli_ini,
            refer_domain="",
            logger=logger
        )

        commands = {}
        commands['刷新證書 certbot 指令'] = slc.renew_ssl_command()

        if len(commands):
            return jsonify({
                "success": True,
                "result": commands
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": commands
            }), 500
    except Exception as err:
        return jsonify({
            "success": False,
            "error": err
        }), 500

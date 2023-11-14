from flask import Blueprint, jsonify, request
from flasgger import swag_from
from src.cloudflare import Record, DNSSEC, Zone
from src.logger import Log
from src import LOG_LEVEL
from pprint import pformat
import os


logger = Log('app_cloudflare')
logger.set_level(LOG_LEVEL)
logger.set_msg_handler()


app_cloudflare = Blueprint(
    name='cloudflare',
    import_name=__name__
)


@app_cloudflare.route('/cloudflare/<domain>', methods=['GET'])
# @swag_from(os.path.join('doc', 'cloudflare.yaml'))
def check(domain, info):
    try:
        api_key = request.args.get('api_key')
        api_token = request.args.get('api_token')
        email = request.args.get('email')

        zone_instance = Zone(
            api_key=api_key,
            api_token=api_token,
            email=email
        )

        zone_response = zone_instance.create_zone(domain)
        if zone_response:
            if zone_response['success']:
                logger.info(f'{domain} 域名已成功添加到 Cloudflare')

                # 創建的域名的 Zone ID
                zone_id = zone_response['result']['id']

                record_instance = Record(
                    api_key=api_key,
                    api_token=api_token,
                    email=email
                )

                # 添加 record
                for record in info['records']:
                    record_response = record_instance.create_dns_record(
                        zone_id=zone_id,
                        record_type=record['type'],
                        record_name=record['name'],
                        record_content=record['content']
                    )

                    if record_response:
                        if record_response['success']:
                            logger.info(f'DNS 指向紀錄已成功添加:\n{pformat(record)}')
                        else:
                            raise RuntimeError(f'DNS 指向紀錄添加失敗:\n{pformat(record)}')
                    else:
                        raise RuntimeError(f'DNS 指向紀錄添加失敗:\n{pformat(record)}')

            if info.get('active_dnssec', False):
                dnssec_instance = DNSSEC(
                    api_key=info['api_key'],
                    api_token=info['api_token'],
                    email=info['email']
                )

                dnssec_response = dnssec_instance.active_dnssec(zone_id)
                if dnssec_response:
                    if dnssec_response['success']:
                        logger.info(f'{domain} DNSSEC 已成功啟用:\n{pformat(dnssec_response["result"])}')
                    else:
                        raise RuntimeError(f'{domain} DNSSEC 啟用失敗 {dnssec_response}')
                else:
                    raise RuntimeError(f'{domain} DNSSEC 啟用失敗 {dnssec_response}')
            else:
                raise RuntimeError(f'{domain} 域名添加失敗')
        else:
            raise RuntimeError(f'{domain} 域名添加失敗')

        return jsonify({
            "success": True,
            "result": dnssec_response
        }), 200
    except Exception as err:
        logger.error(err, exc_info=True)
        return jsonify({
            "success": False,
            "error": err
        }), 500

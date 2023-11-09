from src import LOG_LEVEL, LOG_FILE_DISABLE
from src.logger import Log
from typing import Union
import requests
import json


logger = Log('CLOUDFLARE')
logger.set_level(LOG_LEVEL)
if LOG_FILE_DISABLE:
    logger.set_date_handler()
logger.set_msg_handler()


class CloudFlare():

    def __init__(self, api_key: str, api_token: str, email: str) -> None:
        """初始化cloudflare基本資訊

        Args:
            api_key (str): Cloudflare API 密鑰
            api_token (str): Cloudflare API 令牌
            email (str): Cloudflare 電子郵件
        """
        self.api_key = api_key
        self.api_token = api_token
        self.email = email


class Zone(CloudFlare):

    def __init__(self, api_key: str, api_token: str, email: str) -> None:
        super().__init__(api_key, api_token, email)

    def get_zones(self) -> Union[str, None]:
        """取得所有zones
        [List Zones](https://developers.cloudflare.com/api/operations/zones-get)

        Cloudflare Zone 是指在 Cloudflare 上託管的一個或多個網域，包含了網域的 DNS 設定、安全設定、緩存設定、分發設定等等。

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # 定義 API 請求的 URL
        url = f'https://api.cloudflare.com/client/v4/zones'

        # 定義 API 請求的 headers
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 執行 API 請求
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'取得所有zone 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'取得所有zone 發生錯誤: {response.status_code}\n{response}')
            return None

    def get_zone_id(self, zone_name: str) -> Union[str, None]:
        """根據域名取得zone id

        Args:
            zone_name (str): 域名

        Returns:
            Union[str, None]: 回傳 zone id
        """
        zones = self.get_zones()['result']
        zone_id = None
        for zone in zones:
            if zone['name'] == zone_name:
                zone_id = zone['id']
                break
        if zone_id:
            return zone_id
        else:
            logger.error('根據域名取得zone id 發生錯誤')
            return None

    def get_info_by_zone_id(self, zone_id: str) -> Union[str, None]:
        """根據zone id 取得域名資訊

        Args:
            zone_id (str): 域名 zone id

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # 定義 API 請求的 URL
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}'

        # 定義 API 請求的 headers
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 執行 API 請求
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'根據zone_id取得域名資訊 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'根據zone_id取得域名資訊 發生錯誤: {response.status_code}\n{response}')
            return None

    def create_zone(self, zone_name: str) -> Union[str, None]:
        """新增網域

        [Create Zone](https://developers.cloudflare.com/api/operations/zones-post)

        Args:
            zone_name (str): 域名

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # API 請求的 URL
        url = 'https://api.cloudflare.com/client/v4/zones'

        # 設定請求的標頭
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 設定請求的主體
        data = {
            'name': zone_name
        }

        # 傳送 POST 請求來新增指向紀錄
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'新增網域 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'新增網域 發生錯誤: {response.status_code}\n{response.json()}')
            return None

    def delete_zone(self, zone_id: str) -> Union[str, None]:
        """刪除網域

        [Delete Zone](https://developers.cloudflare.com/api/operations/zones-0-delete)

        Args:
            zone_id (str): 域名 zone id

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # API 請求的 URL
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}'

        # 設定請求的標頭
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 發送 DELETE 請求
        response = requests.delete(url, headers=headers)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'刪除網域 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'刪除網域 發生錯誤: {response.status_code}\n{response.json()}')
            return None


class Record(CloudFlare):

    def __init__(self, api_key: str, api_token: str, email: str) -> None:
        """指向紀錄

        Args:
            api_key (str): _description_
            api_token (str): _description_
            email (str): _description_
        """
        super().__init__(api_key, api_token, email)

    def get_dns_records(self, zone_id: str) -> Union[str, None]:
        """根據zone_id取得所有指向紀錄

        [List DNS Records](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-list-dns-records)

        Args:
            zone_id (str): zone_id 是指你要管理的網域的唯一識別碼。

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # 定義 API 請求的 URL
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

        # 定義 API 請求的 headers
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 發送 API 請求並取得回應
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'根據zone_id取得所有指向紀錄 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'根據zone_id取得所有指向紀錄 發生錯誤: {response.status_code}\n{response.json()}')
            return None

    def create_dns_record(self, zone_id: str, record_type: str, record_name: str, record_content: str, record_ttl: int = 120, proxied: bool = False) -> Union[str, None]:
        """新增dns指向紀錄
        [Create DNS Record](https://developers.cloudflare.com/api/operations/dns-records-for-a-zone-create-dns-record)

        Args:
            zone_id (str): 域名ID
            record_type (str): 指向類型, ex:'A'
            record_name (str): 指向名稱, ex:'example.com'
            record_content (str): 指向內容, ex:'192.0.2.1'
            record_ttl (int, optional): TTL. Defaults to 120.
            proxied (_type_, optional): 指向是否啟用代理。. Defaults to False.

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # 設定 Cloudflare API 的網址
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'

        # 設定 HTTP headers
        headers = {
            'Content-Type': 'application/json',
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Authorization': f'Bearer {self.api_token}'
        }

        # 設定要新增指向紀錄的資料
        data = {
            'type': record_type,
            'name': record_name,
            'content': record_content,
            'ttl': record_ttl,
            'proxied': proxied
        }

        # 傳送 POST 請求來新增指向紀錄
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'新增dns指向紀錄 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'新增dns指向紀錄 發生錯誤: {response.status_code}\n{response.json()}')
            return None


class DNSSEC(CloudFlare):

    def __init__(self, api_key: str, api_token: str, email: str) -> None:
        """

        Args:
            api_key (str): _description_
            api_token (str): _description_
            email (str): _description_
        """
        super().__init__(api_key, api_token, email)

    def get_dnssec_details(self, zone_id: str) -> Union[str, None]:
        """根據 zone_id 取得 dnssec 細節

        [DNSSEC Details](https://developers.cloudflare.com/api/operations/dnssec-dnssec-details)

        Args:
            zone_id (str): 域名ID

        Returns:
            Union[str, None]: cloudflare json格式
        """
        # 設置 API 網址
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec'

        # 設置 API headers
        headers = {
            'X-Auth-Email': self.email,
            'X-Auth-Key': self.api_key,
            'Content-Type': 'application/json'
        }

        # 發送 API 請求
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'根據 zone_id 取得 dnssec 細節 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'根據 zone_id 取得 dnssec 細節 發生錯誤: {response.status_code}\n{response.json()}')
            return None

    def active_dnssec(self, zone_id: str) -> Union[str, None]:
        """啟用DNSSEC

        [Edit DNSSEC Status](https://developers.cloudflare.com/api/operations/dnssec-edit-dnssec-status)

        Args:
            zone_id (str): _description_

        Returns:
            Union[str, None]: cloudflare json格式
        """

        # 設置 API 相關資訊
        # url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec/{dnssec_id}/edit'
        url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dnssec'

        # 設置請求標頭
        headers = {
            'Authorization': f'Bearer {self.api_token}',
            'Content-Type': 'application/json'
        }

        # 設置請求資料
        data = {
            'status': 'active'  # 修改為 active 啟用 DNSSEC
        }

        # 發送請求
        response = requests.patch(url, headers=headers, json=data)
        if response.status_code == 200:
            json_response = json.loads(response.text)
            if not json_response['success']:
                logger.error(f'啟用DNSSEC 發生錯誤:\n{json_response}')
            return json_response
        else:
            logger.error(f'啟用DNSSEC 發生錯誤: {response.status_code}\n{response.json()}')
            return None

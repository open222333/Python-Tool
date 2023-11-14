import os
import cv2
import time
import base64
import hashlib
import requests
from typing import Union
from .logger import Log
from . import LOG_LEVEL, LOG_FILE_DISABLE
from fake_useragent import UserAgent

logger = Log('ICP')
logger.set_level(LOG_LEVEL)
if not LOG_FILE_DISABLE:
    logger.set_file_handler()
logger.set_msg_handler()


class ICP():

    ua = UserAgent()

    def __init__(self) -> None:
        pass

    def get_cookies(self):
        """取得 cookies

        Returns:
            _type_: _description_
        """
        headers = {
            'User-Agent': self.ua.random
        }
        url = 'https://beian.miit.gov.cn/'
        err_num = 0
        while err_num < 3:
            try:
                cookie = requests.utils.dict_from_cookiejar(
                    requests.get(url, headers=headers).cookies)['__jsluid_s']
                return cookie
            except:
                err_num += 1
                time.sleep(3)
        return None

    def get_token(self):
        """使用md5加密字符串"testtest"+timeStamp(當前時間戳)，獲取authKey

        Returns:
            _type_: _description_
        """
        timeStamp = round(time.time()*1000)
        authSecret = 'testtest' + str(timeStamp)
        authKey = hashlib.md5(authSecret.encode(encoding='UTF-8')).hexdigest()
        auth_data = {'authKey': authKey, 'timeStamp': timeStamp}
        url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/auth'
        try:
            t_response = requests.post(url=url, data=auth_data, headers=self.base_header).json()
            token = t_response['params']['bussiness']
        except Exception as err:
            logger.error(f'{err}: {str(t_response)}', exc_info=True)
            return None
        return token

    def get_check_pic(self, token):
        """取得驗證圖片 並根據圖片取得 uuid, value

        Args:
            token (_type_): _description_

        Returns:
            _type_: _description_
        """
        url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/getCheckImage'
        self.base_header['Accept'] = 'application/json, text/plain, */*'
        self.base_header.update({'Content-Length': '0', 'token': token})
        try:
            p_request = requests.post(url=url, data='', headers=self.base_header).json()
            uuid = p_request['params']['uuid']
            big_image = p_request['params']['bigImage']
            small_image = p_request['params']['smallImage']
        except:
            return None
        with open('bigImage.jpg', 'wb') as f:
            f.write(base64.b64decode(big_image))
        with open('smallImage.jpg', 'wb') as f:
            f.write(base64.b64decode(small_image))
        background_image = cv2.imread('bigImage.jpg', cv2.COLOR_GRAY2RGB)
        fill_image = cv2.imread('smallImage.jpg', cv2.COLOR_GRAY2RGB)
        position_match = cv2.matchTemplate(background_image, fill_image, cv2.TM_CCOEFF_NORMED)
        max_loc = cv2.minMaxLoc(position_match)[3][0]
        mouse_length = max_loc + 1
        os.remove('bigImage.jpg')
        os.remove('smallImage.jpg')
        return {'key': uuid, 'value': mouse_length}

    def get_sign(self, payload, token):
        """取得 sigh

        Args:
            payload (_type_): _description_
            token (_type_): _description_

        Returns:
            _type_: _description_
        """
        check_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/image/checkImage'
        self.base_header.update({'Content-Length': '60', 'token': token, 'Content-Type': 'application/json'})
        try:
            pic_sign = requests.post(check_url, json=payload, headers=self.base_header).json()
            sign = pic_sign['params']
        except:
            return None
        return sign

    def get_beian_info(self, payload, uuid, token, sign):
        """取得備案資訊

        Args:
            payload (_type_): payload內容
            uuid (_type_): _description_
            token (_type_): _description_
            sign (_type_): _description_

        Returns:
            Union[None, dict]: _description_
        """
        info_url = 'https://hlwicpfwc.miit.gov.cn/icpproject_query/api/icpAbbreviateInfo/queryByCondition'
        self.base_header.update({'Content-Length': '78', 'uuid': uuid, 'token': token, 'sign': sign})
        try:
            beian_info = requests.post(url=info_url, json=payload, headers=self.base_header)
            logger.debug(beian_info)
            return beian_info
        except:
            return None

    def get_icp_check_result(self, domain_name: str):
        cookie = self.get_cookies()
        payload = {'pageNum': '', 'pageSize': '', 'serviceType': 1, 'unitName': domain_name}
        try:
            self.base_header = {
                'User-Agent': self.ua.random,
                'Origin': 'https://beian.miit.gov.cn',
                'Referer': 'https://beian.miit.gov.cn/',
                'Cookie': f'__jsluid_s={cookie}'
            }
            if cookie:
                token = self.get_token()
                logger.debug(token)
                if token:
                    check_data = self.get_check_pic(token)
                    logger.debug(check_data)
                    if check_data:
                        sign = self.get_sign(check_data, token)
                        uuid = check_data['key']
                        if sign != -1:
                            beian_result = self.get_beian_info(payload=payload, uuid=uuid, token=token, sign=sign)
                            if beian_result:
                                if beian_result.status_code == 200:
                                    domain_list = beian_result.json()['params']['list']
                                    if len(domain_list) > 0:
                                        return {
                                            'message': '有備案',
                                            'data': domain_list,
                                            'hasICPRecord': True
                                        }
                                    else:
                                        return {
                                            'message': '無備案',
                                            'data': domain_list,
                                            'hasICPRecord': False
                                        }
                                else:
                                    return {
                                        'message': '取得備案資訊請求異常',
                                        'data': beian_result.json(),
                                        'hasICPRecord': None
                                    }
                            else:
                                raise ValueError("取得備案資訊失敗")
                        else:
                            raise ValueError("取得sign錯誤")
                    else:
                        raise ValueError("計算圖片缺口位置錯誤")
                else:
                    raise ValueError("讀取token失敗")
            else:
                raise ValueError("取得cookie失敗")
        except Exception as e:
            logger.error(e, exc_info=True)
            return {'message': e, 'hasICPRecord': None}

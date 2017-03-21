# __Author__:oliver
# __DATE__:3/8/17
from config import settings
from src import plugin
from lib.serialize import Json
from lib.log import Logger
import os
import json
import hashlib
import time
import requests


class Base(object):
    def __init__(self):
        self.asset_api = settings.ASSET_API
        self.token = settings.token
        self.key_name = settings.AUTH_KEY_NAME

    def auth_key(self):
        """接口认证"""
        obj = hashlib.md5()
        time_stamp = time.time()
        md5_str = '%f\n%s' % (time_stamp, self.token)
        obj.update(bytes(md5_str, encoding='utf-8'))

        return {self.key_name: '%s&%f' % (obj.hexdigest()[5:15], time_stamp)}

    def post_asset(self, data, callback=None):
        """
        以POST方式向服务端指定的接口提供资产信息
        :param data:
        :param callback:
        :return:
        """
        status = True
        try:

            response = requests.post(
                url=self.asset_api,
                # headers=self.auth_key(),
                params=self.auth_key(),
                json=data
            )
        except Exception as e:
            response = '%s: %s' % ('post_asset', e)
            status = False
        if callback:
            callback(status, response)

    def process(self):
        """
        处理请求的入口
        :return:
        """
        raise NotImplementedError("You must implement 'process' method!")

    def callback(self, status, response):
        """
        将返回结果写入日志
        :param status:
        :param response:
        :return:
        """
        if not status:
            Logger().log(str(response), False)
            return
        ret = json.loads(response.text)
        if ret['code'] == 1000:
            Logger().log(ret['message'], True)
        else:
            Logger().log(ret['message'], False)


class AutoAgent(Base):
    def __init__(self):
        self.path = settings.CERT_FILE_PATH
        super(AutoAgent, self).__init__()

    def load_local_cert(self):
        """获取本地唯一标识 → hostname"""
        if not os.path.exists(self.path):
            return None
        with open(self.path, 'r') as f:
            data = f.read()
        if not data:
            return None
        cert = data.strip()
        return cert

    def write_local_cert(self, cert):
        """
        将cert写入文件
        :param cert: 即hostname，本地唯一标识
        :return:
        """
        with open(self.path, mode='w') as f:
            f.write(cert)

    def process(self):
        """
        获取资产信息
        :return:
        """
        server_info = plugin.get_server_info()
        # print(server_info.status, server_info.data)
        if not server_info.status:
            return
        local_cert = self.load_local_cert()
        if local_cert:
            if local_cert != server_info.data['hostname']:
                # 如果文件中保存的cert标识与系统hostname不同，则已文件为准
                server_info.data['hostname'] = local_cert
        else:
            self.write_local_cert(server_info.data['hostname'])
        data_to_json = Json.dumps(server_info.data)
        print(data_to_json)
        self.post_asset(data_to_json, self.callback)


class NoAgent(Base):
    def get_asset(self):
        """获取未采集的资产"""
        pass


class AutoSSH(NoAgent):
    def process(self):
        pass


class AutoSalt(NoAgent):
    def process(self):
        pass


if __name__ == '__main__':
    ret = Base().auth_key()
    print(ret)

#__Author__:oliver
#__DATE__:3/9/17
from src.plugin.base import BasePlugin
from lib.response import BaseResponse
import traceback
import os

class MainBoard_Plugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_model:
                from config.settings import BASE_DIR
                ret = open(os.path.join(BASE_DIR,'file/board.out'),'r').read()
            else:
                ret = self.exec_shell_cmd('sudo dmidecode -t1')

            response.data = self.parse(ret)
        except Exception as e:
            response.status = False
            msg = "%s MainBoard_Plugin Error: %s" % (self.hostname, traceback.format_exc())
            response.error = msg
            self.logger.log(msg, False)
        return response

    @staticmethod
    def parse(data):
        result = {}
        key_map = {
            'Manufacturer': 'manufacturer',
            'Product Name': 'model',
            'Serial Number': 'sn',
        }

        for item in data.split('\n'):
            row_data = item.strip().split(':')
            if len(row_data) == 2:
                if row_data[0] in key_map:
                    result[key_map[row_data[0]]] = row_data[1].strip() if row_data[1] else row_data[1]
        # print(result)
        return result


if __name__ == '__main__':
    MainBoard_Plugin().linux()
#__Author__:oliver
#__DATE__:3/9/17
from src.plugin.base import BasePlugin
from lib.response import BaseResponse
import os
import traceback
from lib import convert


class Memory_Plugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_model:
                from config.settings import BASE_DIR
                ret = open(os.path.join(BASE_DIR, 'file/memory.out'), 'r').read()
            else:
                ret = self.exec_shell_cmd('sudo dmidecode  -q -t 17 2>/dev/null')
            response.data = self.parse(ret)
        except Exception as e:
            response.status = False
            msg = "%s Memory_Plugin Error: %s" % (self.hostname, traceback.format_exc())
            response.error = msg
            self.logger.log(msg, False)
        return response


    @staticmethod
    def parse(data):
        ram_dict = {}
        key_map = {
            'Size': 'capacity',
            'Locator': 'slot',
            'Type': 'model',
            'Speed': 'speed',
            'Manufacturer': 'manufacturer',
            'Serial Number': 'sn',

        }
        devices = data.split('Memory Device')
        for item in devices:
            item = item.strip()
            if not item:
                continue
            if item.startswith('#'):
                continue
            segment = {}
            lines = item.split('\n\t')
            for line in lines:
                if len(line.split(':')) > 1:
                    key, value = line.split(':')
                else:
                    key = line.split(':')[0]
                    value = ""
                if key in key_map:
                    if key == 'Size':
                        segment[key_map['Size']] = convert.convert_mb_to_gb(value, 0)
                    else:
                        segment[key_map[key.strip()]] = value.strip()
            ram_dict[segment['slot']] = segment
        # print(ram_dict)
        return ram_dict


if __name__ == '__main__':
    Memory_Plugin().linux()
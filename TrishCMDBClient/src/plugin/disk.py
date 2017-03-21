# __Author__:oliver
# __DATE__:3/9/17
from src.plugin.base import BasePlugin
from lib.response import BaseResponse
import os
import re
import traceback


class Disk_Plugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_model:
                from config.settings import BASE_DIR
                ret = open(os.path.join(BASE_DIR, 'file/disk.out'), 'r').read()
            else:
                ret = self.exec_shell_cmd('cat /proc/dd')
            response.data = self.parse(ret)
        except Exception as e:
            response.status = False
            msg = "%s Disk_Plugin Error: %s" % (self.hostname, traceback.format_exc())
            response.error = msg
            self.logger.log(msg, False)
        # print(response.data)
        return response

    def parse(self, data):
        response = {}
        result = []
        for row_line in data.split("\n\n\n\n"):
            result.append(row_line)
        for item in result:
            temp_dict = {}
            for row in item.split('\n'):
                if not row.strip():
                    continue
                if len(row.split(':')) != 2:
                    continue
                key, value = row.split(':')
                name = self.mega_patter_match(key)
                if name:
                    if key == 'Raw Size':
                        raw_size = re.search('(\d+\.\d+)', value.strip())
                        if raw_size:

                            temp_dict[name] = raw_size.group()
                        else:
                            raw_size = '0'
                    else:
                        temp_dict[name] = value.strip()
            if temp_dict:
                response[temp_dict['slot']] = temp_dict
        return response

    @staticmethod
    def mega_patter_match(needle):
        grep_pattern = {'Slot': 'slot', 'Raw Size': 'capacity', 'Inquiry': 'model', 'PD Type': 'pd_type'}
        for key, value in grep_pattern.items():
            if needle.startswith(key):
                return value
        return False



if __name__ == '__main__':
    Disk_Plugin().linux()
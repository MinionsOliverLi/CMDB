# __Author__:oliver
# __DATE__:3/9/17
from src.plugin.base import BasePlugin
from lib.response import BaseResponse
import traceback
import os


class CPU_Plugin(BasePlugin):
    def linux(self):
        response = BaseResponse()
        try:
            if self.test_model:
                from config.settings import BASE_DIR
                ret = open(os.path.join(BASE_DIR, 'file/cpuinfo.out'), 'r').read()
            else:
                ret = self.exec_shell_cmd('cat /proc/cpuinfo')
            response.data = self.parse(ret)
        except Exception as e:
            response.status = False
            msg = "%s CPU_Plugin Error: %s" % (self.hostname, traceback.format_exc())
            response.error = msg
            self.logger.log(msg, False)
        return response

    @staticmethod
    def parse(data):
        """从数据中解析CPU关键信息"""
        cpu_info = {
            'cpu_model': None,
            'cpu_count': 0,
            'cpu_core_count': 0,
        }
        cpu_physical_set = set()
        for item in data.strip().split('\n\n'):
            for row in item.split('\n'):
                key, val = row.split(':')
                key = key.strip()
                if key == 'model name':
                    if not cpu_info['cpu_model']:
                        cpu_info['cpu_model'] = val
                elif key == 'physical id':
                    cpu_physical_set.add(val)
                elif key == 'processor':
                    cpu_info['cpu_core_count'] += 1
        cpu_info['cpu_count'] = len(cpu_physical_set)
        # print(cpu_info)
        return cpu_info


if __name__ == '__main__':
    CPU_Plugin().linux()

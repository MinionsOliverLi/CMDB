#__Author__:oliver
#__DATE__:3/9/17
from src.plugin.base import BasePlugin
from lib.response import BaseResponse
import traceback

class BasicPlugin(BasePlugin):
    def os_platform(self):
        """获取系统平台"""
        if self.test_model:
            platform = 'Linux'
        else:
            platform = self.exec_shell_cmd('uname')

        return platform.strip()


    def os_version(self):
        """获取系统版本"""
        if self.test_model:
            version = 'Ubuntu 16.04.1 LTS \n \l'
        else:
            version = self.exec_shell_cmd('cat /etc/issue')
        version = version.strip().split('\n')[0]
        return version

    def os_hostname(self):
        """获取主机名"""
        if self.test_model:
            hostname = 'C190-A'
        else:
            hostname = self.exec_shell_cmd('hostname')

        return hostname.strip()

    def linux(self):
        response = BaseResponse()
        try:
            ret = {
                'os_platform':self.os_platform(),
                'os_version':self.os_version(),
                'hostname':self.os_hostname(),
            }
            response.data = ret
        except Exception as e:
            response.status = False
            msg = "%s BasicPlugin Error: %s"%(self.hostname,traceback.format_exc())
            response.error = msg
            self.logger.log(msg,False)

        return response
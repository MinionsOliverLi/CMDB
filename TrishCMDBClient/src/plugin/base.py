# __Author__:oliver
# __DATE__:3/9/17
from lib.log import Logger
from config import settings


class BasePlugin(object):
    def __init__(self, hostname=None):
        self.logger = Logger()
        self.test_model = settings.TEST_MODEL
        self.model_list = ['agent', 'ssh', 'salt']
        if hasattr(settings, 'COLLECT_MODEL'):
            self.collect_model = settings.COLLECT_MODEL
        else:
            self.collect_model = 'agent'
        self.hostname = hostname

    def agent(self, cmd):
        import subprocess

        return subprocess.getoutput(cmd)

    def ssh(self):
        pass

    def salt(self):
        pass

    def exec_shell_cmd(self,cmd):
        if self.collect_model not in self.model_list:
            raise Exception("settings.mode must be one of ['agent', 'salt', 'ssh']")
        ret = getattr(self,self.collect_model)(cmd)

        return ret

    def execute(self):

        return self.linux()

    def linux(self):
        raise Exception("You must implement linux method.")

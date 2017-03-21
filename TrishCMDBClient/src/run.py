#__Author__:oliver
#__DATE__:3/8/17
from src import clients
from config import settings

def client():
    if settings.COLLECT_MODEL == 'agent':
        clt = clients.AutoAgent()
    elif settings.COLLECT_MODEL == 'ssh':
        clt = clients.AutoSSH()
    elif settings.COLLECT_MODEL == 'salt':
        clt = clients.AutoSalt()
    else:
        raise Exception('请配置资产采集模式')

    clt.process()

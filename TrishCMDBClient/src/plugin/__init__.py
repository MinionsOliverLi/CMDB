# __Author__:oliver
# __DATE__:3/8/17
from src.plugin.basic import BasicPlugin
from config import settings
import importlib


def get_server_info(hostname=None):
    """
    获取服务器基本信息
    :param hostname: AGENT模式时,hostname为空,可直接从本地获取;其它模式时,表示远程连接的主机.
    :return:
    """
    response = BasicPlugin(hostname).execute()
    if not response.status:
        return response
    for k, v in settings.PLUGINS_DICT.items():
        module_path, cls_name = v.rsplit('.', 1)
        module_name = importlib.import_module(module_path)
        cls = getattr(module_name, cls_name)
        ret = cls(hostname).execute()
        response.data[k] = ret
    return response


if __name__ == '__main__':
    for k, v in settings.PLUGINS_DICT.items():
        # src.plugins.cpu.CPU_Plugin
        module_path, cls_name = v.rsplit('.', 1)
        print(module_path, cls_name)

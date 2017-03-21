# __Author__:oliver
# __DATE__:3/8/17
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 资产采集模式,包括：agen,ssh,salt,默认为agent.
COLLECT_MODEL = 'agent'

# 资产信息API uri
"""
POST返回信息
{"code": 1001, "message": "API authorization failed"}
code:  1000 表示提交成功，1001 表示接口授权失败
"""
ASSET_API = 'http://127.0.0.1:8000/api/asset/'

# 用于API认证的token
token = '123495ft-23d0-21eb-b06a-a45e60bec08b'

# 用于API认证的请求头
AUTH_KEY_NAME = 'auth_key'

# 当采集模式为AGENT时,此路径保存主机全局唯一标识信息
CERT_FILE_PATH = os.path.join(BASE_DIR, 'config', 'cert')

# 测试模式,测试模式下数据从file目录下的文件中读取
TEST_MODEL = True

# 硬件数据采集的插件
PLUGINS_DICT = {
    'cpu': 'src.plugin.cpu.CPU_Plugin',
    'disk': 'src.plugin.disk.Disk_Plugin',
    'main_board': 'src.plugin.main_board.MainBoard_Plugin',
    'memory': 'src.plugin.memory.Memory_Plugin',
    'nic': 'src.plugin.nic.NIC_Plugin',
}

# 日志文件路径
LOG_FILE_PATH = {
    'run_log': os.path.join(BASE_DIR, 'log', 'run.log'),
    'error_log': os.path.join(BASE_DIR, 'log', 'error.log')
}

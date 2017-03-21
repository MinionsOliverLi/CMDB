# __Author__:oliver
# __DATE__:3/11/17
from django.http import JsonResponse
from TrishCMDB import settings
import time
import hashlib


def api_auth(func):
    def inner(request, *args, **kwargs):
        if not auth_method(request):
            return JsonResponse(
                {'code': 1001, 'message': 'API authorization failed'},
                json_dumps_params={'ensure_ascii': False})
        return func(request, *args, **kwargs)

    return inner


visited = []
def auth_method(request):
    auth_key = request.GET.get('auth_key')
    # print(auth_key)
    if not auth_key:
        return False

    ret = auth_key.split('&')
    if len(ret) != 2:
        return False

    encrypt, timestamp = ret
    timestamp = float(timestamp)
    # print(encrypt,timestamp)
    limit_timestamp = time.time() - timestamp
    if limit_timestamp > settings.ASSET_AUTH_TIME:  # 请求超时
        return False

    obj = hashlib.md5()
    md5_str = '%f\n%s' % (timestamp, settings.token)
    obj.update(bytes(md5_str, encoding='utf-8'))
    result = obj.hexdigest()[5:15]
    if result != encrypt:
        return False

    for item in visited:        # 可以放到缓存中或memcach中，并设置超时时间。
        if encrypt == item.get('encrypt'):
            return False

    visited.append({'encrypt': encrypt, 'time': timestamp})
    return True
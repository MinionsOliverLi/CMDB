#__Author__:oliver
#__DATE__:3/9/17

class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.message = None
        self.error = None
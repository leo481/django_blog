import time

VISIT_RECORD = {}
#自定义速率限制
class MyThrottle():
    def __init__(self):
        self.history = None

    def allow_request(self, request, view):
        """
        60秒内只能访问三次
        """
        ip = request.META.get("REMOTE_ADDR")
        timestamp = time.time()
        if ip not in VISIT_RECORD:
            VISIT_RECORD[ip] = [timestamp,]
            return True
        history = VISIT_RECORD[ip]
        self.history = history
        history.insert(0, timestamp)
        while history and history[-1] < timestamp - 60:
            history.pop()
        if len(history) > 3:
            return False
        else:
            return True

    def wait(self):
        """
        限制时间还剩多少
        """
        timestamp = time.time()
        return 60 - (timestamp - self.history[-1])
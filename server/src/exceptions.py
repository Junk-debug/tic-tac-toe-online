class HTTPExceptionEx(Exception):
    def __init__(self, status_code: int, result: str, result_msg=None, headers=None):
        self.status_code = status_code
        self.result = result
        self.result_msg = result_msg
        self.headers = headers


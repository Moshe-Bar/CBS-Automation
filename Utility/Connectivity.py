import urllib3


class Connectivity:
    @classmethod
    def is_connect(cls):
        http = urllib3.PoolManager(timeout=3.0)
        try:
            r = http.request('GET', 'https://www.google.com/', preload_content=False)
        except Exception as err:
            print(f'No connection {err}')
            return False
        code = r.status
        r.release_conn()
        if code == 200:
            return True
        else:
            return False
import requests
PROXY_POOL_URL = 'http://127.0.0.1:5555/random'

def get_proxy():
    try:
        res = requests.get(PROXY_POOL_URL)
        if res.status_code == 200:
            print(res.text)
            return res.text
    except ConnectionError:
        return None

if __name__ == '__main__':
    proxy = get_proxy()
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy
    }
    try:
        res = requests.get('http://www.baidu.com',proxies = proxies)
        print(res.text)
    except requests.exceptions.ConnectionError as e:
        print('Error',e.args)
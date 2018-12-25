import requests


def fetch_json(url):
    try:
        data = requests.get(url)
        return data.json()
    except Exception as e:
        print('Something wrong... ', e)
        return None

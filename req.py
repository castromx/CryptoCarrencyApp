import json
import requests


def fetch_data_coins():
    all_coins = requests.get('https://api.coingecko.com/api/v3/coins/list')

    if all_coins.status_code == 200:
        data_list = json.loads(all_coins.text)
        return data_list
    else:
        # print("Failed to fetch data. Status code:", all_coins.status_code)
        return []

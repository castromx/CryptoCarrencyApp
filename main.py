import time
import flet as ft
import requests
from req import fetch_data_coins


data_coins = fetch_data_coins()
coin_names = [coin['name'] for coin in data_coins]
coin_ids = {coin['name']: coin['id'] for coin in data_coins}


async def main(page: ft.Page):
    page.title = 'CryptoCurrencyApp'
    page.window.width = 350
    page.window.height = 650
    ids = 'bitcoin'
    vs_currencies = 'usd'

    def set_ids(e):
        nonlocal ids
        selected_name = coin_names[e.control.selected_index]
        ids = coin_ids[selected_name]

    def button_clicked(e):
        params = {
            'ids': ids,
            'vs_currencies': vs_currencies,
            'include_market_cap': f'{include_market_cap.value}'.lower(),
            'include_24hr_vol': f'{include_24hr_vol.value}'.lower(),
            'include_24hr_change': f'{include_24hr_change.value}'.lower(),
            'include_last_updated_at': f'{include_last_updated_at.value}'.lower(),
            'precision': '2'
        }
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price', params=params)
            response.raise_for_status()

            data = response.json()
            coin_data = data.get(ids, {})

            result_text = f"Price ({vs_currencies}) 💵: {coin_data.get(vs_currencies, 'N/A')}"

            if f'{vs_currencies}_market_cap' in coin_data:
                result_text += f"\n💰 Market cap.: {coin_data[f'{vs_currencies}_market_cap']}"

            if f'{vs_currencies}_24h_vol' in coin_data:
                result_text += f"\n🪙 Volume for 24h: {coin_data[f'{vs_currencies}_24h_vol']}"

            if f'{vs_currencies}_24h_change' in coin_data:
                result_text += f"\n📈 {coin_data[f'{vs_currencies}_24h_change']}%"

            if 'last_updated_at' in coin_data:
                last_updated = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(coin_data['last_updated_at']))
                result_text += f"\n🕰 Last Update : {last_updated}"

            t.value = result_text
        except requests.exceptions.HTTPError:
            t.value = 'Rate limit exceeded. Waiting 30 seconds.'
        except Exception as err:
            print(f"Other error occurred: {err}")
            t.value = 'Error'
        page.update()

    t = ft.Text()
    coin_icon = ft.IconButton(
        icon=ft.icons.CURRENCY_BITCOIN,
        icon_color=ft.colors.YELLOW,
        icon_size=40,
        disabled=True
    )
    coin_row = ft.Column([
        ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=coin_names[i], value=coin_names[i]) for i in range(len(coin_names))
            ],
            on_select=set_ids,
        ),
        ft.Text("Type a name of crypto coin"),
    ])

    include_market_cap = ft.Switch(label="include_market_cap", value=True)
    include_24hr_vol = ft.Switch(label="include_24hr_vol", value=False)
    include_24hr_change = ft.Switch(label="include_24hr_change", value=False)
    include_last_updated_at = ft.Switch(label="include_last_updated_at")

    b = ft.ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(coin_icon, coin_row, include_market_cap, include_24hr_vol, include_24hr_change, include_last_updated_at, b, t)

ft.app(main)

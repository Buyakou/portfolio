import requests
import json

class BybitExchange:
    def get_data(self):
        url = "https://api2.bybit.com/fiat/otc/item/online"
        data = {
            "amount": "",
            "authMaker": False,
            "canTrade": False,
            "currencyId": "BYN",
            "page": "1",
            "payment": [],
            "side": "1",
            "size": "3", 
            "tokenId": "USDT",
            "userId": ""
        }
        response = requests.post(url, json=data)

        if response.status_code == 200:
            result_json = json.loads(response.text)
            items = result_json.get('result', {}).get('items', [])
            
            return items
        else:
            print("Error:", response.status_code)
            return []

exchange = BybitExchange()

data_items = exchange.get_data()

if data_items:
    
    for item in data_items:
        price = item.get('price')
        currencyId = item.get('currencyId')
        lastQuantity = item.get('lastQuantity')
        nickName = item.get('nickName')
        minAmount = item.get('minAmount')
        
        lastQuantity = float(lastQuantity)
        
        formatted_lastQuantity = "{:.2f}".format(lastQuantity)
        
        print("Цена:", price)
        print("Валюта:", currencyId)
        print("Доступно:", formatted_lastQuantity)
        print("Никнейм:", nickName)
        print("Мин. сумма:", minAmount)
        print("-------------------")

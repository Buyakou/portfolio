import time
import requests
import json
import tkinter as tk
from tkinter import ttk

class CryptoCurrencyParserApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Currency Parser")

        self.currency_label = ttk.Label(root, text="Валюта:")
        self.currency_label.pack()

        self.currency_var = tk.StringVar()
        self.currency_combobox = ttk.Combobox(root, textvariable=self.currency_var, values=["GBR", "BYN"])
        self.currency_combobox.pack()

        self.start_button = ttk.Button(root, text="Начать парсинг", command=self.start_parsing)
        self.start_button.pack()

        self.tree = ttk.Treeview(root, columns=("Price", "Currency", "Available", "Nickname"))
        self.tree.heading("Price", text="Price")
        self.tree.heading("Currency", text="Currency")
        self.tree.heading("Available", text="Available")
        self.tree.heading("Nickname", text="Nickname")
        self.tree.pack()

    def start_parsing(self):
        currency = self.currency_var.get()
        buyorsell = "BUY"
        quantity = 5

        pay_types = []
        if currency == "GBR":
            pay_types = ["Wise"]

        data = {
            "asset": "USDT",
            "countries": [],
            "fiat": currency,
            "page": 1,
            "payTypes": pay_types,
            "proMerchantAds": False,
            "publisherType": None,
            "rows": 10,
            "shieldMerchantAds": False,
            "tradeType": buyorsell,
            "transAmount": "99"
        }

        result = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json=data)
        result_json = json.loads(result.text)
        
        ads_list = result_json.get('data', [])
        
        for a in range(min(quantity, len(ads_list))):
            self.insert_into_table(a, ads_list)
            time.sleep(5)

    def insert_into_table(self, a, ads_list):
        adv = ads_list[a]['adv']
        availebale = adv.get('tradableQuantity', 'N/A')
        price = float(adv.get('price', 0))
        nick = ads_list[a]['advertiser'].get('nickName', 'N/A')
        currency = adv['fiat'][0] if 'fiat' in adv else 'N/A'
        self.tree.insert("", "end", values=(price, currency, availebale, nick))

if __name__ == "__main__":
    root = tk.Tk()
    app = CryptoCurrencyParserApp(root)
    root.mainloop()

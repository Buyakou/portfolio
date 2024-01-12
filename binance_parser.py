import requests
import json
import tkinter as tk
from tkinter import ttk

class CryptoCurrencyParserApp:
    def __init__(self, parent):
        self.parent = parent

        self.main_frame = ttk.Frame(parent, padding=10)
        self.main_frame.pack()

        self.trans_amount_label = ttk.Label(self.main_frame, text="Мин. сумма перевода:")
        self.trans_amount_label.grid(row=0, column=0, sticky="w")

        self.trans_amount_var = tk.StringVar()
        self.trans_amount_entry = ttk.Entry(self.main_frame, textvariable=self.trans_amount_var)
        self.trans_amount_entry.grid(row=0, column=1, sticky="w")

        self.start_button = ttk.Button(self.main_frame, text="Поиск", command=self.start_parsing)
        self.start_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        self.tree_buy = ttk.Treeview(parent, columns=("Price", "Currency", "Available", "Nickname", "MinTransAmount"))
        self.tree_buy.heading("Price", text="Цена")
        self.tree_buy.heading("Currency", text="Валюта")
        self.tree_buy.heading("Available", text="Доступно")
        self.tree_buy.heading("Nickname", text="Никнейм")
        self.tree_buy.heading("MinTransAmount", text="Мин. сумма")
        self.tree_buy.pack()

        self.tree_sell = ttk.Treeview(parent, columns=("Price", "Currency", "Available", "Nickname", "MinTransAmount"))
        self.tree_sell.heading("Price", text="Цена")
        self.tree_sell.heading("Currency", text="Валюта")
        self.tree_sell.heading("Available", text="Доступно")
        self.tree_sell.heading("Nickname", text="Никнейм")
        self.tree_sell.heading("MinTransAmount", text="Мин. сумма")
        self.tree_sell.pack()

        self.last_inserted_items_buy = []
        self.last_inserted_items_sell = []
    def start_parsing(self):
        if self.last_inserted_items_buy:
            for item in self.last_inserted_items_buy:
                self.tree_buy.delete(item)
            self.last_inserted_items_buy = []

        if self.last_inserted_items_sell:
            for item in self.last_inserted_items_sell:
                self.tree_sell.delete(item)
            self.last_inserted_items_sell = []

        min_trans_amount = self.trans_amount_var.get()
        quantity = 5

        pay_types = []
        currency = "BYN"

        data_buy = {
            "asset": "USDT",
            "countries": [],
            "fiat": currency,
            "page": 1,
            "payTypes": pay_types,
            "proMerchantAds": False,
            "publisherType": None,
            "rows": 10,
            "shieldMerchantAds": False,
            "tradeType": "BUY",
            "transAmount": min_trans_amount
        }

        data_sell = {
            "asset": "USDT",
            "countries": [],
            "fiat": currency,
            "page": 1,
            "payTypes": pay_types,
            "proMerchantAds": False,
            "publisherType": None,
            "rows": 10,
            "shieldMerchantAds": False,
            "tradeType": "SELL",
            "transAmount": min_trans_amount
        }

        self.update_data_periodically(data_buy, quantity, self.tree_buy, self.last_inserted_items_buy)
        self.update_data_periodically(data_sell, quantity, self.tree_sell, self.last_inserted_items_sell)
    def update_data_periodically(self, data, quantity, tree, last_inserted_items):
        result = requests.post("https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search", json=data)
        result_json = json.loads(result.text)

        ads_list = result_json.get('data', [])

        for item in last_inserted_items:
            tree.delete(item)

        last_inserted_items.clear()

        for a in range(min(quantity, len(ads_list))):
            self.insert_into_table(a, ads_list, tree, last_inserted_items)

        if tree == self.tree_buy:
            self.parent.after(5000, self.update_data_periodically, data, quantity, tree, last_inserted_items)
        elif tree == self.tree_sell:
            self.parent.after(5000, self.update_data_periodically, data, quantity, tree, last_inserted_items)
    def insert_into_table(self, a, ads_list, tree, last_inserted_items):
        adv = ads_list[a]['adv']
        available = adv.get('tradableQuantity', 'N/A')
        price = float(adv.get('price', 0))
        nick = ads_list[a]['advertiser'].get('nickName', 'N/A')
        currency = "BYN"
        min_single_trans_amount = adv.get('minSingleTransAmount', 'N/A')

        item = tree.insert("", "end", values=(price, currency, available, nick, min_single_trans_amount))
        last_inserted_items.append(item)
class OrderBookApp:
    def __init__(self, parent):
        self.parent = parent

        self.fetch_button = tk.Button(parent, text="Получить данные", command=self.fetch_data)
        self.fetch_button.pack(pady=10)

        self.asks_text = tk.Text(parent, height=10, width=40)
        self.asks_text.pack(side=tk.LEFT, padx=10)

        self.bids_text = tk.Text(parent, height=10, width=40)
        self.bids_text.pack(side=tk.RIGHT, padx=10)

        self.result_label = tk.Label(parent, text="")
        self.result_label.pack()

        self.fetch_data() 
    def fetch_data(self):
        response = requests.get("https://bynex.io/trading/ru/api/symbolOrderBook/pair/USDT-BYN")

        if response.status_code == 200:
            data = response.json()
            asks = data['asks']
            bids = data['bids']

            asks_price_sums = {}
            bids_price_sums = {}

            for deal in asks:
                price = deal['price']
                volume = deal['volume']

                if price in asks_price_sums:
                    asks_price_sums[price] += volume
                else:
                    asks_price_sums[price] = volume

            for deal in bids:
                price = deal['price']
                volume = deal['volume']

                if price in bids_price_sums:
                    bids_price_sums[price] += volume
                else:
                    bids_price_sums[price] = volume

            self.asks_text.delete(1.0, tk.END)
            sorted_asks = sorted(asks_price_sums.items(), key=lambda x: x[0])
            for price, volume in sorted_asks[:7]:
                formatted_price = "{:.5f}".format(price)
                formatted_volume = "{:.2f}".format(volume)
                self.asks_text.insert(tk.END, f"Цена: {formatted_price}, Объём: {formatted_volume}\n")

            self.bids_text.delete(1.0, tk.END)
            sorted_bids = sorted(bids_price_sums.items(), key=lambda x: x[0], reverse=True)
            for price, volume in sorted_bids[:7]:
                formatted_price = "{:.5f}".format(price)
                formatted_volume = "{:.2f}".format(volume)
                self.bids_text.insert(tk.END, f"Цена: {formatted_price}, Объём: {formatted_volume}\n")

        self.result_label.config(text="")
        self.parent.after(5000, self.fetch_data) 

class MainApp:
    def __init__(self, parent):
        self.parent = parent

        tab_control = ttk.Notebook(parent)

        tab_combined = ttk.Frame(tab_control)
        tab_control.add(tab_combined, text="Объединенное приложение")

        parser_app = CryptoCurrencyParserApp(tab_combined)
        order_book_app = OrderBookApp(tab_combined)

        tab_control.pack(expand=1, fill="both")
def main():
    root = tk.Tk()
    root.title("Crypto Currency Tool")

    app = MainApp(root)

    root.mainloop()

if __name__ == "__main__":
    main()

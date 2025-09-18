import requests
import csv

def obtener_datos_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "payTypes": ["Banesco"],
        "tradeType": "SELL",
        "page": 1,
        "rows": 3
    }

    response = requests.post(url, json=payload)
    data = response.json().get("data", [])

    with open("offers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Precio", "Mínimo", "Máximo"])
        for offer in data:
            writer.writerow([
                offer["advertiser"]["nickName"],
                offer["adv"]["price"],
                offer["adv"]["minSingleTransAmount"],
                offer["adv"]["maxSingleTransAmount"]
            ])

if __name__ == "__main__":
    obtener_datos_binance()

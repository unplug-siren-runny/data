import requests
import json

def obtener_json_completo():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "payTypes": ["Banesco"],
        "tradeType": "SELL",
        "page": 1,
        "rows": 2
    }
    response = requests.post(url, json=payload)
    data = response.json()
    # Guardar JSON completo en archivo para análisis
    with open("response_complete.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return data

if __name__ == "__main__":
    obtener_json_completo()

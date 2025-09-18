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
        "rows": 2  # Solo las dos primeras ofertas
    }

    response = requests.post(url, json=payload)
    data = response.json().get("data", [])

    # Generar archivo CSV
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

    # Generar archivo HTML estático
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Ofertas Binance P2P</title>
</head>
<body>
  <h1>Ofertas Binance P2P</h1>
  <table border="1" cellpadding="5" cellspacing="0">
    <thead>
      <tr><th>Nombre</th><th>Precio</th><th>Mínimo</th><th>Máximo</th></tr>
    </thead>
    <tbody>
"""
    for offer in data:
        html_content += f"<tr><td>{offer['advertiser']['nickName']}</td><td>{offer['adv']['price']}</td><td>{offer['adv']['minSingleTransAmount']}</td><td>{offer['adv']['maxSingleTransAmount']}</td></tr>\n"

    html_content += """
    </tbody>
  </table>
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

if __name__ == "__main__":
    obtener_datos_binance()

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
        "rows": 2
    }

    response = requests.post(url, json=payload)
    data = response.json().get("data", [])

    with open("offers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Precio", "Mínimo (VES)", "Máximo (VES)", "Cantidad disponible (USDT)", "Método"])
        for offer in data:
            nombre = offer["advertiser"]["nickName"]
            precio = offer["adv"]["price"]
            minimo = offer["adv"]["minSingleTransAmount"]
            maximo = offer["adv"]["maxSingleTransAmount"]
            disponible = offer["adv"]["surplusAmount"]
            metodos = ", ".join([m["tradeMethodName"] for m in offer["adv"]["tradeMethods"]])

            writer.writerow([nombre, precio, minimo, maximo, disponible, metodos])

    # Generar archivo HTML estático con tabla
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Ofertas Binance P2P</title>
</head>
<body>
  <h1>Ofertas Binance P2P con Banesco</h1>
  <table border="1" cellpadding="5" cellspacing="0">
    <thead>
      <tr><th>Nombre</th><th>Precio</th><th>Mínimo (VES)</th><th>Máximo (VES)</th><th>Cantidad disponible (USDT)</th><th>Método</th></tr>
    </thead>
    <tbody>
"""
    for offer in data:
        nombre = offer["advertiser"]["nickName"]
        precio = offer["adv"]["price"]
        minimo = offer["adv"]["minSingleTransAmount"]
        maximo = offer["adv"]["maxSingleTransAmount"]
        disponible = offer["adv"]["surplusAmount"]
        metodos = ", ".join([m["tradeMethodName"] for m in offer["adv"]["tradeMethods"]])

        html_content += f"<tr><td>{nombre}</td><td>{precio}</td><td>{minimo}</td><td>{maximo}</td><td>{disponible}</td><td>{metodos}</td></tr>\n"

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

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
        "rows": 3,  # Solo los primeros 3 resultados
        "publisherType": "merchant"  # Filtro para vendedores verificados
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    print(response_json)  # Para debug y ver respuesta
    data = response_json.get("data") or []
    with open("offers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Precio"])
        for offer in data[:3]:  # Solo primeros 3
            nombre = offer["advertiser"]["nickName"]
            precio = offer["adv"]["price"]
            writer.writerow([nombre, precio])
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Ofertas Binance P2P - Verified Merchants</title>
</head>
<body>
  <h1>Ofertas Binance P2P (Solo Vendedores Verificados)</h1>
  <table border="1" cellpadding="5" cellspacing="0">
    <thead>
      <tr><th>Nombre</th><th>Precio</th></tr>
    </thead>
    <tbody>
"""
    for offer in data[:3]:  # Solo primeros 3
        nombre = offer["advertiser"]["nickName"]
        precio = offer["adv"]["price"]
        html_content += f"<tr><td>{nombre}</td><td>{precio}</td></tr>\n"
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

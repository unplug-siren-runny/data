import requests
import csv

def obtener_datos_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    rows_per_page = 10
    max_pages = 5
    collected_offers = []

    for page in range(1, max_pages + 1):
        payload = {
            "asset": "USDT",
            "fiat": "VES",
            "payTypes": ["Banesco"],
            "tradeType": "SELL",
            "page": page,
            "rows": rows_per_page
        }
        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()
        data = response_json.get("data") or []

        verified_offers = [offer for offer in data if offer["advertiser"].get("proMerchant")]
        print(f"Página {page}: {len(verified_offers)} vendedores verificados encontrados.")
        if not verified_offers:
            # No más vendedores verificados, podrías romper el bucle
            break
        collected_offers.extend(verified_offers)

    if not collected_offers:
        print("No se encontraron vendedores verificados en las páginas consultadas.")
        return

    with open("offers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Precio", "Mínimo (VES)", "Máximo (VES)", "Cantidad disponible (USDT)", "Método"])
        for offer in collected_offers:
            nombre = offer["advertiser"]["nickName"]
            precio = offer["adv"]["price"]
            minimo = offer["adv"]["minSingleTransAmount"]
            maximo = offer["adv"]["maxSingleTransAmount"]
            disponible = offer["adv"]["surplusAmount"]
            metodos = ", ".join([m["tradeMethodName"] for m in offer["adv"]["tradeMethods"]])
            writer.writerow([nombre, precio, minimo, maximo, disponible, metodos])

    html_content = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <title>Ofertas Binance P2P con Banesco - Verified Merchants</title>
</head>
<body>
  <h1>Ofertas Binance P2P con Banesco - Vendedores Verificados</h1>
  <table border="1" cellpadding="5" cellspacing="0">
    <thead>
      <tr><th>Nombre</th><th>Precio</th><th>Mínimo (VES)</th><th>Máximo (VES)</th><th>Cantidad disponible (USDT)</th><th>Método</th></tr>
    </thead>
    <tbody>
"""

    for offer in collected_offers:
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

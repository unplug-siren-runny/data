import requests
import csv
import subprocess
def obtener_datos_binance():
    url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    payload = {
        "asset": "USDT",
        "fiat": "VES",
        "payTypes": ["Banesco"],
        "tradeType": "SELL",
        "page": 1,
        "rows": 3,  # Cambiado a 3
        "publisherType": "merchant"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_json = response.json()
    print(response_json)
    data = response_json.get("data") or []
    with open("offers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Nombre", "Precio", "Mínimo (VES)", "Máximo (VES)", "Cantidad disponible (USDT)", "Método"])
        for offer in data[:3]:  # Recorrer solo 3 ítems
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
  <title>Ofertas Binance P2P - Verified Merchants</title>
</head>
<body>
  <h1>Ofertas Binance P2P (Solo Vendedores Verificados)</h1>
  <table border="1" cellpadding="5" cellspacing="0">
    <thead>
      <tr><th>Nombre</th><th>Precio</th><th>Mínimo (VES)</th><th>Máximo (VES)</th><th>Cantidad disponible (USDT)</th><th>Método</th></tr>
    </thead>
    <tbody>
"""
    for offer in data[:3]:
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

def git_commit_and_push():
    subprocess.run(["git", "config", "user.name", "github-actions[bot]"], check=True)
    subprocess.run(["git", "config", "user.email", "github-actions[bot]@users.noreply.github.com"], check=True)
    subprocess.run(["git", "add", "offers.csv", "index.html"], check=True)
    commit_result = subprocess.run(["git", "commit", "-m", "Actualizar tasas Binance P2P automáticamente"], capture_output=True, text=True)
    if "nothing to commit" in commit_result.stdout:
        print("No hay cambios para commitear.")
    else:
        subprocess.run(["git", "push"], check=True)

if __name__ == "__main__":
    obtener_datos_binance()
    git_commit_and_push()

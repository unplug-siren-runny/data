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
        "rows": 3,
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
        writer.writerow(["Nombre", "Precio"])
        for offer in data[:3]:
            nombre = offer["advertiser"]["nickName"]
            precio = offer["adv"]["price"]
            writer.writerow([nombre, precio])
    html_content = """
<!DOCTYPE html>
<html lang="es">
<head><meta charset="UTF-8" /><title>Ofertas Binance P2P</title></head>
<body>
<table border="1">
<thead><tr><th>Nombre</th><th>Precio</th></tr></thead>
<tbody>
"""
    for offer in data[:3]:
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

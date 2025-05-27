# Bibliotecas necessárias 
import json
import requests
import mysql.connector
from datetime import datetime

hoje_formatado = datetime.now().strftime("%Y%m%d")

# Conexão com o banco de dados MySQL
conn = mysql.connector.connect(
    # host='localhost',
    # port='3306',
    # user='root',
    # password='',
    # database='your_database_name',
)

cursor = conn.cursor(dictionary=True)

# IMPLEMENTAR DIA NA SELECT

query = f"""
DIGITE SEU SELECT AQUI
"""

cursor.execute(query)
dados = cursor.fetchall()

cursor.close()
conn.close()


for item in dados:
    url = f"http://api.anymarket.com.br/v2/orders/{item['orderId']}"
    
    now = datetime.now().isoformat(timespec='seconds') + "-03:00"
    payload = {
        "status": "INVOICED",
        "invoice": {
            "accessKey": item["accessKey"],
            "series": str(item["series"]),
            "number": str(item["number"]),
            "date": now
        }
    }

    headers = {
        "Content-Type": "application/json",
        "gumgaToken": "DIGITE O GUMGATOKEN ANYMARKET AQUI",
        "authorization": "DIGITE O GUMGATOKEN ANYMARKET AQUI"
    }

#Montagem cURL
    
    curl = f"""curl -X PUT {url} \\
  -H "Content-Type: application/json" \\
  -H "gumgaToken: {headers['gumgaToken']}" \\
  -H "authorization: {headers['authorization']}" \\
  -d '{json.dumps(payload)}'"""
    print("\n Comando cURL gerado:")
    print(curl)

    
    print(f"\nEnviando pedido {item['orderId']}\n")
    response = requests.put(url, headers=headers, json=payload)
    print(f"Pedido {item['orderId']} enviado com sucesso! Status: {response.status_code}\n")

    if response.status_code == 200:
        print(f"Pedido {item['orderId']} enviado com sucesso!\n")
    else:
        # Tenta novamente com outro status
        print(f"Falha no pedido {item['orderId']}. Tentando com status PAID_WAITING_DELIVERY...\n")
        payload["status"] = "PAID_WAITING_DELIVERY"
        retry_response = requests.put(url, headers=headers, json=payload)
        print(f"Retentativa enviada. Status: {retry_response.status_code}\n")
import json
import requests
import time

API_URL = "https://economia.awesomeapi.com.br/last/XAU-EUR"

def fetch_gold_price():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            return {"error": f"Erro ao acessar a API: {response.status_code}"}

        data = response.json().get("XAUEUR")
        if not data:
            return {"error": "Dados não encontrados na resposta da API"}

        price = float(data["bid"])
        price_gram_24k = price / 31.1035
        price_gram_22k = price_gram_24k * (22 / 24)
        price_gram_21k = price_gram_24k * (21 / 24)
        price_gram_20k = price_gram_24k * (20 / 24)
        price_gram_18k = price_gram_24k * (18 / 24)
        price_gram_14k = price_gram_24k * (14 / 24)
        price_gram_10k = price_gram_24k * (10 / 24)

        gold_price_data = {
            "timestamp": int(time.time()),
            "metal": "XAU",
            "currency": "EUR",
            "exchange": "LIVEPRICE",
            "symbol": "LIVEPRICE:XAUUSD",
            "price": round(price, 2),
            "price_gram_24k": round(price_gram_24k, 2),
            "price_gram_22k": round(price_gram_22k, 2),
            "price_gram_21k": round(price_gram_21k, 2),
            "price_gram_19,2k": round(price_gram_20k * 0.755, 2),
            "price_gram_18k": round(price_gram_18k, 2),
            "price_gram_14k": round(price_gram_14k, 2),
            "price_gram_10k": round(price_gram_10k, 2),
        }

        return gold_price_data

    except Exception as e:
        return {"error": str(e)}

def handler(event, context):
    gold_price = fetch_gold_price()
    return {
        "statusCode": 200,
        "body": json.dumps(gold_price),
        "headers": {
            "Content-Type": "application/json"
        }
    }

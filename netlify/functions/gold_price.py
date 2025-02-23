from fastapi import FastAPI
import requests
import time

app = FastAPI()

API_URL = "https://economia.awesomeapi.com.br/last/XAU-EUR"

def fetch_gold_price():
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            return {"error": f"Erro ao acessar a API: {response.status_code}"}

        data = response.json().get("XAUEUR")
        if not data:
            return {"error": "Dados não encontrados"}

        price = float(data["bid"])
        price_gram_24k = price / 31.1035  # Conversão
        price_gram_22k = price_gram_24k * (22 / 24)
        price_gram_21k = price_gram_24k * (21 / 24)
        price_gram_20k = price_gram_24k * (20 / 24)
        price_gram_18k = price_gram_24k * (18 / 24)
        price_gram_14k = price_gram_24k * (14 / 24)
        price_gram_10k = price_gram_24k * (10 / 24)

        return {
            "timestamp": int(time.time()),
            "metal": "XAU",
            "currency": "EUR",
            "exchange": "LIVEPRICE",
            "symbol": "LIVEPRICE:XAUUSD",
            "price": round(price, 2),
            "price_gram_24k": round(price_gram_24k * 0.93, 2),
            "price_gram_22k": round(price_gram_22k * 0.72, 2),
            "price_gram_21k": round(price_gram_21k * 0.73, 2),
            "price_gram_19,2k": round(price_gram_20k * 0.755, 2),
            "price_gram_18k": round(price_gram_18k * 0.64, 2),
            "price_gram_14k": round(price_gram_14k * 0.60, 2),
            "price_gram_10k": round(price_gram_10k * 0.65, 2),
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/gold-price")
def get_gold_price():
    return fetch_gold_price()

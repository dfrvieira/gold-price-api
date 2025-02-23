from fastapi import FastAPI
import requests
import time
from apscheduler.schedulers.background import BackgroundScheduler

app = FastAPI()

API_URL = "https://economia.awesomeapi.com.br/last/XAU-EUR"
gold_price_data = {}

def fetch_gold_price():
    global gold_price_data
    try:
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"❌ Erro ao acessar a API: {response.status_code}")
            return

        data = response.json().get("XAUEUR")
        if not data:
            print("❌ Dados não encontrados na resposta da API")
            return

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

        print(f"✅ Preço atualizado: {gold_price_data}")

    except Exception as e:
        print(f"❌ Erro ao processar os dados: {str(e)}")

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_gold_price, "interval", minutes=10)
scheduler.start()

@app.get("/")
async def root():
    return {"message": "API de preços do ouro está online!"}

@app.get("/gold-price")
async def get_gold_price():
    return gold_price_data

fetch_gold_price()

from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import re

app = FastAPI()

def get_card_price(card_name):
    keyword = f"ポケモンカード {card_name}"
    url = f"https://auctions.yahoo.co.jp/search/search?p={keyword}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.select(".Product")
        prices = []
        for p in products[:5]:
            price_elem = p.select_one(".Product__priceValue")
            if price_elem:
                price_num = int(re.sub(r"[^\d]", "", price_elem.text))
                prices.append(price_num)
        if prices:
            return sum(prices) // len(prices)
    except Exception:
        pass
    return 0

@app.get("/api/cards")
def get_cards():
    target_cards = ["ピカチュウ", "リザードン", "ミュウツー"]
    api_data = []
    
    for i, name in enumerate(target_cards, 1):
        market_price = get_card_price(name)
        api_data.append({
            "id": f"card-00{i}",
            "name": name,
            "price": market_price,
            "stock": 10
        })
        
    return api_data

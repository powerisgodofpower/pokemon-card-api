from fastapi import FastAPI

app = FastAPI()

@app.get("/api/cards")
def get_cards():
    return [
        {"id": "pika-001", "name": "ピカチュウ", "price": 1500, "stock": 5},
        {"id": "char-002", "name": "リザードン", "price": 12000, "stock": 2},
    ]
from fastapi import FastAPI, Query
from typing import Optional, List
from pydantic import BaseModel

app = FastAPI(
    title="Pokemon TCG Market Price API",
    description="Real-time Japanese Pokémon card market prices for global developers.",
    version="1.0.0"
)

# 海外開発者が求める正確なデータ構造
class CardPrice(BaseModel):
    card_id: str          # 型番（例: "SV2a-173"）
    name_ja: str          # 日本語名
    name_en: str          # 英語名（海外エンジニア用）
    set_name: str         # 収録パック名
    card_number: str      # カード番号（例: "173/165"）
    rarity: str           # レアリティ（SAR, SR, AR, etc.）
    price_jpy: int        # 相場価格（日本円）
    stock_status: str     # 在庫状況（in_stock, low_stock, out_of_stock）
    updated_at: str       # 最終更新日時

# 詳細データを持たせたデータベース（サンプル）
CARD_DATABASE: List[dict] = [
    {
        "card_id": "SV2a-205",
        "name_ja": "リザードンex",
        "name_en": "Charizard ex",
        "set_name": "ポケモンカード151",
        "card_number": "205/165",
        "rarity": "SAR",
        "price_jpy": 24800,
        "stock_status": "in_stock",
        "updated_at": "2026-10-08 18:00"
    },
    {
        "card_id": "SV2a-173",
        "name_ja": "ピカチュウ",
        "name_en": "Pikachu",
        "set_name": "ポケモンカード151",
        "card_number": "173/165",
        "rarity": "AR",
        "price_jpy": 2480,
        "stock_status": "in_stock",
        "updated_at": "2026-10-08 18:00"
    },
    {
        "card_id": "SV1S-098",
        "name_ja": "ミモザ",
        "name_en": "Miriam",
        "set_name": "バイオレットex",
        "card_number": "098/078",
        "rarity": "SAR",
        "price_jpy": 39800,
        "stock_status": "low_stock",
        "updated_at": "2026-10-08 18:00"
    },
    {
        "card_id": "SV4a-348",
        "name_ja": "ナンジャモ",
        "name_en": "Iono",
        "set_name": "シャイニートレジャーex",
        "card_number": "348/190",
        "rarity": "SAR",
        "price_jpy": 29800,
        "stock_status": "in_stock",
        "updated_at": "2026-10-08 18:00"
    }
]

# 検索・絞り込み対応エンドポイント
@app.get("/cards", response_model=List[CardPrice])
def get_cards(
    search: Optional[str] = Query(None, description="カード名、英語名、または型番（例: ピカチュウ, Pikachu, SV2a-173）"),
    rarity: Optional[str] = Query(None, description="レアリティ（例: SAR, SR, AR）"),
    limit: int = Query(20, ge=1, le=100)
):
    results = CARD_DATABASE

    # 検索処理
    if search:
        search_kw = search.lower()
        results = [
            card for card in results 
            if search_kw in card["name_ja"].lower() 
            or search_kw in card["name_en"].lower()
            or search_kw in card["card_id"].lower()
        ]

    # レアリティ絞り込み
    if rarity:
        results = [card for card in results if card["rarity"].upper() == rarity.upper()]

    return results[:limit]

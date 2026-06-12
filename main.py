from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

app = FastAPI(title="Stock Scanner AI - Gap + Momentum")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_smart_candidates():
    """Gera candidatos de forma mais realista e variada"""
    
    base_tickers = [
        {"ticker": "HCAI", "base_price": 9.40},
        {"ticker": "TGL", "base_price": 5.15},
        {"ticker": "LUD", "base_price": 4.90},
        {"ticker": "PRBKY", "base_price": 11.20},
        {"ticker": "SOXS", "base_price": 6.15},
        {"ticker": "MBAVU", "base_price": 13.10},
        {"ticker": "CCHH", "base_price": 0.85},
    ]

    candidates = []

    for stock in base_tickers:
        # Variação de preço entre -8% e +38%
        change = round(random.uniform(-8.0, 38.0), 1)
        price = round(stock["base_price"] * (1 + change/100), 2)
        volume = random.randint(750_000, 4_800_000)

        # Lógica de qualidade do setup
        if change >= 22 and volume > 2_000_000:
            grade = random.choice(["A", "A-"])
            risk = "LOW"
            score = round(random.uniform(7.8, 9.3), 1)
            stage = "EARLY"
        elif change >= 10:
            grade = random.choice(["B+", "B", "B-"])
            risk = "MEDIUM"
            score = round(random.uniform(5.9, 7.6), 1)
            stage = "DEVELOPING"
        else:
            grade = random.choice(["C+", "C", "C-"])
            risk = random.choice(["HIGH", "MEDIUM"])
            score = round(random.uniform(3.2, 5.4), 1)
            stage = "EXTENDED"

        candidates.append({
            "ticker": stock["ticker"],
            "price": price,
            "change_pct": change,
            "volume": volume,
            "setup_grade": grade,
            "risk_level": risk,
            "opportunity_score": score,
            "movement_stage": stage,
            "catalyst": random.choice([
                "Balanço forte + guidance elevado",
                "Contrato relevante anunciado",
                "Volume anormal + gap técnico",
                "Possível short squeeze",
                "Movimento setorial sem catalisador claro"
            ]),
            "red_flags": random.choice([
                "Nenhum",
                "Float baixo - alta volatilidade",
                "Liquidez moderada",
                "Já subiu muito no dia",
                "Sem catalisador fundamental claro"
            ]),
            "liquidity_score": random.randint(4, 8),
            "comment": "Setup gerado dinamicamente"
        })

    # Ordena do melhor para o pior
    candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return candidates


@app.get("/")
def root():
    return {"message": "Stock Scanner AI está rodando", "status": "ok"}


@app.get("/api/v1/scan")
def scan(
    mode: str = Query("auto"),
    preferred_ai: str = Query("grok")
):
    candidates = generate_smart_candidates()

    return {
        "timestamp": datetime.now().isoformat(),
        "market_regime": "RISK-ON",
        "mode": mode,
        "preferred_ai": preferred_ai,
        "total_candidates": len(candidates),
        "candidates": candidates
    }


@app.get("/api/v1/status")
def status():
    return {"status": "online", "message": "Scanner funcionando"}

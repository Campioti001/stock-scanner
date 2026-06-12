from fastapi import FastAPI, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import json
import random

app = FastAPI(title="Stock Scanner AI - Gap + Momentum")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def generate_aggressive_candidates(regime: str = "RISK_ON"):
    base_tickers = [
        {"ticker": "HCAI", "base_price": 9.40},
        {"ticker": "TGL", "base_price": 5.15},
        {"ticker": "LUD", "base_price": 4.90},
        {"ticker": "PRBKY", "base_price": 11.20},
        {"ticker": "SOXS", "base_price": 6.15},
        {"ticker": "MBAVU", "base_price": 13.10},
        {"ticker": "CCHH", "base_price": 0.85},
        {"ticker": "VSME", "base_price": 2.60},
    ]

    candidates = []

    for stock in base_tickers:
        if regime == "RISK_ON":
            change = round(random.uniform(-5.0, 42.0), 1)
        elif regime == "RISK_OFF":
            change = round(random.uniform(-12.0, 18.0), 1)
        else:
            change = round(random.uniform(-8.0, 28.0), 1)

        price = round(stock["base_price"] * (1 + change / 100), 2)
        volume = random.randint(650_000, 5_200_000)

        if change >= 25 and volume > 1_800_000:
            grade = random.choice(["A", "A-"])
            risk = random.choice(["MEDIUM", "HIGH"])
            score = round(random.uniform(7.2, 9.4), 1)
            stage = random.choice(["EARLY", "DEVELOPING"])
        elif change >= 12:
            grade = random.choice(["B+", "B", "B-"])
            risk = "MEDIUM"
            score = round(random.uniform(5.5, 7.5), 1)
            stage = "DEVELOPING"
        else:
            grade = random.choice(["C+", "C", "C-"])
            risk = random.choice(["HIGH", "MEDIUM"])
            score = round(random.uniform(2.8, 5.2), 1)
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
                "Já subiu muito no dia - risco de reversão",
                "Sem catalisador fundamental claro"
            ]),
            "liquidity_score": random.randint(3, 8),
            "comment": "Setup gerado de forma agressiva"
        })

    candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return candidates


@app.get("/")
def root():
    return {"message": "Stock Scanner AI está rodando", "status": "ok"}


@app.get("/api/v1/scan")
def scan(
    mode: str = Query("auto"),
    preferred_ai: str = Query("grok"),
    regime: str = Query("RISK_ON")
):
    candidates = generate_aggressive_candidates(regime=regime)

    data = {
        "timestamp": datetime.now().isoformat(),
        "market_regime": regime,
        "mode": mode,
        "preferred_ai": preferred_ai,
        "total_candidates": len(candidates),
        "candidates": candidates
    }

    # Retorna JSON formatado e legível
    return Response(
        content=json.dumps(data, indent=2, ensure_ascii=False),
        media_type="application/json"
    )


@app.get("/api/v1/status")
def status():
    return {"status": "online", "message": "Scanner funcionando"}

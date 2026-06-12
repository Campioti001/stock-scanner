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

# ============================================
# FUNÇÃO QUE GERA CANDIDATOS SIMULADOS (mais inteligente)
# ============================================
def generate_candidates(market_regime: str = "RISK_ON", quality: str = "mixed"):
    """
    Gera candidatos de forma mais realista e variada.
    """
    candidates = []

    # Base de tickers com diferentes perfis
    base_tickers = [
        {"ticker": "HCAI", "base_price": 9.40, "sector": "tech"},
        {"ticker": "TGL", "base_price": 5.15, "sector": "tech"},
        {"ticker": "LUD", "base_price": 4.90, "sector": "industrial"},
        {"ticker": "PRBKY", "base_price": 11.20, "sector": "health"},
        {"ticker": "SOXS", "base_price": 6.15, "sector": "etf"},
    ]

    for stock in base_tickers:
        # Variação de preço e volume
        price_variation = random.uniform(-0.08, 0.35)  # -8% até +35%
        current_price = round(stock["base_price"] * (1 + price_variation), 2)
        change_pct = round(price_variation * 100, 1)

        # Volume simulado
        volume = random.randint(800000, 4500000)

        # Lógica de Setup Grade e Risk Level
        if change_pct > 20 and volume > 2000000:
            setup_grade = random.choice(["A", "A-", "B+"])
            risk_level = "LOW" if change_pct < 30 else "MEDIUM"
            opportunity = round(random.uniform(7.5, 9.2), 1)
            stage = "EARLY" if change_pct < 25 else "DEVELOPING"
        elif change_pct > 8:
            setup_grade = random.choice(["B+", "B", "B-"])
            risk_level = "MEDIUM"
            opportunity = round(random.uniform(5.8, 7.4), 1)
            stage = "DEVELOPING"
        else:
            setup_grade = random.choice(["C+", "C", "C-"])
            risk_level = random.choice(["HIGH", "MEDIUM"])
            opportunity = round(random.uniform(3.5, 5.5), 1)
            stage = "EXTENDED"

        # Catalisador simulado
        catalysts = [
            "Balanço acima do esperado + guidance elevado",
            "Anúncio de contrato relevante",
            "Possível short squeeze via redes sociais",
            "Movimento setorial forte (sem catalisador específico)",
            "Gap com volume anormal - possível hype de low float"
        ]

        red_flags_list = [
            "Nenhum",
            "Float baixo (~3.5M) - maior volatilidade",
            "Liquidez moderada para posições maiores",
            "Já subiu muito no dia - risco de reversão",
            "Sem catalisador fundamental claro"
        ]

        candidate = {
            "ticker": stock["ticker"],
            "price": current_price,
            "change_pct": change_pct,
            "volume": volume,
            "setup_grade": setup_grade,
            "risk_level": risk_level,
            "opportunity_score": opportunity,
            "movement_stage": stage,
            "catalyst": random.choice(catalysts),
            "red_flags": random.choice(red_flags_list),
            "liquidity_score": random.randint(4, 8),
            "comment": "Setup gerado com base em volume e variação de preço."
        }
        candidates.append(candidate)

    # Ordena por opportunity_score (melhores primeiro)
    candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)

    return candidates


@app.get("/")
def root():
    return {
        "message": "Stock Scanner AI - Gap + Momentum",
        "status": "online",
        "version": "1.1"
    }


@app.get("/api/v1/scan")
def scan(
    mode: str = Query("auto", description="Modo de operação"),
    preferred_ai: str = Query("grok", description="IA preferida"),
    regime: str = Query("RISK_ON", description="Regime de mercado simulado"),
    quality: str = Query("mixed", description="Qualidade dos setups")
):
    """
    Endpoint principal do scanner.
    Agora gera dados de forma mais inteligente e variada.
    """
    candidates = generate_candidates(market_regime=regime, quality=quality)

    return {
        "timestamp": datetime.now().isoformat(),
        "market_regime": regime,
        "mode": mode,
        "preferred_ai": preferred_ai,
        "total_candidates": len(candidates),
        "candidates": candidates
    }


@app.get("/api/v1/status")
def status():
    return {
        "status": "online",
        "message": "Stock Scanner AI funcionando corretamente",
        "python_version": "3.11.9"
    }

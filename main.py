from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(title="Stock Scanner AI")

# Permite que o frontend (celular) chame o backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Stock Scanner AI está rodando!"}

@app.get("/api/v1/scan")
def scan(mode: str = "auto", preferred_ai: str = "grok"):
    """
    Endpoint principal do scanner.
    Por enquanto retorna dados simulados.
    Depois vamos conectar com Grok e Claude de verdade.
    """
    
    # Dados simulados de exemplo (vamos melhorar depois)
    candidates = [
        {
            "ticker": "HCAI",
            "price": 9.45,
            "change_pct": 28.5,
            "volume": 2450000,
            "setup_grade": "A",
            "risk_level": "LOW",
            "opportunity_score": 8.4,
            "movement_stage": "EARLY",
            "catalyst": "Balanço acima do esperado + guidance elevado",
            "red_flags": "Nenhum",
            "liquidity_score": 7,
            "comment": "Melhor setup do dia. Catalisador real e movimento saudável."
        },
        {
            "ticker": "TGL",
            "price": 5.20,
            "change_pct": 14.2,
            "volume": 1850000,
            "setup_grade": "B+",
            "risk_level": "MEDIUM",
            "opportunity_score": 7.1,
            "movement_stage": "DEVELOPING",
            "catalyst": "Contrato de expansão no Sudeste Asiático",
            "red_flags": "Float baixo (~3.5M)",
            "liquidity_score": 6,
            "comment": "Bom catalisador, mas exige stop bem ajustado."
        },
        {
            "ticker": "LUD",
            "price": 4.95,
            "change_pct": 11.8,
            "volume": 980000,
            "setup_grade": "B",
            "risk_level": "MEDIUM",
            "opportunity_score": 6.8,
            "movement_stage": "DEVELOPING",
            "catalyst": "Anúncio de contrato relevante",
            "red_flags": "Liquidez moderada",
            "liquidity_score": 6,
            "comment": "Setup aceitável com catalisador real."
        },
        {
            "ticker": "VSME",
            "price": 2.65,
            "change_pct": 185.0,
            "volume": 125000000,
            "setup_grade": "C",
            "risk_level": "HIGH",
            "opportunity_score": 3.9,
            "movement_stage": "EXTENDED",
            "catalyst": "Possível short squeeze via redes sociais",
            "red_flags": "Sem catalisador fundamental claro. Já subiu muito.",
            "liquidity_score": 4,
            "comment": "Armadilha clássica de low-float. Evitar."
        },
        {
            "ticker": "KMRK",
            "price": 6.80,
            "change_pct": 320.0,
            "volume": 89000000,
            "setup_grade": "D",
            "risk_level": "TRAP",
            "opportunity_score": 2.1,
            "movement_stage": "EXHAUSTED",
            "catalyst": "Nenhum catalisador identificado",
            "red_flags": "Gap extremo sem sustentação. Alto risco de reversão violenta.",
            "liquidity_score": 3,
            "comment": "Evitar completamente. Movimento sem fundamento."
        }
    ]
    
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
    return {"status": "online", "message": "Stock Scanner AI funcionando"}

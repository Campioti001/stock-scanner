from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse, Response
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

# ==================== LÓGICA DOS CANDIDATOS (mantida e melhorada) ====================
def generate_aggressive_candidates(regime: str = "RISK_ON"):
    tickers = ["PRBKY", "HCAI", "SOXS", "TGL", "LUD", "VSME", "CCHH", "MBAVU", "KMRK", "EDHL"]
    candidates = []
    
    for ticker in random.sample(tickers, 6):
        if regime == "RISK_ON":
            change = round(random.uniform(8, 42), 1)
            score = round(random.uniform(7.5, 9.8), 1)
        else:
            change = round(random.uniform(3, 18), 1)
            score = round(random.uniform(5.5, 8.2), 1)
        
        price = round(random.uniform(3.5, 18.5), 2)
        volume = random.randint(800000, 8500000)
        
        if score >= 9.0:
            grade = "A+"
        elif score >= 8.0:
            grade = "A"
        elif score >= 7.0:
            grade = "B+"
        elif score >= 6.0:
            grade = "B"
        else:
            grade = "C"
        
        risk = "HIGH" if score >= 8.0 else ("MEDIUM" if score >= 6.5 else "LOW")
        stage = random.choice(["EARLY", "DEVELOPING", "EXTENDED"])
        
        candidates.append({
            "ticker": ticker,
            "price": price,
            "change_pct": change,
            "volume": volume,
            "setup_grade": grade,
            "risk_level": risk,
            "opportunity_score": score,
            "movement_stage": stage,
            "catalyst": random.choice([
                "Possível short squeeze", 
                "Contrato relevante anunciado",
                "Balanco forte + guidance elevado",
                "Catalisador setorial forte"
            ]),
            "red_flags": random.choice([
                "Float baixo - alta volatilidade",
                "Liquidez moderada",
                "Volume ainda subindo",
                "Nenhum red flag relevante"
            ]),
            "liquidity_score": random.randint(4, 9),
            "comment": "Setup gerado de forma agressiva"
        })
    
    candidates.sort(key=lambda x: x["opportunity_score"], reverse=True)
    return candidates

# ==================== ROTAS DA API ====================
@app.get("/api/v1/scan")
def scan(mode: str = Query("auto"), preferred_ai: str = Query("grok"), regime: str = Query("RISK_ON")):
    candidates = generate_aggressive_candidates(regime=regime)
    data = {
        "timestamp": datetime.now().isoformat(),
        "market_regime": regime,
        "mode": mode,
        "preferred_ai": preferred_ai,
        "total_candidates": len(candidates),
        "candidates": candidates
    }
    return Response(
        content=json.dumps(data, indent=2, ensure_ascii=False),
        media_type="application/json"
    )

@app.get("/api/v1/status")
def status():
    return {"status": "online", "service": "Stock Scanner AI", "timestamp": datetime.now().isoformat()}

# ==================== DASHBOARD HTML BONITO ====================
@app.get("/", response_class=HTMLResponse)
def dashboard():
    html = """
<!DOCTYPE html>
<html lang="pt">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Scanner • Gap + Momentum</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        .card { transition: all 0.2s ease; }
        .card:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1); }
        .grade-A\\+ { background-color: #15803d; color: white; }
        .grade-A { background-color: #16a34a; color: white; }
        .grade-B\\+ { background-color: #ca8a04; color: white; }
        .grade-B { background-color: #eab308; color: #111827; }
        .grade-C { background-color: #ea580c; color: white; }
        .risk-HIGH { border-left: 6px solid #dc2626; }
        .risk-MEDIUM { border-left: 6px solid #d97706; }
        .risk-LOW { border-left: 6px solid #16a34a; }
        .change-positive { color: #16a34a; font-weight: 700; }
        .change-negative { color: #dc2626; font-weight: 700; }
    </style>
</head>
<body class="bg-zinc-950 text-zinc-200">
    <div class="max-w-7xl mx-auto p-4 md:p-8">
        <!-- Header -->
        <div class="flex items-center justify-between mb-8">
            <div>
                <h1 class="text-4xl font-bold tracking-tight">Scanner Gap + Momentum</h1>
                <p class="text-zinc-400 mt-1">Lucas • Atualizado em tempo real</p>
            </div>
            <div class="flex items-center gap-3">
                <button onclick="loadData()" 
                        class="flex items-center gap-2 px-5 py-2.5 bg-white text-zinc-900 rounded-2xl font-semibold hover:bg-zinc-100 transition">
                    <i class="fa-solid fa-sync"></i>
                    <span>Atualizar</span>
                </button>
            </div>
        </div>

        <!-- Market Regime -->
        <div id="regime-bar" class="mb-6 px-5 py-3 rounded-3xl bg-zinc-900 border border-zinc-800 flex items-center justify-between">
            <div class="flex items-center gap-3">
                <span class="text-sm text-zinc-400">Market Regime:</span>
                <span id="regime-text" class="font-bold text-lg px-4 py-1 rounded-2xl bg-emerald-500 text-white">RISK_ON</span>
            </div>
            <div class="text-xs text-zinc-500" id="timestamp"></div>
        </div>

        <!-- Cards Grid -->
        <div id="cards-container" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <!-- Cards serão injetados via JS -->
        </div>
        
        <div class="mt-8 text-center text-xs text-zinc-500">
            Dados gerados para fins de teste • Use com responsabilidade
        </div>
    </div>

    <script>
        function getGradeClass(grade) {
            if (grade === "A+") return "grade-A+";
            if (grade === "A") return "grade-A";
            if (grade === "B+") return "grade-B+";
            if (grade === "B") return "grade-B";
            return "grade-C";
        }

        function createCard(stock) {
            const changeColor = stock.change_pct >= 0 ? 'change-positive' : 'change-negative';
            const riskBorder = `risk-${stock.risk_level}`;
            
            return `
                <div class="card bg-zinc-900 border border-zinc-800 rounded-3xl p-5 ${riskBorder}">
                    <div class="flex justify-between items-start mb-4">
                        <div>
                            <div class="text-3xl font-bold tracking-tighter">${stock.ticker}</div>
                            <div class="text-2xl font-semibold mt-0.5 ${changeColor}">
                                ${stock.change_pct >= 0 ? '+' : ''}${stock.change_pct}%
                            </div>
                        </div>
                        <div class="text-right">
                            <div class="text-xs text-zinc-400">Score</div>
                            <div class="text-3xl font-bold text-white">${stock.opportunity_score}</div>
                        </div>
                    </div>

                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <span class="px-4 py-1.5 rounded-2xl text-sm font-bold ${getGradeClass(stock.setup_grade)}">
                                ${stock.setup_grade}
                            </span>
                        </div>
                        <div class="text-xs px-3 py-1 rounded-2xl bg-zinc-800 text-zinc-300">
                            ${stock.risk_level} RISK
                        </div>
                    </div>

                    <div class="space-y-2 text-sm">
                        <div class="flex justify-between">
                            <span class="text-zinc-400">Preço</span>
                            <span class="font-medium">$${stock.price}</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-zinc-400">Volume</span>
                            <span class="font-medium">${(stock.volume / 1000000).toFixed(1)}M</span>
                        </div>
                        <div class="flex justify-between">
                            <span class="text-zinc-400">Estágio</span>
                            <span class="font-medium">${stock.movement_stage}</span>
                        </div>
                    </div>

                    <div class="mt-4 pt-4 border-t border-zinc-800">
                        <div class="text-xs text-emerald-400 font-medium mb-1">CATALYST</div>
                        <div class="text-sm">${stock.catalyst}</div>
                    </div>

                    <div class="mt-3">
                        <div class="text-xs text-red-400 font-medium mb-1">RED FLAGS</div>
                        <div class="text-sm text-zinc-300">${stock.red_flags}</div>
                    </div>

                    <div class="mt-4 text-[10px] text-zinc-500">
                        Liquidity: ${stock.liquidity_score}/10
                    </div>
                </div>
            `;
        }

        async function loadData() {
            const container = document.getElementById('cards-container');
            container.innerHTML = `<div class="col-span-full text-center py-12 text-zinc-400">Carregando setups...</div>`;
            
            try {
                const res = await fetch('/api/v1/scan?regime=RISK_ON');
                const data = await res.json();
                
                document.getElementById('regime-text').innerText = data.market_regime;
                document.getElementById('timestamp').innerText = new Date(data.timestamp).toLocaleTimeString('pt-BR');
                
                container.innerHTML = data.candidates.map(createCard).join('');
            } catch (e) {
                container.innerHTML = `<div class="col-span-full text-center py-12 text-red-400">Erro ao carregar dados</div>`;
            }
        }

        // Carrega automaticamente
        window.onload = () => {
            loadData();
            // Auto refresh a cada 90 segundos
            setInterval(loadData, 90000);
        };
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

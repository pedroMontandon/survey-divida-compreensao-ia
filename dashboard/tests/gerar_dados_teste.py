"""Gera um CSV FICTÍCIO no formato da exportação do Google Forms.

Serve SOMENTE para testar o dashboard antes de a coleta começar e para ensaiar
a apresentação. O arquivo leva uma coluna "[TESTE]" e o dashboard mostra um
aviso vermelho sempre que ela estiver presente. Nunca misture estas linhas com
as respostas reais.

Uso:  python tests/gerar_dados_teste.py  ->  tests/DADOS_FICTICIOS_teste.csv
"""

import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import questionario as Q  # noqa: E402

TITULOS = {
    "CONS": "[CONS] Você concorda em participar?",
    "T1": "[T1] Você trabalha atualmente desenvolvendo software (incluindo estágio)?",
    "T2": "[T2] Nos últimos 3 meses, você usou assistentes de IA (ex.: Copilot, ChatGPT, Claude, Cursor) em tarefas de código no trabalho?",
}
for cod in Q.OBRIGATORIOS + ["A1"]:
    TITULOS.setdefault(cod, f"[{cod}] {Q.ROTULOS.get(cod, cod)}")
ORDEM = ["CONS", "T1", "T2", "P1", "P2", "P3", "P4", "P5", "P6", "P7", "U1", "U2", "U3", "U4",
         "G1", "G2", "DC1", "DC2", "DC3", "ATT1", "DC4", "DC5", "CP1", "CP2", "CP3", "CP4",
         "PV1", "PV2", "PV3", "A1"]


def likert(rng, media, k=5):
    return int(np.clip(np.rint(rng.normal(media, 0.9)), 1, k))


def resposta_valida(rng):
    r = {"CONS": Q.CONSENTIMENTO_SIM, "T1": "Sim", "T2": "Sim"}
    exp = rng.choice(5, p=[0.12, 0.30, 0.28, 0.18, 0.12])
    r["P1"] = Q.OPCOES["P1"][exp]
    r["P2"] = Q.OPCOES["P2"][min(5, [0, 1, 2, 3, 4][exp] if rng.random() > 0.2 else rng.integers(0, 6))]
    r["P3"] = rng.choice(Q.OPCOES["P3"])
    r["P4"] = Q.OPCOES["P4"][min(4, max(0, exp - rng.integers(0, 2)))]
    r["P5"] = rng.choice(Q.OPCOES["P5"], p=[0.3, 0.15, 0.2, 0.15, 0.1, 0.05, 0.05])
    r["P6"] = rng.choice(Q.OPCOES["P6"], p=[0.55, 0.3, 0.15])
    r["P7"] = rng.choice(Q.OPCOES["P7"], p=[0.4, 0.3, 0.1, 0.15, 0.05])
    uso = rng.choice(5, p=[0.15, 0.25, 0.25, 0.2, 0.15])
    r["U1"] = Q.OPCOES["U1"][min(3, max(0, uso - rng.integers(0, 2)))]
    r["U2"] = Q.OPCOES["U2"][uso]
    r["U3"] = Q.OPCOES["U3"][min(2, uso // 2 + rng.integers(0, 2))]
    r["U4"] = ", ".join(sorted(set(rng.choice(Q.OPCOES["U4"], size=rng.integers(1, 4)))))
    pv = np.clip(rng.normal(3.6 - 0.25 * (uso - 2), 0.8), 1, 5)
    dc = np.clip(rng.normal(2.4 + 0.35 * (uso - 2) - 0.15 * (exp - 2) - 0.3 * (pv - 3.5), 0.7), 1, 5)
    cp = np.clip(rng.normal(3.4 + 0.15 * (uso - 2), 0.7), 1, 5)
    r["G1"] = Q.MUDANCA[likert(rng, 3.4 - 0.6 * (dc - 2.5)) - 1]
    r["G2"] = Q.MUDANCA[likert(rng, 3.0 + 0.6 * (cp - 3)) - 1]
    for i in ("DC1", "DC2", "DC4", "DC5"):
        r[i] = Q.LIKERT[likert(rng, dc) - 1]
    r["DC3"] = Q.LIKERT[likert(rng, 6 - dc) - 1]
    r["ATT1"] = Q.LIKERT[0]
    for i in ("CP1", "CP2", "CP3", "CP4"):
        r[i] = Q.LIKERT[likert(rng, cp) - 1]
    r["PV1"] = Q.FREQUENCIA[likert(rng, pv) - 1]
    r["PV2"] = Q.FREQUENCIA[likert(rng, pv) - 1]
    r["PV3"] = Q.FREQUENCIA[likert(rng, 6 - pv) - 1]
    r["A1"] = "" if rng.random() < 0.6 else "Texto fictício de teste."
    return r


def main(n=130, semente=7):
    rng = np.random.default_rng(semente)
    linhas = []
    inicio = datetime.combine(Q.DATA_INICIO_COLETA, datetime.min.time())
    for _ in range(3):  # pré-teste
        r = resposta_valida(rng)
        r["_t"] = inicio - timedelta(days=3, hours=int(rng.integers(1, 20)))
        linhas.append(r)
    for i in range(n):
        r = resposta_valida(rng)
        u = rng.random()
        if u < 0.03:
            r = {"CONS": "Não concordo"}
        elif u < 0.07:
            r = {"CONS": Q.CONSENTIMENTO_SIM, "T1": "Sim", "T2": "Não"}
        elif u < 0.09:
            r = {"CONS": Q.CONSENTIMENTO_SIM, "T1": "Não"}
        elif u < 0.13:
            r["ATT1"] = Q.LIKERT[3]
        elif u < 0.15:
            for k in Q.ITENS_LINHA_RETA:
                r[k] = (Q.LIKERT if k[:2] in ("DC", "CP") else Q.FREQUENCIA)[3]
        r["_t"] = inicio + timedelta(minutes=int(rng.integers(0, 21 * 24 * 60)))
        linhas.append(r)
    linhas.append(dict(linhas[10], _t=linhas[10]["_t"] + timedelta(minutes=2)))  # duplicata
    linhas.sort(key=lambda r: r["_t"])

    destino = Path(__file__).with_name("DADOS_FICTICIOS_teste.csv")
    with destino.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Carimbo de data/hora"] + [TITULOS[c] for c in ORDEM]
                   + ["[TESTE] Dados fictícios — não usar como resultado"])
        for r in linhas:
            w.writerow([r["_t"].strftime("%d/%m/%Y %H:%M:%S")] + [r.get(c, "") for c in ORDEM]
                       + ["FICTÍCIO"])
    print(f"{len(linhas)} linhas fictícias -> {destino}")


if __name__ == "__main__":
    main()

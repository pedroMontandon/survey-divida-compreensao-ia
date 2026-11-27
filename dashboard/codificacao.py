"""Codificação da pergunta aberta A1: planilhas dos codificadores, kappa de Cohen e arquivo final.

Uso (dentro de dashboard/):

    python codificacao.py preparar "<exportação do Forms (.csv ou .xlsx)>"
        Cria dados/codificador_1.xlsx e dados/codificador_2.xlsx com as respostas A1 válidas.
        Cada integrante preenche só a sua planilha (1 = o código se aplica).

    python codificacao.py kappa
        Calcula o kappa de Cohen nas primeiras 20 respostas (protocolo), por código e geral,
        e cria dados/consenso.xlsx já preenchido onde houve concordância. Aplica a regra do grupo
        (OUTRO contra um código específico -> vale o código específico) e lista as demais
        divergências na aba 'divergencias'. Não sobrescreve um consenso existente sem --refazer.

    python codificacao.py final
        Lê dados/consenso.xlsx (divergências resolvidas pelo grupo) e grava codificacao_abertas.csv
        (colunas ID, codigo), que o dashboard usa. Esse arquivo não contém os textos.

As planilhas ficam em dados/, que o .gitignore mantém fora do repositório (contêm os textos).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

import analise as A

BASE = Path(__file__).parent
DADOS = BASE / "dados"
COD = [BASE / "dados" / "codificador_1.xlsx", BASE / "dados" / "codificador_2.xlsx"]
CONSENSO = DADOS / "consenso.xlsx"
SAIDA = BASE / "codificacao_abertas.csv"
CODIGOS = ["PERDA_COMPREENSAO", "GANHO_CODIGO", "PRODUTO_DOMINIO", "DEPENDENCIA",
           "VERIFICACAO", "PAPEL_SATISFACAO", "QUALIDADE_EQUIPE", "OUTRO"]
N_KAPPA = 20   # protocolo: kappa nas primeiras 20 respostas


def preparar(exportacao: str) -> None:
    df, _ = A.mapear_colunas(A.ler_exportacao(exportacao))
    df = A.limpar(df)
    texto = df["A1"].fillna("").astype(str).str.strip()
    abertas = df.loc[df["VALIDA"] & (texto != ""), ["ID"]].assign(resposta=texto)
    base = abertas.assign(**{c: "" for c in CODIGOS}, observacao="")
    DADOS.mkdir(exist_ok=True)
    for caminho in COD:
        if caminho.exists():
            sys.exit(f"{caminho.name} já existe; apague-o se quiser recriar.")
        base.to_excel(caminho, index=False)
    print(f"{len(base)} respostas -> {COD[0].name} e {COD[1].name}")


def _ler(caminho: Path) -> pd.DataFrame:
    df = pd.read_excel(caminho, dtype=str).fillna("")
    for c in CODIGOS:
        v = df[c].str.strip()
        invalidos = sorted(set(v) - {"", "0", "1"})
        if invalidos:
            sys.exit(f"{caminho.name}, coluna {c}: use só 1 ou vazio (encontrei {invalidos}).")
        df[c] = (v == "1").astype(int)
    return df.set_index("ID")


def _kappa(a: pd.Series, b: pd.Series) -> float:
    po = (a == b).mean()
    pe = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def kappa() -> None:
    c1, c2 = (_ler(p) for p in COD)
    if list(c1.index) != list(c2.index):
        sys.exit("As duas planilhas precisam ter os mesmos IDs, na mesma ordem.")
    vazias = [i for i in c1.index if c1.loc[i, CODIGOS].sum() == 0 or c2.loc[i, CODIGOS].sum() == 0]
    if vazias:
        sys.exit(f"Respostas sem nenhum código marcado: {', '.join(vazias)}.")
    ids = list(c1.index[:N_KAPPA])
    linhas = []
    for c in CODIGOS:
        a, b = c1.loc[ids, c], c2.loc[ids, c]
        linhas.append({"código": c, "codificador 1": int(a.sum()), "codificador 2": int(b.sum()),
                       "concordância": f"{(a == b).mean():.0%}", "kappa": round(_kappa(a, b), 2)})
    geral = _kappa(c1.loc[ids, CODIGOS].stack(), c2.loc[ids, CODIGOS].stack())
    print(f"Kappa nas primeiras {len(ids)} respostas ({ids[0]} a {ids[-1]}):")
    print(pd.DataFrame(linhas).to_string(index=False))
    print(f"\nKappa geral (todas as decisões código × resposta): {geral:.2f}")
    print("Referência (Landis e Koch): < 0,40 fraca; 0,41–0,60 moderada; 0,61–0,80 substancial; > 0,80 quase perfeita.")

    if CONSENSO.exists() and "--refazer" not in sys.argv:
        print(f"\n{CONSENSO.name} já existe e não foi alterado (pode conter decisões do grupo). "
              "Para recriá-lo do zero, rode 'python codificacao.py kappa --refazer'.")
        return

    consenso = c1[["resposta"]].copy()
    for c in CODIGOS:
        consenso[c] = c1[c].where(c1[c] == c2[c]).map({1: "1", 0: ""}).fillna("DIVERGE")

    # Regra de consenso do grupo: OUTRO contra um código específico -> vale o código específico
    automaticas = []
    for i in consenso.index[consenso["OUTRO"] == "DIVERGE"]:
        marcou_outro, outro_lado = (c1, c2) if c1.loc[i, "OUTRO"] == 1 else (c2, c1)
        especificos = [c for c in CODIGOS[:-1]
                       if consenso.loc[i, c] == "DIVERGE" and outro_lado.loc[i, c] == 1
                       and marcou_outro.loc[i, c] == 0]
        if especificos:
            consenso.loc[i, "OUTRO"] = ""
            for c in especificos:
                consenso.loc[i, c] = "1"
            automaticas.append((i, especificos))

    linhas = []
    for i in consenso.index:
        for c in CODIGOS:
            if consenso.loc[i, c] == "DIVERGE":
                linhas.append({"ID": i, "código": c, "codificador 1": int(c1.loc[i, c]),
                               "codificador 2": int(c2.loc[i, c]), "resposta": c1.loc[i, "resposta"],
                               "observação 1": c1.loc[i, "observacao"],
                               "observação 2": c2.loc[i, "observacao"]})
    consenso["observacao"] = ""
    with pd.ExcelWriter(CONSENSO) as xl:
        consenso.reset_index().to_excel(xl, sheet_name="consenso", index=False)
        pd.DataFrame(linhas).to_excel(xl, sheet_name="divergencias", index=False)

    print("\nRegra OUTRO × código específico aplicada em:")
    for i, cs in automaticas:
        print(f"  {i}: OUTRO removido, vale {', '.join(cs)}")
    print(f"\n{len(linhas)} divergências para o grupo decidir (DIVERGE na aba 'consenso'; "
          f"detalhes na aba 'divergencias' de {CONSENSO.name}):")
    for r in linhas:
        print(f"  {r['ID']}: {r['código']} (cod. 1 = {r['codificador 1']}, cod. 2 = {r['codificador 2']})")


def final() -> None:
    if not CONSENSO.exists():
        sys.exit(f"{CONSENSO.name} não existe: rode primeiro 'python codificacao.py kappa'.")
    df = pd.read_excel(CONSENSO, sheet_name="consenso", dtype=str).fillna("")
    pendentes = [(r.ID, c) for r in df.itertuples() for c in CODIGOS if getattr(r, c).strip() == "DIVERGE"]
    if pendentes:
        sys.exit(f"Ainda há {len(pendentes)} divergências sem consenso, por exemplo {pendentes[0]}.")
    linhas = [(r.ID, c) for r in df.itertuples() for c in CODIGOS if getattr(r, c).strip() == "1"]
    pd.DataFrame(linhas, columns=["ID", "codigo"]).to_csv(SAIDA, index=False)
    print(f"{len(linhas)} códigos em {df['ID'].nunique()} respostas -> {SAIDA.name}")


if __name__ == "__main__":
    comando = sys.argv[1] if len(sys.argv) > 1 else ""
    if comando == "preparar" and len(sys.argv) == 3:
        preparar(sys.argv[2])
    elif comando == "kappa":
        kappa()
    elif comando == "final":
        final()
    else:
        sys.exit(__doc__)

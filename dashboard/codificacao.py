"""Codificação da pergunta aberta A1: planilhas dos codificadores, kappa de Cohen e arquivo final.

Uso (dentro de dashboard/):

    python codificacao.py preparar "<exportação do Forms (.csv ou .xlsx)>"
        Cria dados/codificador_1.xlsx e dados/codificador_2.xlsx com as respostas A1 válidas.
        Cada integrante preenche só a sua planilha (1 = o código se aplica).

    python codificacao.py kappa
        Calcula o kappa de Cohen nas primeiras 20 respostas (protocolo), por código e geral,
        lista as divergências e cria dados/consenso.xlsx já preenchido onde houve concordância.

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

    consenso = c1[["resposta"]].copy()
    divergencias = []
    for c in CODIGOS:
        iguais = c1[c] == c2[c]
        consenso[c] = c1[c].where(iguais).map({1: "1", 0: ""}).fillna("DIVERGE")
        divergencias += [(i, c) for i in c1.index[~iguais]]
    consenso["observacao"] = ""
    consenso.reset_index().to_excel(CONSENSO, index=False)
    print(f"\n{len(divergencias)} divergências (marcadas como DIVERGE em {CONSENSO.name}):")
    for i, c in divergencias:
        print(f"  {i}: {c}")


def final() -> None:
    if not CONSENSO.exists():
        sys.exit(f"{CONSENSO.name} não existe: rode primeiro 'python codificacao.py kappa'.")
    df = pd.read_excel(CONSENSO, dtype=str).fillna("")
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

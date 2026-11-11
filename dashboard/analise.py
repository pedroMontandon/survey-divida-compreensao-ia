"""Leitura dos dados brutos, limpeza, índices e testes estatísticos.

Funções puras (sem Streamlit) para que possam ser testadas e conferidas
fora do dashboard.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from scipy import stats

import questionario as Q

COLUNAS_DATA = ["carimbo de data/hora", "timestamp", "data/hora", "carimbo de data e hora"]
MARCADOR_TESTE = "[TESTE]"


# =============================================================== leitura
def _norm(texto) -> str:
    if texto is None or (isinstance(texto, float) and np.isnan(texto)):
        return ""
    t = unicodedata.normalize("NFC", str(texto)).strip()
    return re.sub(r"\s+", " ", t)


def ler_exportacao(origem) -> pd.DataFrame:
    """Lê o CSV/XLSX exportado do Google Forms (ou do Google Sheets)."""
    nome = getattr(origem, "name", str(origem)).lower()
    if nome.endswith((".xlsx", ".xls")):
        return pd.read_excel(origem, dtype=str)
    return pd.read_csv(origem, dtype=str, keep_default_na=False, encoding="utf-8-sig")


def mapear_colunas(bruto: pd.DataFrame) -> tuple[pd.DataFrame, bool]:
    """Renomeia colunas para os códigos [XX] dos títulos. Retorna (df, eh_teste)."""
    renomear, coluna_data = {}, None
    for col in bruto.columns:
        m = re.match(r"^\s*\[([A-Z]+[0-9]*)\]", str(col))
        if m:
            renomear[col] = m.group(1)
        elif str(col).strip().lower() in COLUNAS_DATA and coluna_data is None:
            coluna_data = col
    if coluna_data is None:
        coluna_data = bruto.columns[0]
    renomear[coluna_data] = "DATA_HORA"
    df = bruto.rename(columns=renomear)
    eh_teste = any(MARCADOR_TESTE in str(c) for c in bruto.columns)
    manter = ["DATA_HORA"] + [c for c in renomear.values() if c != "DATA_HORA"]
    df = df[[c for c in manter if c in df.columns]].copy()
    for c in df.columns:
        if c != "DATA_HORA":
            df[c] = df[c].map(_norm)
    df["DATA_HORA"] = _parse_datas(df["DATA_HORA"])
    df = df.sort_values("DATA_HORA", kind="stable").reset_index(drop=True)
    df.insert(0, "ID", [f"R{i + 1:03d}" for i in range(len(df))])
    return df, eh_teste


def _parse_datas(serie: pd.Series) -> pd.Series:
    s = serie.astype(str).str.strip()
    br = pd.to_datetime(s, format="%d/%m/%Y %H:%M:%S", errors="coerce")
    resto = br.isna()
    if resto.any():
        br[resto] = pd.to_datetime(s[resto], errors="coerce", dayfirst=True)
    return br


def colunas_faltantes(df: pd.DataFrame) -> list[str]:
    esperadas = ["CONS", "T1", "T2"] + Q.OBRIGATORIOS
    return [c for c in esperadas if c not in df.columns]


# =============================================================== escores
def escore(df: pd.DataFrame, codigo: str) -> pd.Series:
    """Converte o texto da opção na posição 1..k (NaN se ausente ou fora da ordem)."""
    if codigo not in df.columns:
        return pd.Series(np.nan, index=df.index)
    mapa = {_norm(op).casefold(): i + 1 for i, op in enumerate(Q.OPCOES[codigo])
            if op != Q.NAO_ORDINAL.get(codigo)}
    return df[codigo].map(lambda v: mapa.get(_norm(v).casefold(), np.nan)).astype(float)


def _eq(serie: pd.Series, valor: str) -> pd.Series:
    return serie.map(lambda v: _norm(v).casefold() == valor.casefold())


# =============================================================== limpeza
def limpar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica as regras D0–D6 na ordem do protocolo. Adiciona MOTIVO e VALIDA."""
    df = df.copy()
    for c in ["CONS", "T1", "T2"] + Q.OBRIGATORIOS:
        if c not in df.columns:
            df[c] = ""
    motivo = pd.Series("", index=df.index, dtype=object)

    def marcar(cond, codigo):
        sel = cond & (motivo == "")
        motivo[sel] = codigo

    inicio = pd.Timestamp(Q.DATA_INICIO_COLETA)
    marcar(df["DATA_HORA"].notna() & (df["DATA_HORA"] < inicio), "D0")
    marcar(~_eq(df["CONS"], Q.CONSENTIMENTO_SIM), "D1")
    marcar(_eq(df["T1"], "Não") | _eq(df["T2"], "Não"), "D2")
    att = escore(df, "ATT1")
    marcar(att.notna() & (att != 1), "D3")
    escores = pd.DataFrame({c: escore(df, c) for c in Q.ITENS_LINHA_RETA})
    completos = escores.notna().all(axis=1)
    marcar(completos & (escores.nunique(axis=1) == 1), "D4")
    conteudo = [c for c in df.columns if c not in ("ID", "DATA_HORA")]
    marcar(df.duplicated(subset=conteudo, keep="first"), "D5")
    obrig = df[Q.OBRIGATORIOS].apply(lambda col: col.map(lambda v: _norm(v) == ""))
    marcar(obrig.any(axis=1), "D6")

    df["MOTIVO"] = motivo
    df["VALIDA"] = motivo == ""
    return df


# =============================================================== variáveis derivadas
def derivar(df: pd.DataFrame) -> pd.DataFrame:
    """Escores numéricos, índices dos construtos e agrupamentos pré-registrados."""
    df = df.copy()
    for c in Q.ORDINAIS:
        df[f"s_{c}"] = escore(df, c)
    for chave, cfg in Q.CONSTRUTOS.items():
        cols = []
        for item in cfg["itens"]:
            s = df[f"s_{item}"]
            df[f"r_{item}"] = 6 - s if item in cfg["invertidos"] else s
            cols.append(f"r_{item}")
        df[chave] = df[cols].mean(axis=1, skipna=False)
    df["FAIXA_EXP"] = df["P1"].map(Q.FAIXAS_EXPERIENCIA)
    df["G2_CAT"] = pd.cut(df["s_G2"], bins=[0, 2, 3, 5],
                          labels=["Diminuiu", "Não mudou", "Aumentou"]).astype(object)
    df["REVIEW_SEMPRE"] = np.where(_eq(df["P6"], "Sim, sempre"), "Code review sempre",
                                   "Nem sempre")
    return df


def alpha_cronbach(itens: pd.DataFrame) -> dict:
    x = itens.dropna()
    k, n = x.shape[1], len(x)
    if n < 3 or k < 2:
        return {"alfa": np.nan, "n": n, "itens": pd.DataFrame()}
    def _alfa(m):
        kk = m.shape[1]
        total = m.sum(axis=1).var(ddof=1)
        return np.nan if total == 0 else kk / (kk - 1) * (1 - m.var(ddof=1).sum() / total)
    linhas = []
    for c in x.columns:
        resto = x.drop(columns=c)
        r_it = np.corrcoef(x[c], resto.sum(axis=1))[0, 1] if x[c].std() > 0 else np.nan
        linhas.append({"Item": c.replace("r_", ""), "Média": x[c].mean(),
                       "Correlação item-total corrigida": r_it,
                       "Alfa sem o item": _alfa(resto) if resto.shape[1] > 1 else np.nan})
    return {"alfa": _alfa(x), "n": n, "itens": pd.DataFrame(linhas)}


def classificar_alfa(a: float) -> str:
    if np.isnan(a):
        return "não calculável"
    if a >= 0.70:
        return "adequado (≥ 0,70)"
    if a >= 0.60:
        return "aceitável com ressalva (0,60–0,70)"
    return "insuficiente (< 0,60): analisar itens separadamente"


# =============================================================== estatística
def margem_erro(p: float, n: int, z: float = 1.96) -> float:
    return z * np.sqrt(p * (1 - p) / n) if n > 0 else np.nan


def proporcao(cond: pd.Series) -> dict:
    cond = cond.dropna().astype(bool)
    n = len(cond)
    p = cond.mean() if n else np.nan
    return {"p": p, "n": n, "k": int(cond.sum()), "me": margem_erro(p, n) if n else np.nan}


def holm(pvalores: list[float]) -> list[float]:
    p = np.asarray(pvalores, dtype=float)
    ok = ~np.isnan(p)
    ajust = np.full_like(p, np.nan)
    idx = np.where(ok)[0]
    if len(idx) == 0:
        return ajust.tolist()
    ordem = idx[np.argsort(p[idx])]
    m, corrente = len(ordem), 0.0
    for i, j in enumerate(ordem):
        corrente = max(corrente, min(1.0, (m - i) * p[j]))
        ajust[j] = corrente
    return ajust.tolist()


def rotulo_efeito(valor: float, cortes=(0.1, 0.3, 0.5)) -> str:
    if valor is None or np.isnan(valor):
        return "—"
    v = abs(valor)
    if v < cortes[0]:
        return "desprezível"
    if v < cortes[1]:
        return "pequeno"
    if v < cortes[2]:
        return "médio"
    return "grande"


@dataclass
class Resultado:
    id: str
    hipotese: str
    teste: str
    n: int
    estatistica: str
    p: float
    efeito_nome: str
    efeito: float
    efeito_rotulo: str
    familia: str
    p_holm: float = np.nan
    detalhe: str = ""
    extra: dict = field(default_factory=dict)


def wilcoxon_neutro(x: pd.Series, neutro: float = 3) -> dict | None:
    d = (x.dropna() - neutro)
    nz = d[d != 0]
    if len(nz) < 6:
        return None
    r = stats.rankdata(np.abs(nz))
    w_mais, w_menos = r[nz > 0].sum(), r[nz < 0].sum()
    res = stats.wilcoxon(nz, zero_method="wilcox", alternative="two-sided")
    rrb = (w_mais - w_menos) / (w_mais + w_menos)
    return {"W": res.statistic, "p": res.pvalue, "rrb": rrb, "n": len(d),
            "n_sem_empate": len(nz), "mediana": float(x.dropna().median())}


def spearman(x: pd.Series, y: pd.Series) -> dict | None:
    dados = pd.concat([x, y], axis=1).dropna()
    n = len(dados)
    if n < 5 or dados.iloc[:, 0].nunique() < 2 or dados.iloc[:, 1].nunique() < 2:
        return None
    rho, p = stats.spearmanr(dados.iloc[:, 0], dados.iloc[:, 1])
    if n > 3:
        se = np.sqrt(1.06 / (n - 3))
        z = np.arctanh(np.clip(rho, -0.9999, 0.9999))
        ic = (np.tanh(z - 1.96 * se), np.tanh(z + 1.96 * se))
    else:
        ic = (np.nan, np.nan)
    return {"rho": rho, "p": p, "n": n, "ic": ic}


def unir_grupos_pequenos(rotulos: pd.Series, ordem: list[str], minimo: int = 5):
    """Une grupos ordenados com n < minimo ao vizinho menor (regra pré-registrada)."""
    grupos = [[g] for g in ordem]
    def contagem(gs):
        return int(rotulos.isin(gs).sum())
    unidos = False
    while len(grupos) > 2:
        tamanhos = [contagem(g) for g in grupos]
        i = int(np.argmin(tamanhos))
        if tamanhos[i] >= minimo:
            break
        if i == 0:
            j = 1
        elif i == len(grupos) - 1:
            j = i - 1
        else:
            j = i - 1 if tamanhos[i - 1] <= tamanhos[i + 1] else i + 1
        a, b = sorted((i, j))
        grupos[a] = grupos[a] + grupos[b]
        del grupos[b]
        unidos = True
    mapa = {g: " + ".join(grp) for grp in grupos for g in grp}
    return rotulos.map(mapa), [" + ".join(g) for g in grupos], unidos


def kruskal_dunn(valores: pd.Series, grupos: pd.Series, ordem: list[str]) -> dict | None:
    dados = pd.DataFrame({"v": valores, "g": grupos}).dropna()
    ordem = [g for g in ordem if (dados["g"] == g).sum() > 0]
    amostras = [dados.loc[dados["g"] == g, "v"].values for g in ordem]
    if len(amostras) < 2 or any(len(a) < 2 for a in amostras):
        return None
    if dados["v"].nunique() < 2:
        return None
    H, p = stats.kruskal(*amostras)
    N = len(dados)
    eps2 = H / (N - 1)
    # Dunn com correção de empates
    rk = stats.rankdata(dados["v"])
    dados = dados.assign(rank=rk)
    _, t = np.unique(dados["v"], return_counts=True)
    corr = (t ** 3 - t).sum() / (12 * (N - 1))
    pares = []
    for i in range(len(ordem)):
        for j in range(i + 1, len(ordem)):
            gi, gj = ordem[i], ordem[j]
            ri = dados.loc[dados["g"] == gi, "rank"]
            rj = dados.loc[dados["g"] == gj, "rank"]
            se = np.sqrt((N * (N + 1) / 12 - corr) * (1 / len(ri) + 1 / len(rj)))
            z = (ri.mean() - rj.mean()) / se
            pares.append({"Comparação": f"{gi} × {gj}", "z": z,
                          "p": 2 * stats.norm.sf(abs(z))})
    pares = pd.DataFrame(pares)
    pares["p (Holm)"] = holm(pares["p"].tolist())
    return {"H": H, "p": p, "eps2": eps2, "n": N, "gl": len(ordem) - 1, "dunn": pares,
            "medianas": {g: float(np.median(a)) for g, a in zip(ordem, amostras)},
            "ns": {g: len(a) for g, a in zip(ordem, amostras)}}


def mann_whitney(valores: pd.Series, grupos: pd.Series, g1: str, g2: str) -> dict | None:
    a = valores[grupos == g1].dropna()
    b = valores[grupos == g2].dropna()
    if len(a) < 3 or len(b) < 3:
        return None
    res = stats.mannwhitneyu(a, b, alternative="two-sided")
    rrb = 2 * res.statistic / (len(a) * len(b)) - 1
    return {"U": res.statistic, "p": res.pvalue, "rrb": rrb, "n": len(a) + len(b),
            "n1": len(a), "n2": len(b), "med1": float(a.median()), "med2": float(b.median())}


def qui_quadrado(x: pd.Series, y: pd.Series, n_perm: int = 10_000, semente: int = 2026) -> dict | None:
    dados = pd.DataFrame({"x": x, "y": y}).dropna()
    tab = pd.crosstab(dados["x"], dados["y"])
    if tab.shape[0] < 2 or tab.shape[1] < 2:
        return None
    chi2, p, gl, esperado = stats.chi2_contingency(tab, correction=False)
    n = int(tab.values.sum())
    v = np.sqrt(chi2 / (n * (min(tab.shape) - 1)))
    frac_baixa = (esperado < 5).mean()
    metodo = "assintótico"
    if frac_baixa > 0.20:
        rng = np.random.default_rng(semente)
        xi = pd.Categorical(dados["x"]).codes.astype(np.int64)
        yi = pd.Categorical(dados["y"]).codes.astype(np.int64)
        r, c = int(xi.max()) + 1, int(yi.max()) + 1
        esp = np.outer(np.bincount(xi, minlength=r), np.bincount(yi, minlength=c)) / n
        perm = np.argsort(rng.random((n_perm, n)), axis=1)          # permutações de y
        celulas = xi[None, :] * c + yi[perm]                          # (n_perm, n)
        offs = (np.arange(n_perm) * r * c)[:, None]
        obs = np.bincount((celulas + offs).ravel(), minlength=n_perm * r * c).reshape(n_perm, r, c)
        chis = ((obs - esp) ** 2 / esp).sum(axis=(1, 2))
        p = (int((chis >= chi2 - 1e-9).sum()) + 1) / (n_perm + 1)
        metodo = f"permutação ({n_perm:,} reamostragens)".replace(",", ".")
    return {"chi2": chi2, "p": p, "gl": gl, "V": v, "n": n, "tabela": tab,
            "frac_esperado_baixo": frac_baixa, "metodo": metodo}


# =============================================================== hipóteses
def testar_hipoteses(df: pd.DataFrame) -> list[Resultado]:
    """Executa a família confirmatória (H1–H4b) e a exploratória (E1–E3)."""
    res: list[Resultado] = []

    def add_wilcoxon(id_, hip, col):
        r = wilcoxon_neutro(df[col])
        if r:
            res.append(Resultado(id_, hip, "Wilcoxon de uma amostra (vs. 3 = não mudou)", r["n"],
                                 f"W = {r['W']:.1f}", r["p"], "rank-bisserial pareada", r["rrb"],
                                 rotulo_efeito(r["rrb"]), "confirmatória",
                                 detalhe=f"Direção: predominam respostas de "
                                         f"{'aumento' if r['rrb'] > 0 else 'diminuição'} (efeito "
                                         f"{'positivo' if r['rrb'] > 0 else 'negativo'}). Mediana = "
                                         f"{r['mediana']:.1f}; {r['n'] - r['n_sem_empate']} respostas "
                                         f"'não mudou' ficam fora do teste.", extra=r))

    def add_spearman(id_, hip, x, y, familia="confirmatória"):
        r = spearman(df[x], df[y])
        if r:
            res.append(Resultado(id_, hip, "Correlação de Spearman", r["n"], f"ρ = {r['rho']:.3f}",
                                 r["p"], "ρ", r["rho"], rotulo_efeito(r["rho"]), familia,
                                 detalhe=f"IC 95% de ρ: [{r['ic'][0]:.2f}; {r['ic'][1]:.2f}]", extra=r))

    def add_kruskal(id_, hip, valor, grupo, ordem, familia):
        rot, ordem2, unidos = unir_grupos_pequenos(df[grupo], ordem, Q.MIN_SEGMENTO)
        r = kruskal_dunn(df[valor], rot, ordem2)
        if r:
            det = "grupos com n < 5 foram unidos ao vizinho (regra pré-registrada)" if unidos else ""
            res.append(Resultado(id_, hip, "Kruskal-Wallis + Dunn (Holm)", r["n"],
                                 f"H({r['gl']}) = {r['H']:.2f}", r["p"], "ε²", r["eps2"],
                                 rotulo_efeito(r["eps2"], (0.01, 0.08, 0.26)), familia,
                                 detalhe=det, extra=r))

    add_wilcoxon("H1", "QP1 — Conhecimento da base de código mudou desde o uso de IA (G1 ≠ 3)", "s_G1")
    add_spearman("H2", "QP2 — Intensidade de uso (U2) × dívida de compreensão (DC)", "s_U2", "DC")
    add_wilcoxon("H3a", "QP3 — Conhecimento do produto mudou desde o uso de IA (G2 ≠ 3)", "s_G2")
    add_spearman("H3b", "QP3 — Intensidade de uso (U2) × conhecimento do produto (CP)", "s_U2", "CP")
    add_kruskal("H4a", "QP4 — Dívida de compreensão por faixa de experiência", "DC", "FAIXA_EXP",
                Q.ORDEM_FAIXAS, "confirmatória")
    add_spearman("H4b", "QP4 — Práticas de verificação (PV) × dívida de compreensão (DC)", "PV", "DC")

    add_kruskal("E1", "Dívida de compreensão por forma de uso predominante (U3)", "DC", "U3",
                Q.OPCOES["U3"], "exploratória")
    r = qui_quadrado(df["U3"].replace("", np.nan), df["G2_CAT"])
    if r:
        res.append(Resultado("E2", "Avaliação do conhecimento do produto (G2) × forma de uso (U3)",
                             f"χ² de independência — p {r['metodo']}", r["n"],
                             f"χ²({r['gl']}) = {r['chi2']:.2f}", r["p"], "V de Cramér", r["V"],
                             rotulo_efeito(r["V"]), "exploratória",
                             detalhe=f"{r['frac_esperado_baixo']:.0%} das células com frequência esperada < 5",
                             extra=r))
    r = mann_whitney(df["DC"], df["REVIEW_SEMPRE"], "Code review sempre", "Nem sempre")
    if r:
        res.append(Resultado("E3", "Dívida de compreensão: code review obrigatório × não obrigatório",
                             "Mann-Whitney", r["n"], f"U = {r['U']:.1f}", r["p"], "rank-bisserial",
                             r["rrb"], rotulo_efeito(r["rrb"]), "exploratória",
                             detalhe=f"mediana DC: sempre = {r['med1']:.2f} (n={r['n1']}); "
                                     f"às vezes/não = {r['med2']:.2f} (n={r['n2']})", extra=r))

    for familia in ("confirmatória", "exploratória"):
        membros = [x for x in res if x.familia == familia]
        for x, pa in zip(membros, holm([x.p for x in membros])):
            x.p_holm = pa
    return res


def tabela_resultados(res: list[Resultado]) -> pd.DataFrame:
    return pd.DataFrame([{
        "ID": r.id, "Hipótese": r.hipotese, "Família": r.familia, "Teste": r.teste, "n": r.n,
        "Estatística": r.estatistica, "p": r.p, "p (Holm)": r.p_holm,
        "Efeito": f"{r.efeito_nome} = {r.efeito:.3f}", "Magnitude": r.efeito_rotulo,
        "Decisão (α = 0,05, Holm)": "Rejeita H₀" if r.p_holm < Q.ALFA else "Não rejeita H₀",
        "Observação": r.detalhe,
    } for r in res])


def formatar_p(p: float) -> str:
    if p is None or np.isnan(p):
        return "—"
    return "< 0,001" if p < 0.001 else f"{p:.3f}".replace(".", ",")

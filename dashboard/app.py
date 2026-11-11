"""Dashboard do survey "Dívida de compreensão no uso de IA".

Executar:  streamlit run app.py
Lê a exportação bruta do Google Forms (CSV/XLSX), aplica a limpeza pré-registrada
e recalcula todas as estatísticas a cada carga.
"""

from __future__ import annotations

import io
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

import analise as A
import questionario as Q

BASE = Path(__file__).parent
ARQ_PADRAO = BASE / "dados" / "respostas.csv"
ARQ_TESTE = BASE / "tests" / "DADOS_FICTICIOS_teste.csv"
ARQ_DESVIOS = BASE / "desvios.md"
ARQ_CODIFICACAO = BASE / "codificacao_abertas.csv"

# Paleta divergente (vermelho ↔ azul, meio cinza) e cores de série
DIVERGENTE = ["#c43c3c", "#ef9a96", "#bdbbb4", "#86b6ef", "#2a78d6"]
SERIE = ["#2a78d6", "#eb6834", "#1baf7a"]
COR_DESTAQUE = "#2a78d6"

st.set_page_config(page_title="Dívida de compreensão no uso de IA", page_icon="📊", layout="wide")


# =============================================================== dados
@st.cache_data(show_spinner=False)
def carregar(conteudo: bytes, nome: str):
    bruto = A.ler_exportacao(_Arquivo(conteudo, nome))
    df, eh_teste = A.mapear_colunas(bruto)
    faltantes = A.colunas_faltantes(df)
    df = A.limpar(df)
    df = A.derivar(df)
    return df, eh_teste, faltantes


class _Arquivo(io.BytesIO):
    def __init__(self, conteudo, nome):
        super().__init__(conteudo)
        self.name = nome


def obter_fonte():
    st.sidebar.header("Dados")
    enviado = st.sidebar.file_uploader("Exportação do Google Forms (CSV ou XLSX)",
                                       type=["csv", "xlsx"])
    if enviado is not None:
        return enviado.getvalue(), enviado.name, "arquivo enviado"
    if ARQ_PADRAO.exists():
        return ARQ_PADRAO.read_bytes(), ARQ_PADRAO.name, f"dados/{ARQ_PADRAO.name}"
    url = None
    try:
        url = st.secrets.get("CSV_URL")
    except Exception:
        url = None
    if url:
        import urllib.request
        with urllib.request.urlopen(url, timeout=20) as r:
            return r.read(), "remoto.csv", "planilha conectada (CSV_URL)"
    if ARQ_TESTE.exists() and st.sidebar.toggle("Usar dados FICTÍCIOS de teste", value=False):
        return ARQ_TESTE.read_bytes(), ARQ_TESTE.name, "dados fictícios de teste"
    return None, None, None


# =============================================================== gráficos
def layout(fig, altura=None, **kw):
    fig.update_layout(margin=dict(l=10, r=10, t=40, b=10), height=altura,
                      font=dict(size=13), hoverlabel=dict(font_size=13),
                      legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0), **kw)
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(128,128,128,0.18)", zeroline=False)
    return fig


def barras_divergentes(df: pd.DataFrame, itens: list[str], opcoes: list[str], titulo: str):
    linhas = []
    for item in itens:
        s = A.escore(df, item).dropna()
        n = len(s)
        if n == 0:
            continue
        pct = [(s == k).mean() * 100 for k in range(1, 6)]
        cont = [int((s == k).sum()) for k in range(1, 6)]
        linhas.append((f"{item} · {Q.ROTULOS.get(item, item)}", pct, cont, n))
    if not linhas:
        st.info("Sem respostas para estes itens.")
        return
    linhas = linhas[::-1]
    fig = go.Figure()
    for k in range(5):
        x, base, txt, hover = [], [], [], []
        for rot, pct, cont, n in linhas:
            esquerda = -(pct[0] + pct[1] + pct[2] / 2)
            inicio = esquerda + sum(pct[:k])
            x.append(pct[k]); base.append(inicio)
            txt.append(f"{pct[k]:.0f}%" if pct[k] >= 8 else "")
            hover.append(f"{opcoes[k]}: {cont[k]} de {n} ({pct[k]:.1f}%)")
        fig.add_trace(go.Bar(
            y=[l[0] for l in linhas], x=x, base=base, orientation="h", name=opcoes[k],
            marker=dict(color=DIVERGENTE[k], line=dict(width=1, color="rgba(255,255,255,0.9)")),
            text=txt, textposition="inside", insidetextanchor="middle",
            textfont=dict(color="#0b0b0b" if k in (1, 2, 3) else "#ffffff"),
            hovertext=hover, hoverinfo="text"))
    fig.add_vline(x=0, line_width=1, line_color="rgba(128,128,128,0.7)")
    fig.update_layout(barmode="overlay", bargap=0.35)
    st.markdown(f"**{titulo}**")
    fig.update_xaxes(ticksuffix="%", range=[-100, 100], title="← discordância / menor  ·  concordância / maior →")
    fig = layout(fig, altura=120 + 52 * len(linhas))
    fig.update_layout(margin=dict(t=10), legend=dict(y=1.0, yanchor="bottom"))
    st.plotly_chart(fig, width="stretch")


def barras_categorias(serie: pd.Series, titulo: str, ordem: list[str] | None = None, multi=False):
    s = serie.replace("", np.nan).dropna()
    if multi:
        s = s.str.split(", ").explode().str.strip()
    cont = s.value_counts()
    if ordem:
        extras = [c for c in cont.index if c not in ordem]
        cont = cont.reindex([o for o in ordem if o in cont.index] + extras)
    n = len(serie.replace("", np.nan).dropna())
    fig = go.Figure(go.Bar(
        y=cont.index[::-1], x=cont.values[::-1], orientation="h", marker_color=COR_DESTAQUE,
        text=[f"{v} ({v / n:.0%})" for v in cont.values[::-1]], textposition="outside",
        cliponaxis=False, hovertemplate="%{y}: %{x}<extra></extra>"))
    fig.update_layout(title=titulo)
    fig.update_xaxes(showticklabels=False, range=[0, cont.max() * 1.35 if len(cont) else 1])
    st.plotly_chart(layout(fig, altura=90 + 34 * len(cont)), width="stretch")


def caixas(df: pd.DataFrame, valor: str, grupo: str, ordem: list[str], titulo: str, eixo_y: str):
    fig = go.Figure()
    for g in ordem:
        v = df.loc[df[grupo] == g, valor].dropna()
        if len(v) == 0:
            continue
        fig.add_trace(go.Box(y=v, name=f"{g}<br>(n={len(v)})", boxpoints="all", jitter=0.45,
                             pointpos=0, marker=dict(size=7, opacity=0.55, color=COR_DESTAQUE),
                             line=dict(color="#184f95"), fillcolor="rgba(42,120,214,0.12)",
                             showlegend=False, hovertemplate="%{y:.2f}<extra></extra>"))
    fig.update_layout(title=titulo)
    fig.update_yaxes(title=eixo_y, range=[0.8, 5.2])
    st.plotly_chart(layout(fig, altura=380), width="stretch")


def dispersao(df, x, y, titulo, rotx, roty, ticks=None):
    d = df[[x, y]].dropna()
    rng = np.random.default_rng(1)
    fig = go.Figure(go.Scatter(
        x=d[x] + rng.uniform(-0.15, 0.15, len(d)), y=d[y] + rng.uniform(-0.05, 0.05, len(d)),
        mode="markers", marker=dict(size=9, opacity=0.55, color=COR_DESTAQUE,
                                    line=dict(width=1, color="white")),
        hovertemplate=f"{rotx}: %{{x:.1f}}<br>{roty}: %{{y:.2f}}<extra></extra>"))
    if ticks:
        fig.update_xaxes(tickvals=list(range(1, len(ticks) + 1)), ticktext=ticks)
    fig.update_layout(title=titulo)
    fig.update_xaxes(title=rotx)
    fig.update_yaxes(title=roty, range=[0.8, 5.2])
    st.plotly_chart(layout(fig, altura=380), width="stretch")


# =============================================================== blocos de texto
def cartao_teste(r: A.Resultado):
    decisao = "Rejeita H₀" if r.p_holm < Q.ALFA else "Não rejeita H₀"
    with st.container(border=True):
        st.markdown(f"**{r.id} — {r.hipotese}**  \n{r.teste} · _família {r.familia}_")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("p ajustado (Holm)", A.formatar_p(r.p_holm))
        c2.metric(f"Efeito: {r.efeito_nome}", f"{r.efeito:.2f}".replace(".", ","))
        c3.metric("n", r.n)
        c4.metric("Decisão (α = 0,05)", decisao)
        st.caption(f"{r.estatistica}; p bruto = {A.formatar_p(r.p)}; magnitude do efeito: "
                   f"{r.efeito_rotulo}. {r.detalhe}")


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%".replace(".", ",")


def texto_proporcao(rotulo: str, prop: dict):
    if prop["n"] == 0:
        return
    me = prop["me"]
    me_txt = f"{me * 100:.1f}".replace(".", ",")
    st.markdown(f"- **{rotulo}:** {_pct(prop['p'])} ({prop['k']} de {prop['n']}), margem de erro "
                f"±{me_txt} p.p. → entre {_pct(max(0, prop['p'] - me))} e "
                f"{_pct(min(1, prop['p'] + me))}")


# =============================================================== páginas
def pagina_perfil(todos: pd.DataFrame, validos: pd.DataFrame, filtrado: bool):
    st.title("Perfil da amostra")
    n_tot, n_val = len(todos), int(todos["VALIDA"].sum())
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Respostas recebidas", n_tot)
    c2.metric("Descartadas", n_tot - n_val)
    c3.metric("Válidas", n_val)
    c3.caption(f"meta {Q.META_VALIDAS} · mínimo {Q.MINIMO_VALIDAS}")
    me = A.margem_erro(0.5, n_val) if n_val else np.nan
    c4.metric("Margem de erro (pior caso)", f"±{me * 100:.1f} p.p.".replace(".", ",", 1) if n_val else "—")
    if n_val < Q.MINIMO_VALIDAS:
        st.warning(f"Ainda abaixo do mínimo de {Q.MINIMO_VALIDAS} respostas válidas.")

    st.subheader("Descartes e motivos")
    regras = pd.DataFrame(Q.REGRAS_DESCARTE, columns=["Regra", "Motivo"])
    regras["Respostas"] = regras["Regra"].map(todos["MOTIVO"].value_counts()).fillna(0).astype(int)
    col1, col2 = st.columns([1, 1])
    col1.dataframe(regras[["Regra", "Respostas", "Motivo"]], hide_index=True, width="stretch")
    log = todos.loc[~todos["VALIDA"], ["ID", "DATA_HORA", "MOTIVO"]].copy()
    log["Motivo"] = log["MOTIVO"].map(dict(Q.REGRAS_DESCARTE))
    log["Data e hora"] = log["DATA_HORA"].dt.strftime("%d/%m/%Y %H:%M")
    col2.dataframe(log[["ID", "Data e hora", "MOTIVO", "Motivo"]].rename(columns={"MOTIVO": "Regra"}),
                   hide_index=True, width="stretch", height=280)

    st.subheader("Respostas ao longo da coleta")
    t = todos.dropna(subset=["DATA_HORA"]).sort_values("DATA_HORA")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t["DATA_HORA"], y=np.arange(1, len(t) + 1), name="Recebidas",
                             line=dict(color="#86b6ef", width=2, shape="hv")))
    tv = t[t["VALIDA"]]
    fig.add_trace(go.Scatter(x=tv["DATA_HORA"], y=np.arange(1, len(tv) + 1), name="Válidas",
                             line=dict(color="#184f95", width=2, shape="hv")))
    for d, rot in ((Q.DATA_INICIO_COLETA, "início"), (Q.DATA_FIM_COLETA, "fim previsto")):
        x = pd.Timestamp(d).timestamp() * 1000
        fig.add_vline(x=x, line_dash="dot", line_color="rgba(128,128,128,0.8)",
                      annotation_text=rot, annotation_position="top left")
    fig.add_hline(y=Q.MINIMO_VALIDAS, line_dash="dot", line_color="#c43c3c",
                  annotation_text="mínimo (50)", annotation_position="bottom right")
    fig.update_yaxes(title="Respostas acumuladas")
    st.plotly_chart(layout(fig, altura=330), width="stretch")
    st.caption("Calculado a partir do carimbo de data/hora de cada resposta na exportação bruta.")

    st.subheader("Quem respondeu" + (" (segmento filtrado)" if filtrado else ""))
    st.caption(f"{len(validos)} respostas válidas no recorte atual.")
    a, b = st.columns(2)
    with a:
        barras_categorias(validos["P1"], "Experiência profissional", Q.OPCOES["P1"])
        barras_categorias(validos["P3"], "Porte da empresa", Q.OPCOES["P3"])
        barras_categorias(validos["P5"], "Tipo de organização", Q.OPCOES["P5"])
        barras_categorias(validos["P7"], "Canal de recebimento do link", Q.OPCOES["P7"])
        barras_categorias(validos["U2"], "Parcela do código gerada por IA (último mês)", Q.OPCOES["U2"])
    with b:
        barras_categorias(validos["P2"], "Cargo", Q.OPCOES["P2"])
        barras_categorias(validos["P4"], "Tempo na base de código atual", Q.OPCOES["P4"])
        barras_categorias(validos["P6"], "Code review obrigatório", Q.OPCOES["P6"])
        barras_categorias(validos["U1"], "Frequência de uso de IA", Q.OPCOES["U1"])
        barras_categorias(validos["U3"], "Forma de uso predominante", Q.OPCOES["U3"])
    barras_categorias(validos["U4"], "Ferramentas usadas (múltipla escolha; % sobre respondentes)",
                      Q.OPCOES["U4"], multi=True)


def pagina_likert(v: pd.DataFrame):
    st.title("Itens em escala Likert")
    st.caption("Barras centradas no ponto neutro: à esquerda, discordância (ou diminuição); à direita, "
               "concordância (ou aumento). A categoria neutra fica dividida ao meio. "
               "(R) = item invertido, mostrado como respondido.")
    barras_divergentes(v, ["G1", "G2"], Q.MUDANCA, "Avaliação global desde que passou a usar IA")
    barras_divergentes(v, Q.CONSTRUTOS["DC"]["itens"], Q.LIKERT, "Dívida de compreensão (DC)")
    barras_divergentes(v, Q.CONSTRUTOS["CP"]["itens"], Q.LIKERT, "Conhecimento do produto (CP)")
    barras_divergentes(v, Q.CONSTRUTOS["PV"]["itens"], Q.FREQUENCIA,
                       "Práticas de verificação (PV) — frequência")


def pagina_qps(v: pd.DataFrame, filtrado: bool):
    st.title("Questões de pesquisa")
    if filtrado:
        st.warning("Há filtros ativos: os testes abaixo foram recalculados só para o segmento e são "
                   "exploratórios. A resposta confirmatória usa a amostra válida completa.")
    res = {r.id: r for r in A.testar_hipoteses(v)}
    n = len(v)
    me_txt = f"{A.margem_erro(.5, n) * 100:.1f}".replace(".", ",") if n else "—"
    st.caption(f"n = {n} respostas válidas · margem de erro no pior caso ±{me_txt} p.p. "
               "· α = 0,05 · correção de Holm por família (confirmatória: H1–H4b; exploratória: E1–E3).")

    with st.expander("Tabela-resumo de todos os testes", expanded=False):
        tab = A.tabela_resultados(list(res.values()))
        tab["p"] = tab["p"].map(A.formatar_p)
        tab["p (Holm)"] = tab["p (Holm)"].map(A.formatar_p)
        st.dataframe(tab, hide_index=True, width="stretch")
        st.download_button("Baixar tabela (CSV)", tab.to_csv(index=False).encode("utf-8"),
                           "resultados_testes.csv", "text/csv")

    abas = st.tabs(["QP1 · perda de conhecimento do código", "QP2 · intensidade × dívida",
                    "QP3 · conhecimento do produto", "QP4 · experiência e verificação",
                    "Exploratórias"])

    with abas[0]:
        st.markdown("**Desenvolvedores percebem perda de conhecimento da base de código desde que passaram a usar IA?**")
        if "H1" in res:
            cartao_teste(res["H1"])
        texto_proporcao("Dizem que o conhecimento da base de código diminuiu (M6)",
                        A.proporcao(v["s_G1"].dropna() <= 2))
        texto_proporcao("Dizem que aumentou", A.proporcao(v["s_G1"].dropna() >= 4))
        texto_proporcao("Concordam que há código entregue com IA que não conseguiriam explicar (DC1, M8)",
                        A.proporcao(v["s_DC1"].dropna() >= 4))
        texto_proporcao("Índice DC acima do ponto neutro (> 3)", A.proporcao(v["DC"].dropna() > 3))
        barras_divergentes(v, ["G1"], Q.MUDANCA, "G1 — conhecimento da base de código")

    with abas[1]:
        st.markdown("**O uso mais intenso de IA está associado a maior dívida de compreensão?**")
        if "H2" in res:
            cartao_teste(res["H2"])
        caixas(v.assign(U2_ROT=v["U2"]), "DC", "U2_ROT", Q.OPCOES["U2"],
               "Índice de dívida de compreensão por parcela de código gerada por IA",
               "Índice DC (1–5)")

    with abas[2]:
        st.markdown("**O uso de IA ajudou o desenvolvedor a conhecer melhor o produto da empresa?**")
        for k in ("H3a", "H3b"):
            if k in res:
                cartao_teste(res[k])
        texto_proporcao("Dizem que o conhecimento do produto aumentou (M7)", A.proporcao(v["s_G2"].dropna() >= 4))
        texto_proporcao("Dizem que diminuiu", A.proporcao(v["s_G2"].dropna() <= 2))
        texto_proporcao("Índice CP acima do ponto neutro (> 3)", A.proporcao(v["CP"].dropna() > 3))
        a, b = st.columns(2)
        with a:
            barras_divergentes(v, ["G2"], Q.MUDANCA, "G2 — conhecimento do produto")
        with b:
            caixas(v, "CP", "U2", Q.OPCOES["U2"], "Índice CP por parcela de código gerada por IA",
                   "Índice CP (1–5)")

    with abas[3]:
        st.markdown("**Experiência e práticas de verificação estão associadas a dívida de compreensão diferente?**")
        for k in ("H4a", "H4b"):
            if k in res:
                cartao_teste(res[k])
        a, b = st.columns(2)
        with a:
            caixas(v, "DC", "FAIXA_EXP", Q.ORDEM_FAIXAS, "Índice DC por faixa de experiência",
                   "Índice DC (1–5)")
            if "H4a" in res:
                st.markdown("Pós-teste de Dunn (Holm):")
                d = res["H4a"].extra["dunn"].copy()
                d["p"] = d["p"].map(A.formatar_p); d["p (Holm)"] = d["p (Holm)"].map(A.formatar_p)
                st.dataframe(d.round(3), hide_index=True, width="stretch")
        with b:
            dispersao(v, "PV", "DC", "Práticas de verificação × dívida de compreensão",
                      "Índice PV (1–5)", "Índice DC (1–5)")

    with abas[4]:
        st.caption("Análises exploratórias: geram hipóteses, não confirmam.")
        if "E1" in res:
            cartao_teste(res["E1"])
        caixas(v, "DC", "U3", Q.OPCOES["U3"], "Índice DC por forma de uso predominante", "Índice DC (1–5)")
        if "E2" in res:
            cartao_teste(res["E2"])
            tab = res["E2"].extra["tabela"]
            st.dataframe(tab, width="stretch")
        if "E3" in res:
            cartao_teste(res["E3"])
            caixas(v, "DC", "REVIEW_SEMPRE", ["Code review sempre", "Nem sempre"],
                   "Índice DC por obrigatoriedade de code review", "Índice DC (1–5)")


def pagina_confiabilidade(v: pd.DataFrame):
    st.title("Confiabilidade dos construtos")
    st.caption("Alfa de Cronbach calculado sobre os itens já recodificados (invertidos corrigidos). "
               "Critério pré-registrado: ≥ 0,70 adequado; 0,60–0,70 aceitável com ressalva; "
               "< 0,60 o índice não é usado e os itens são analisados um a um.")
    resumo = []
    for chave, cfg in Q.CONSTRUTOS.items():
        r = A.alpha_cronbach(v[[f"r_{i}" for i in cfg["itens"]]])
        resumo.append({"Construto": f"{chave} — {cfg['nome']}", "Itens": len(cfg["itens"]),
                       "Invertidos": ", ".join(cfg["invertidos"]) or "—", "n": r["n"],
                       "Alfa de Cronbach": round(r["alfa"], 3), "Avaliação": A.classificar_alfa(r["alfa"])})
        with st.container(border=True):
            c1, c2 = st.columns([1, 2])
            c1.metric(f"{chave} — {cfg['nome']}", f"α = {r['alfa']:.2f}".replace(".", ","))
            c1.caption(A.classificar_alfa(r["alfa"]))
            if len(r["itens"]):
                c2.dataframe(r["itens"].round(3), hide_index=True, width="stretch")
    st.subheader("Resumo")
    st.dataframe(pd.DataFrame(resumo), hide_index=True, width="stretch")


def pagina_abertas(v: pd.DataFrame):
    st.title("Respostas abertas (A1)")
    resp = v.loc[v["A1"].fillna("") != "", ["ID", "A1"]]
    st.metric("Respostas abertas", f"{len(resp)} de {len(v)}")
    if ARQ_CODIFICACAO.exists():
        cod = pd.read_csv(ARQ_CODIFICACAO, dtype=str).dropna(how="all")
        cod = cod[cod["ID"].isin(v["ID"])] if "ID" in cod.columns else cod.iloc[0:0]
        if len(cod):
            freq = cod["codigo"].str.strip().value_counts()
            fig = go.Figure(go.Bar(y=freq.index[::-1], x=freq.values[::-1], orientation="h",
                                   marker_color=COR_DESTAQUE, text=freq.values[::-1],
                                   textposition="outside", cliponaxis=False))
            fig.update_layout(title="Frequência dos códigos temáticos")
            st.plotly_chart(layout(fig, altura=100 + 36 * len(freq)), width="stretch")
            st.caption("Uma resposta pode receber mais de um código. Concordância entre codificadores "
                       "(kappa de Cohen) registrada na página de metodologia.")
        else:
            st.info("A codificação ainda não foi feita. Preencha codificacao_abertas.csv (colunas ID, codigo).")
    if st.toggle("Mostrar textos (já revisados para remover dados identificáveis)"):
        st.dataframe(resp, hide_index=True, width="stretch")


def pagina_metodologia(todos: pd.DataFrame, v: pd.DataFrame, faltantes: list[str]):
    st.title("Metodologia e desvios")
    st.markdown(f"""
**Protocolo registrado (Parte 1).** Survey transversal com amostragem não probabilística por conveniência
e bola de neve. População: pessoas que trabalham desenvolvendo software no Brasil e usaram assistentes de IA
em tarefas de código nos últimos 3 meses. Coleta prevista: {Q.DATA_INICIO_COLETA:%d/%m/%Y} a
{Q.DATA_FIM_COLETA:%d/%m/%Y} (prorrogável até 24/11 se houver menos de 50 válidas em 19/11);
entrega final em {Q.DATA_ENTREGA_FINAL:%d/%m/%Y}. Meta: {Q.META_VALIDAS} respostas válidas (mínimo {Q.MINIMO_VALIDAS}).
Testes não paramétricos, α = 0,05, correção de Holm por família, tamanho de efeito em todos os testes.
""")
    st.subheader("Regras de descarte (na ordem aplicada)")
    st.dataframe(pd.DataFrame(Q.REGRAS_DESCARTE, columns=["Regra", "Descrição"]), hide_index=True,
                 width="stretch")

    st.subheader("Desvios detectados automaticamente")
    auto = []
    n_val = int(todos["VALIDA"].sum())
    if faltantes:
        auto.append(f"Colunas esperadas ausentes na exportação: {', '.join(faltantes)}.")
    if n_val < Q.META_VALIDAS:
        auto.append(f"Amostra válida ({n_val}) abaixo da meta de {Q.META_VALIDAS}; "
                    f"margem de erro no pior caso ±{A.margem_erro(.5, max(n_val, 1)) * 100:.1f} p.p. "
                    f"em vez de ±9,8 p.p.")
    datas = todos.loc[todos["VALIDA"], "DATA_HORA"].dropna()
    if len(datas) and datas.max() > pd.Timestamp(Q.DATA_FIM_COLETA) + pd.Timedelta(days=1):
        auto.append(f"Respostas válidas após a data final prevista (última: {datas.max():%d/%m/%Y}).")
    for chave, cfg in Q.CONSTRUTOS.items():
        a = A.alpha_cronbach(v[[f"r_{i}" for i in cfg["itens"]]])["alfa"]
        if not np.isnan(a) and a < 0.60:
            auto.append(f"Alfa de {chave} = {a:.2f} < 0,60: índice substituído pela análise item a item.")
    for r in A.testar_hipoteses(v):
        if "unidos" in r.detalhe:
            auto.append(f"{r.id}: {r.detalhe}.")
        if "permutação" in r.teste:
            auto.append(f"{r.id}: p-valor obtido por permutação (frequências esperadas baixas).")
    if auto:
        for linha in auto:
            st.markdown(f"- {linha}")
    else:
        st.markdown("Nenhum desvio automático detectado.")

    st.subheader("Desvios declarados pelo grupo")
    if ARQ_DESVIOS.exists():
        st.markdown(ARQ_DESVIOS.read_text(encoding="utf-8"))
    else:
        st.info("Crie o arquivo desvios.md para registrar os desvios em relação ao protocolo.")


# =============================================================== main
def main():
    conteudo, nome, rotulo = obter_fonte()
    if conteudo is None:
        st.title("Dívida de compreensão no uso de IA")
        st.info("Envie a exportação do Google Forms na barra lateral (Respostas → ⋮ → Baixar respostas "
                "(.csv)) ou salve o arquivo como `dados/respostas.csv`.")
        return
    todos, eh_teste, faltantes = carregar(conteudo, nome)
    if eh_teste:
        st.error("⚠️ DADOS FICTÍCIOS DE TESTE — estes números não são resultados do survey.")
    st.sidebar.caption(f"Fonte: {rotulo} · {len(todos)} linhas")

    pagina = st.sidebar.radio("Página", ["Perfil da amostra", "Itens Likert", "Questões de pesquisa",
                                         "Confiabilidade", "Respostas abertas", "Metodologia e desvios"])

    st.sidebar.header("Filtros por segmento")
    validos_todos = todos[todos["VALIDA"]].copy()
    filtros = {"FAIXA_EXP": ("Experiência", Q.ORDEM_FAIXAS), "P2": ("Cargo", Q.OPCOES["P2"]),
               "P3": ("Porte da empresa", Q.OPCOES["P3"]), "P5": ("Tipo de organização", Q.OPCOES["P5"]),
               "U3": ("Forma de uso de IA", Q.OPCOES["U3"])}
    mascara = pd.Series(True, index=validos_todos.index)
    filtrado = False
    for col, (rot, ordem) in filtros.items():
        presentes = [o for o in ordem if o in set(validos_todos[col].dropna())]
        presentes += sorted(set(validos_todos[col].dropna()) - set(presentes) - {""})
        escolha = st.sidebar.multiselect(rot, presentes, default=[], placeholder="Todos")
        if escolha:
            filtrado = True
            mascara &= validos_todos[col].isin(escolha)
    validos = validos_todos[mascara]
    if filtrado:
        st.sidebar.caption(f"{len(validos)} respostas válidas no segmento.")
    if filtrado and len(validos) < Q.MIN_SEGMENTO:
        st.warning(f"Segmento com menos de {Q.MIN_SEGMENTO} respostas: resultados ocultos para "
                   "proteger o anonimato e evitar conclusões instáveis.")
        if pagina not in ("Metodologia e desvios",):
            return

    if pagina == "Perfil da amostra":
        pagina_perfil(todos, validos, filtrado)
    elif pagina == "Itens Likert":
        pagina_likert(validos)
    elif pagina == "Questões de pesquisa":
        pagina_qps(validos, filtrado)
    elif pagina == "Confiabilidade":
        pagina_confiabilidade(validos)
    elif pagina == "Respostas abertas":
        pagina_abertas(validos)
    else:
        pagina_metodologia(todos, validos_todos, faltantes)


main()

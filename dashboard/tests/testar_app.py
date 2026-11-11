"""Executa todas as páginas do dashboard com os dados fictícios e falha se houver exceção."""
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parents[1] / "app.py")
PAGINAS = ["Perfil da amostra", "Itens Likert", "Questões de pesquisa", "Confiabilidade",
           "Respostas abertas", "Metodologia e desvios"]

for pagina in PAGINAS:
    at = AppTest.from_file(APP, default_timeout=120)
    at.run()
    at.sidebar.toggle[0].set_value(True).run()
    at.sidebar.radio[0].set_value(pagina).run()
    assert not at.exception, (pagina, at.exception)
    print(f"ok  {pagina}: {len(at.get('plotly_chart'))} gráficos, {len(at.dataframe)} tabelas")

# filtro que reduz o segmento
at = AppTest.from_file(APP, default_timeout=120); at.run()
at.sidebar.toggle[0].set_value(True).run()
at.sidebar.radio[0].set_value("Questões de pesquisa").run()
at.sidebar.multiselect[0].set_value(["10 anos ou mais"]).run()
assert not at.exception, at.exception
print("ok  filtro por experiência:", [w.value[:60] for w in at.warning])

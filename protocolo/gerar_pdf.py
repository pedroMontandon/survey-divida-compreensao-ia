"""Gera o PDF compacto do protocolo (A4, até 6 páginas) a partir do Markdown.

Fluxo: edite o documento do protocolo, exporte como Markdown (ou edite protocolo.md
diretamente) e rode:

    pip install markdown playwright && playwright install chromium
    python gerar_pdf.py protocolo.md

O PDF sai com o mesmo nome (.pdf) e o script informa o número de páginas.
"""

import re
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

CSS = """
@page { size: A4; margin: 15mm 15mm 14mm 15mm;
        @bottom-right { content: counter(page); } }
body { font-family: "Source Sans 3", "Source Sans Pro", "Segoe UI", Arial, sans-serif;
       font-size: 9.6pt; line-height: 1.32; color: #1b1b1a; }
h1 { font-size: 15pt; margin: 0 0 2pt; line-height: 1.15; }
h2 { font-size: 11.5pt; margin: 9pt 0 3pt; padding-bottom: 1pt; border-bottom: 0.6pt solid #b9b7b0;
     break-after: avoid; }
p { margin: 0 0 4pt; text-align: justify; hyphens: auto; }
ul { margin: 0 0 4pt; padding-left: 13pt; } li { margin: 0 0 1.5pt; }
table { border-collapse: collapse; width: 100%; margin: 3pt 0 5pt; font-size: 8.4pt;
        line-height: 1.22; }
th, td { border: 0.5pt solid #c9c7c0; padding: 1.6pt 4pt; vertical-align: top; text-align: left; }
th { background: #eeede9; font-weight: 600; }
tr { break-inside: avoid; }
.formula { text-align: center; font-style: italic; margin: 3pt 0 4pt; font-size: 10pt; }
.byline { color: #5a5955; font-size: 8.6pt; margin-bottom: 5pt; }
a { color: #1c5cab; text-decoration: none; }
"""


def tex_para_texto(tex: str) -> str:
    t = tex.strip().replace("{,}", ",").replace("\\times", "×").replace("\\cdot", "·")
    for _ in range(3):
        t = re.sub(r"\\frac\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}\{([^{}]*)\}", r"\1 / \2", t)
        t = re.sub(r"\\sqrt\{([^{}]*)\}", r"√(\1)", t)
    return t.replace("{", "").replace("}", "")


def preparar(md: str) -> str:
    md = re.sub(r"```latex\n(.*?)```", lambda m: f'<p class="formula">{tex_para_texto(m.group(1))}</p>',
                md, flags=re.S)
    # linha de data/autor exportada pelo documento vira uma linha discreta
    md = re.sub(r"^(\w{3} \d{1,2}, \d{4} · @\S+)\s*$", r'<p class="byline">\1</p>', md, flags=re.M)
    return md


def main(caminho: str):
    origem = Path(caminho)
    html_corpo = markdown.markdown(preparar(origem.read_text(encoding="utf-8")),
                                   extensions=["tables", "sane_lists"])
    html = f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><style>{CSS}</style></head>" \
           f"<body>{html_corpo}</body></html>"
    destino = origem.with_suffix(".pdf")
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pg = nav.new_page()
        pg.set_content(html, wait_until="load")
        pg.pdf(path=str(destino), format="A4", print_background=True, display_header_footer=True,
               header_template="<span></span>",
               footer_template="<div style='font-size:7pt;width:100%;text-align:right;"
                               "padding-right:15mm;color:#777'><span class='pageNumber'></span>"
                               "/<span class='totalPages'></span></div>",
               margin={"top": "14mm", "bottom": "14mm", "left": "15mm", "right": "15mm"})
        nav.close()
    paginas = len(re.findall(rb"/Type\s*/Page[^s]", destino.read_bytes()))
    print(f"{destino} — {paginas} página(s){'  ⚠ acima do limite de 6' if paginas > 6 else ''}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).with_name("protocolo.md")))

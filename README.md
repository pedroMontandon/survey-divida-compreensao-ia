# Survey: Dívida de compreensão no uso de IA

Trabalho final de Medição e Experimentação em Engenharia de Software (PUC Minas, 2º/2026).

```
protocolo/   protocolo da Parte 1 (PDF) — o commit deste arquivo é a prova de data do pré-registro
formulario/  criar_formulario.gs — cria o questionário no Google Forms
dashboard/   dashboard da Parte 2 (Streamlit), que lê a exportação bruta do formulário
```

## Ordem de trabalho

1. Criar o formulário. Em script.google.com, novo projeto, cole `formulario/criar_formulario.gs`,
   ajuste `CONTATO_GRUPO` e execute `criarFormulario`. Os links aparecem no registro de execução.
   Confira no Forms que "Coletar endereços de e-mail" está desativado.
2. Pré-teste (3 a 5 pessoas fora da turma). Anote tempo, dúvidas e mudanças na seção 4 do protocolo.
   Se mudar algum texto de item ou opção, mude também em `dashboard/questionario.py`.
   Depois, apague as respostas do pré-teste (Respostas → ⋮ → Excluir todas as respostas).
3. Registrar o protocolo. Preencha os campos `[PREENCHER]`, exporte o PDF, salve em `protocolo/`
   e faça o commit antes da primeira resposta. Envie o mesmo PDF na plataforma até sexta, 13/11.
4. Coletar de 14/11 a 22/11 (seção 8 do protocolo); entrega final em 27/11. Guarde capturas datadas de cada divulgação.
5. Rodar o dashboard com os dados reais (abaixo) e registrar desvios em `dashboard/desvios.md`.
6. Codificar a pergunta aberta (A1) em `dashboard/codificacao_abertas.csv` (colunas `ID,codigo`;
   uma linha por código; o ID é o que aparece no dashboard, R001, R002…).

## Dashboard

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

Dados: baixe as respostas do Forms (Respostas → ⋮ → Baixar respostas (.csv)) e envie pelo botão
da barra lateral, ou salve como `dashboard/dados/respostas.csv`. O `.gitignore` mantém os dados
brutos fora do repositório; se o repositório for privado e compartilhado só com o professor, pode
versioná-los removendo essa linha.

Para publicar no Streamlit Community Cloud lendo a planilha ao vivo, defina `CSV_URL` em
`.streamlit/secrets.toml` com o link de exportação CSV da planilha. Atenção: um link público expõe
as respostas; prefira o upload durante a apresentação.

### Dados fictícios (só para ensaio)

```bash
python tests/gerar_dados_teste.py   # cria tests/DADOS_FICTICIOS_teste.csv
python tests/testar_app.py          # executa todas as páginas e falha se houver erro
```

O arquivo fictício tem uma coluna `[TESTE]`; sempre que ela estiver presente o dashboard mostra
um aviso vermelho. Nunca misture essas linhas com respostas reais nem as apresente como resultado.

### O que cada página mostra

| Página | Conteúdo |
| --- | --- |
| Perfil da amostra | recebidas, descartadas por regra (D0–D6), válidas, margem de erro, respostas ao longo da coleta, perfil |
| Itens Likert | barras divergentes de G1–G2, DC, CP e PV |
| Questões de pesquisa | por QP: teste, p bruto e ajustado (Holm), tamanho de efeito, n, proporções com margem de erro, gráficos |
| Confiabilidade | alfa de Cronbach, correlação item-total e alfa sem cada item |
| Respostas abertas | frequência dos códigos temáticos |
| Metodologia e desvios | resumo do protocolo, regras de descarte, desvios automáticos e `desvios.md` |

Filtros por segmento (experiência, cargo, porte, tipo de organização, forma de uso) ficam na barra
lateral; com filtros ativos os testes são marcados como exploratórios e segmentos com menos de
5 respostas ficam ocultos.

### Onde cada regra do protocolo está no código

- Opções, construtos, itens invertidos, faixas e datas: `dashboard/questionario.py`
- Limpeza D0–D6, índices, testes, efeitos, Holm, Cronbach, margem de erro: `dashboard/analise.py`

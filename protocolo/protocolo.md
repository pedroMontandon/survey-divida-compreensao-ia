# Protocolo do Survey — Dívida de compreensão no uso de IA

**Disciplina:** Medição e Experimentação em Engenharia de Software — PUC Minas, 2º/2026 · **Grupo 5:** Jonathan Senna, Matheus Titton, Murilo Andrade, Pedro Luiz Nato e Pedro Henrique Barbosa · **Registro:** este protocolo é versionado no repositório https://github.com/pedroMontandon/survey-divida-compreensao-ia; o hash e a data do commit comprovam que foi registrado antes da primeira resposta · **Instrumento:** Google Forms · **Análise:** dashboard em Streamlit (Python) que lê a exportação bruta do formulário.

**Contexto.** “Dívida de compreensão” é o nome dado à distância crescente entre a quantidade de código de um sistema e o quanto dele alguma pessoa realmente entende, agravada quando a IA gera código mais rápido do que é possível revisá-lo (Osmani, 2026; Storey, 2026). Um ensaio controlado recente encontrou pior desempenho em compreensão entre quem aprendeu uma biblioteca com assistência de IA, sobretudo quando a IA foi usada por delegação passiva (Anthropic, 2026). Este survey investiga como desenvolvedores percebem esse efeito no próprio trabalho e se, em contrapartida, a IA os ajuda a conhecer melhor o produto da empresa.

## 1. Objetivo e questões de pesquisa

**Objetivo (GQM).** *Analisar* o uso de assistentes de IA no desenvolvimento de software *com o propósito de* caracterizar e avaliar *com respeito à* compreensão da base de código (dívida de compreensão) e ao conhecimento do produto da empresa *do ponto de vista de* desenvolvedores de software *no contexto de* profissionais que atuam no Brasil e usam IA no trabalho.

| QP | Pergunta | Hipótese nula (H₀) | Métricas |
| --- | --- | --- | --- |
| QP1 | Desenvolvedores percebem perda de conhecimento da base de código desde que passaram a usar IA? | H1₀: a mediana de G1 é igual a 3 (“não mudou”). | M6, M1, M8 |
| QP2 | O uso mais intenso de IA está associado a maior dívida de compreensão? | H2₀: ρ(U2, DC) = 0. | M4, M1 |
| QP3 | O uso de IA ajudou o desenvolvedor a conhecer melhor o produto da empresa? | H3a₀: a mediana de G2 é igual a 3. H3b₀: ρ(U2, CP) = 0. | M7, M2, M4 |
| QP4 | Experiência e práticas de verificação estão associadas a dívida de compreensão diferente? | H4a₀: DC tem a mesma distribuição nas três faixas de experiência. H4b₀: ρ(PV, DC) = 0. | M1, M3, M5 |

As seis hipóteses acima formam a família confirmatória. Testes adicionais (seção 5) são exploratórios e serão relatados como tal. Por ser um estudo transversal de percepção, nenhuma conclusão será causal.

## 2. População e amostragem

A meta é 100 respostas válidas (mínimo de 50), o que dá margem de erro de ±9,8 p.p. no pior caso.

- **População-alvo:** pessoas que trabalham atualmente desenvolvendo software no Brasil (incluindo estágio) e que usaram assistentes de IA em tarefas de código nos últimos 3 meses. Duas perguntas de triagem garantem isso. Colegas da turma não fazem parte da amostra: o link não será divulgado em nenhum canal da turma.
- **Origem dos contatos:** redes profissionais dos integrantes (LinkedIn, colegas de trabalho e de curso fora desta turma), comunidades de desenvolvedores (grupos de WhatsApp/Telegram, Discord, Reddit r/brdev, TabNews).
- **Estratégia:** amostragem não probabilística por conveniência, com bola de neve (o convite pede que o respondente repasse o link). Não há lista da população, o que impede amostragem aleatória.
- **Tamanho:** análise de poder para detectar correlação de Spearman ρ = 0,30 (efeito médio), α = 0,05 bicaudal e poder de 80% indica n ≈ 85. Prevendo cerca de 15% de descartes, buscamos ~120 respostas brutas.

```latex
e = 1{,}96 \times \sqrt{\frac{p(1-p)}{n}}
```

| Respostas válidas (n) | Margem de erro no pior caso (p = 0,5) |
| --- | --- |
| 50 (mínimo) | ±13,9 p.p. |
| 85 (poder) | ±10,6 p.p. |
| 100 (meta) | ±9,8 p.p. |

A população é grande o bastante para dispensar a correção de população finita. Como a amostra não é aleatória, a margem de erro será relatada como referência de precisão, e não como garantia de representatividade.

## 3. Questionário com rastreabilidade

O formulário tem 30 itens em 8 seções (≈ 7 minutos). Cada título de pergunta começa com seu código entre colchetes (ex.: “[DC1]”), que o dashboard usa para ler a exportação. Escala Likert = 1 Discordo totalmente … 5 Concordo totalmente; escala de frequência = 1 Nunca … 5 Sempre; escala de mudança = 1 Diminuiu muito … 3 Não mudou … 5 Aumentou muito. (R) = item invertido.

| Código | Item | Escala | QP / Métrica |
| --- | --- | --- | --- |
| CONS | Termo de consentimento: concordo em participar | Nominal | Triagem |
| T1 | Atualmente, trabalha com desenvolvimento de software (incluindo estágio)? | Nominal | Triagem |
| T2 | Usou assistentes de IA em tarefas de código nos últimos 3 meses? | Nominal | Triagem |
| P1 | Tempo de experiência profissional (5 faixas: menos de 1 ano, 1 a 2, 3 a 5, 6 a 9 e 10 anos ou mais) | Ordinal | QP4 / M5 |
| P2 | Cargo (estágio, júnior, pleno, sênior, liderança técnica, outro) | Nominal | Filtro |
| P3 | Porte da empresa (nº de funcionários, 5 faixas) | Ordinal | Filtro |
| P4 | Tempo no sistema atual (5 faixas: menos de 6 meses, 6 a 11 meses, 1 a 2, 3 a 4 e 5 anos ou mais) | Ordinal | Filtro |
| P5 | Tipo de organização | Nominal | Filtro |
| P6 | A equipe exige code review antes do merge? (sim, sempre; sim, em alguns casos; não) | Nominal | QP4 expl. |
| P7 | Onde recebeu o link do questionário? | Nominal | Ameaças |
| U1 | Frequência de uso de IA para código (4 níveis) | Ordinal | Descritiva |
| U2 | Parcela do código entregue no último mês gerada por IA (0–20% … 81–100%) | Ordinal | QP2, QP3 / M4 |
| U3 | Forma predominante: autocompletar, chat ou agentes | Nominal | QP2, QP3 expl. |
| U4 | Ferramentas usadas (múltipla escolha) | Nominal | Descritiva |
| G1 | Desde que uso IA, meu conhecimento da base de código… | Ordinal (mudança) | QP1 / M6 |
| G2 | Desde que uso IA, meu conhecimento do produto da empresa… | Ordinal (mudança) | QP3 / M7 |
| DC1 | Há trechos que entreguei com IA que eu não conseguiria explicar em detalhe a um colega | Likert | QP1, QP2 / M1, M8 |
| DC2 | Tenho mais dificuldade de localizar onde uma funcionalidade está implementada sem pedir ajuda à IA | Likert | M1 |
| DC3 (R) | Consigo explicar a arquitetura e o fluxo principal do sistema sem consultar ferramentas | Likert | M1 |
| ATT1 | Atenção: marque “Discordo totalmente” nesta linha | Likert | Descarte |
| DC4 | Quando há bug em código gerado com IA, preciso da IA para entender o que ele faz | Likert | M1 |
| DC5 | Conheço a base de código menos do que conheceria se tivesse escrito sem IA | Likert | M1 |
| CP1 | A IA me ajudou a entender regras de negócio do produto | Likert | QP3 / M2 |
| CP2 | Uso a IA para explorar partes do sistema que eu ainda não conhecia | Likert | M2 |
| CP3 | Com a IA, compreendo melhor como as funcionalidades do produto se relacionam | Likert | M2 |
| CP4 | Com a IA, respondo dúvidas de colegas ou da área de negócio sobre o produto com mais segurança | Likert | M2 |
| PV1 | Leio e entendo todo o código sugerido pela IA antes de aceitá-lo | Frequência | QP4 / M3 |
| PV2 | Peço à IA que explique o código gerado quando não o entendo | Frequência | M3 |
| PV3 (R) | Aceito sugestões que funcionam mesmo sem entender como funcionam | Frequência | M3 |
| A1 | (Aberta, opcional) Situação em que a IA afetou sua compreensão do código ou do produto | Texto | Todas |

**Métricas.** M1 = índice de dívida de compreensão (média de DC1–DC5, DC3 invertido; 1–5, maior = mais dívida). M2 = índice de conhecimento do produto (média de CP1–CP4). M3 = índice de práticas de verificação (média de PV1–PV3, PV3 invertido). M4 = intensidade de uso (U2, 1–5). M5 = faixa de experiência (P1 agrupada em até 2, de 3 a 9 e 10 anos ou mais). M6 e M7 = proporção que respondeu “diminuiu” em G1 e “aumentou” em G2. M8 = proporção que concorda com DC1. Os índices M1–M3 são escores ordinais compostos, analisados com testes não paramétricos.

**Ordem.** As avaliações globais (G1, G2) vêm antes dos blocos específicos para não serem influenciadas por eles. A pergunta de atenção fica no meio do bloco DC, e os itens invertidos ajudam a detectar respostas em linha reta e aquiescência.

## 4. Pré-teste

O questionário foi aplicado, antes da entrega deste protocolo, a 3 desenvolvedores de fora da turma, de senioridades diferentes (sênior, pleno e júnior). Cada pessoa recebeu o link por mensagem, respondeu sozinha e relatou por mensagem suas dúvidas e problemas; registramos o tempo de preenchimento.

Verificamos: clareza e ambiguidade de cada item, adequação das escalas, tempo ≤ 10 minutos, funcionamento das ramificações da triagem e leitura correta da exportação pelo dashboard. As respostas do pré-teste são apagadas do formulário antes do início da coleta; por segurança, o dashboard também descarta respostas anteriores à data de início (regra D0).

| Participante (perfil) | Tempo (min) | Problemas encontrados | Mudança feita |
| --- | --- | --- | --- |
| 1 (sênior) | 8 | Erros de grafia e redação | Grafia corrigida |
| 2 (pleno) | 3 | Nenhum relatado; respondeu sem ler com atenção e errou a pergunta de atenção (ATT1) | Nenhuma: a regra D3 descarta esse tipo de resposta |
| 3 (júnior) | 6 | Nenhum | Nenhuma |

**Resumo das mudanças:** nenhum item foi incluído ou removido, e nenhum participante apontou ambiguidade de conteúdo. O tempo de preenchimento (3 a 8 minutos) ficou dentro do limite de 10. O participante 2 respondeu sem atenção e errou ATT1, o que mostra que a pergunta de atenção identifica esse tipo de resposta; por isso mantivemos a regra D3 sem alteração. A grafia apontada pelo participante 1 foi corrigida, e a redação do termo de consentimento, da triagem e dos blocos de perfil e uso de IA foi revisada. As faixas de tempo de P1 e P4 passaram a ser em anos completos, sem sobreposição nos limites (ex.: “De 1 a 2 anos”, “De 3 a 5 anos”); os cortes de P1 que definem as faixas de experiência (M5) não mudaram.

## 5. Plano de análise

Todos os testes usam α = 0,05 bicaudal, são não paramétricos (as variáveis são ordinais) e são recalculados pelo dashboard a partir da exportação bruta.

**Limpeza (aplicada nesta ordem; cada descarte registra a primeira regra violada):** D0 resposta anterior à data de início da coleta (pré-teste) · D1 sem consentimento · D2 fora da população (T1 ou T2 = Não) · D3 errou a pergunta de atenção · D4 respostas em linha reta (mesma posição nos 12 itens DC, CP e PV, incoerente com os itens invertidos) · D5 duplicata exata de resposta anterior · D6 item obrigatório ausente.

**Descritiva.** Frequências e percentuais por item; mediana e intervalo interquartil dos índices; barras divergentes para itens Likert. Toda proporção vem com margem de erro de 95%.

**Confiabilidade.** Alfa de Cronbach para DC, CP e PV, com correlação item-total corrigida e alfa sem cada item. Critério: α ≥ 0,70 adequado; 0,60 a 0,70 aceitável com ressalva; abaixo de 0,60 o índice não é usado e os itens são analisados um a um (desvio declarado).

| Hipótese | Teste | Tamanho de efeito | Por quê |
| --- | --- | --- | --- |
| H1 (G1 vs. 3) | Wilcoxon de uma amostra contra o ponto neutro | Correlação rank-bisserial pareada | Variável ordinal; pergunta “há perda?” |
| H2 (U2 × DC) | Correlação de Spearman | ρ (0,1 / 0,3 / 0,5) | Duas variáveis ordinais |
| H3a (G2 vs. 3) | Wilcoxon de uma amostra | Rank-bisserial pareada | Igual a H1 |
| H3b (U2 × CP) | Spearman | ρ | Duas ordinais |
| H4a (DC por experiência) | Kruskal-Wallis + pós-teste de Dunn | ε² (0,01 / 0,08 / 0,26) | Três grupos independentes |
| H4b (PV × DC) | Spearman | ρ | Duas ordinais |
| Expl. 1 (DC por forma de uso U3) | Kruskal-Wallis + Dunn | ε² | Três grupos |
| Expl. 2 (G2 por forma de uso) | χ² de independência (G2 em 3 categorias) | V de Cramér | Duas nominais |
| Expl. 3 (DC por code review obrigatório) | Mann-Whitney | Rank-bisserial | Dois grupos |

**Múltiplas comparações.** Correção de Holm-Bonferroni na família confirmatória (6 testes) e, separadamente, na exploratória; também nos pós-testes de Dunn. Relatamos p bruto e ajustado. Se algum grupo tiver menos de 5 respostas, ele é unido ao grupo vizinho; no χ², se mais de 20% das células tiverem frequência esperada abaixo de 5, o p-valor é obtido por permutação (10.000 reamostragens).

**Respostas abertas (A1).** Análise temática: dois integrantes codificam as respostas de forma independente com um livro de códigos inicial (perda de compreensão, ganho de compreensão do código, aprendizado do domínio/produto, dependência da IA, estratégias de verificação, outro), que pode receber novos códigos. A concordância é medida pelo kappa de Cohen nas primeiras 20 respostas; divergências são resolvidas em consenso antes de codificar o restante. As frequências dos códigos aparecem no dashboard.

## 6. Ética e LGPD

O survey é uma pesquisa de opinião com participantes não identificados, situação que a Resolução CNS nº 510/2016 (art. 1º, parágrafo único, I) dispensa de registro no sistema CEP/Conep; ainda assim, seguiremos as orientações da PUC Minas e confirmaremos o enquadramento com o professor.

- **Termo de consentimento (1ª seção do formulário):** objetivo do estudo em linguagem neutra, tempo estimado, participação voluntária, possibilidade de desistir a qualquer momento sem enviar, ausência de riscos além dos cotidianos, uso exclusivamente acadêmico e agregado, contato do grupo. Quem não concorda é levado direto ao fim do formulário.
- **Anonimização:** o formulário não coleta e-mail nem exige login; nenhuma pergunta pede nome, empresa ou cidade. Respostas abertas são revisadas e qualquer dado identificável (nome de pessoa, empresa ou cliente) é substituído por “[removido]” antes de entrar no dashboard.
- **Armazenamento:** respostas brutas e base anonimizada ficam no Google Drive, com acesso restrito aos integrantes e ao professor. O repositório GitHub é público, mas contém apenas o protocolo, o script do formulário e o código de análise; nenhum dado de resposta é versionado (o `.gitignore` os exclui). Os resultados só são apresentados de forma agregada, e o dashboard oculta segmentos com menos de 5 respostas.
- **Base legal e retenção (LGPD):** consentimento do titular (art. 7º, I). Os dados brutos serão excluídos até 6 meses após o fim da disciplina; a base anonimizada, que deixa de ser dado pessoal (art. 12), pode ser mantida para fins acadêmicos.

## 7. Ameaças à validade

| Ameaça | Tipo | Mitigação |
| --- | --- | --- |
| Não resposta | Externa | Questionário curto (≈ 7 min), vários canais, dois lembretes; relatamos o perfil obtido e sua limitação. |
| Autosseleção (entusiastas ou críticos de IA respondem mais) | Externa | Convite neutro (“uso de IA e conhecimento do código”), sem citar “dívida” nem as hipóteses; P7 permite comparar canais. |
| Desejabilidade social (admitir que não entende o código) | Construto | Anonimato reforçado no termo, redação sem julgamento, itens indiretos e invertidos. |
| Percepção ≠ compreensão real (autorrelato) | Construto | Conclusões restritas à percepção; construtos com vários itens e alfa de Cronbach. |
| Viés de memória ao estimar a parcela de código gerada por IA (U2) | Construto | Faixas largas de 20 p.p. e período recente (último mês). |
| Aquiescência e respostas descuidadas ou automáticas | Interna | Itens invertidos, pergunta de atenção, regras D3–D5. |
| Colegas da turma respondem (proibido pelo enunciado) | Externa | O link não é divulgado nos canais da turma, e o termo de consentimento pede que alunos da disciplina não respondam. |
| Variáveis de confusão (experiência, tempo na base, tipo de empresa) | Interna | Estudo correlacional sem conclusão causal; filtros por segmento no dashboard; análises exploratórias por grupo. |
| Amostra por conveniência e bola de neve concentrada na rede do grupo (ex.: Minas Gerais) | Externa | Diversificar canais; relatar perfil e margem de erro; não generalizar para todos os desenvolvedores. |
| Muitos testes e pouco poder | Conclusão | Família confirmatória pré-definida, correção de Holm, análise de poder, tamanho de efeito sempre relatado. |
| Ordem das perguntas | Construto | Avaliações globais antes dos blocos específicos. |

## 8. Plano de divulgação

A coleta vai de 14/11/2026 a 22/11/2026 (9 dias), começando no dia seguinte à entrega deste protocolo. A entrega final (dashboard e defesa) é em 27/11/2026; os dias entre o fim da coleta e a entrega ficam para limpeza, codificação das respostas abertas e revisão do dashboard.

- **Canais:** publicações dos integrantes no LinkedIn (com pedido de compartilhamento); grupos de WhatsApp/Telegram de desenvolvedores; servidores de Discord, Reddit r/brdev e TabNews; colegas de trabalho e de curso fora desta turma; ao final do formulário, pedido para repassar o link (bola de neve).
- **Cronograma:** divulgação inicial em 14/11; lembretes em 17/11 e 20/11; em 19/11, se houver menos de 50 respostas válidas, a coleta é prorrogada até 24/11 (desvio a ser declarado na Parte 2). O formulário é fechado na data final, independentemente do número de respostas.
- **Evidências:** cada publicação é registrada em captura de tela com data e hora, sem dados de respondentes; a exportação bruta do formulário (com carimbo de data/hora) e o acesso ao painel do Forms serão mostrados na apresentação.

## Referências

- ANTHROPIC. *How AI impacts skill formation*. arXiv:2601.20245, 2026. [Link](https://arxiv.org/abs/2601.20245)
- BRASIL. Conselho Nacional de Saúde. *Resolução nº 510, de 7 de abril de 2016*. [Link](https://www.conass.org.br/?p=6270)
- BRASIL. *Lei nº 13.709, de 14 de agosto de 2018* (Lei Geral de Proteção de Dados Pessoais).
- KITCHENHAM, B.; PFLEEGER, S. L. Personal opinion surveys. In: SHULL, F.; SINGER, J.; SJØBERG, D. (ed.). *Guide to Advanced Empirical Software Engineering*. London: Springer, 2008.
- OSMANI, A. *Comprehension debt: the hidden cost of AI-generated code*. O’Reilly Radar, 13 abr. 2026. [Link](https://www.oreilly.com/radar/comprehension-debt-the-hidden-cost-of-ai-generated-code/)
- STOREY, M.-A. *Cognitive debt*. Blog, 9 fev. 2026. [Link](https://margaretstorey.com/blog/2026/02/09/cognitive-debt/)
- WOHLIN, C. et al. *Experimentation in Software Engineering*. Berlin: Springer, 2012.

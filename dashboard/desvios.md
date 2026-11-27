Desvios em relação ao protocolo registrado na Parte 1 (commit de 11/11/2026). Cada desvio: o que mudou, quando, por quê e o impacto na análise.

| Data | O que mudou | Por quê | Impacto na análise |
| --- | --- | --- | --- |
| 19/11 | Convite não neutro em um grupo de WhatsApp (sem alunos desta disciplina): "me ajudem a fazer o trabalho de medição e experimentação? Respondam esse quiz rapidinho". O protocolo previa um convite neutro, sem pedir favor. | Divulgação informal, escrita às pressas. | Possível viés de desejabilidade social e de autosseleção: quem responde para ajudar um colega pode responder como imagina que ajuda o grupo. A exportação não permite saber quantas respostas vieram desse convite; na exportação, nenhuma resposta chegou entre 19/11 18:54 e 26/11 21:56. |
| 22/11 a 26/11 | Coleta prorrogada até 26/11; o protocolo previa encerrar em 22/11, com prorrogação máxima até 24/11. A prorrogação foi autorizada pelo professor da disciplina. | Em 22/11 havia 11 respostas válidas, bem abaixo do mínimo de 50. | 33 das 44 respostas válidas chegaram depois de 22/11 (uma em 26/11 à tarde e 32 na noite de 26/11). |
| 26/11 | Formulário mantido aberto depois da data final prevista. | Mesma razão da linha anterior. | Mesmo impacto da linha anterior. |
| 26/11 | Canal novo, fora do plano de divulgação: o link foi apresentado em sala de aula por um professor de outra disciplina, e o grupo convidou diretamente profissionais (inclusive líderes técnicos) na mesma noite. | Os canais online previstos renderam poucas respostas. | 38 das 50 respostas recebidas chegaram entre 22h44 e 23h39 de 26/11. A pergunta P7 não tem opção "sala de aula", então não é possível separar com precisão os alunos dos convidados diretos. Ver ameaça à validade abaixo. |
| 26/11 | Amostra final de 44 respostas válidas, abaixo do mínimo de 50 do enunciado e da meta de 100 do protocolo. Número aceito pelo professor. | Baixa adesão nos canais online. | Margem de erro de ±14,8 p.p. no pior caso, em vez de ±9,8 p.p. Os testes têm menos poder do que o planejado (n ≈ 85 para ρ = 0,30); resultados não significativos não indicam ausência de efeito. |

**Ameaça à validade: concentração das respostas em uma única sessão.** 38 das 50 respostas recebidas (76%) e 32 das 44 válidas (73%) foram enviadas em uma janela de 55 minutos, na noite de 26/11. A maior parte veio de alunos de uma mesma sala, que responderam juntos. Nem todos eram alunos: na mesma noite, o grupo pediu respostas diretamente a outros profissionais, incluindo líderes técnicos. Isso traz três riscos:

- **Falta de independência entre respostas:** quem responde junto pode conversar sobre as perguntas ou se influenciar, e o contexto de sala (presença do professor, pressa) é o mesmo para todos.
- **Homogeneidade da amostra:** a maioria vem de um mesmo curso e de uma mesma rede de contatos, o que restringe ainda mais a generalização, já limitada pela amostragem por conveniência.
- **Atenção menor:** 5 das 6 respostas descartadas na sessão de 26/11 erraram a pergunta de atenção (13% da sessão, contra nenhuma nas 12 respostas anteriores), o que sugere preenchimento mais rápido. As regras D3 e D4 removem os casos detectáveis, mas não os descuidos parciais.

**Análise da QP4 (H4b):** o índice de práticas de verificação teve α = 0,41, abaixo de 0,60. Pela regra pré-registrada, o índice não foi usado e cada item (PV1, PV2, PV3) foi correlacionado com o índice DC. O protocolo não dizia como contar esses testes na correção de Holm; adotamos a opção mais conservadora, com os três na família confirmatória, que passou de 6 para 8 testes.

**Mitigação e forma de relato:** os resultados são apresentados como exploratórios, com a margem de erro em destaque; o perfil da amostra mostra a distribuição das respostas ao longo da coleta; e as conclusões não são generalizadas para todos os desenvolvedores.

**Concordância da codificação das respostas abertas:** kappa de Cohen geral = 0,62 (concordância substancial) nas primeiras 20 respostas (R002 a R049), calculado por `codificacao.py kappa`. Codificaram, à mão e de forma independente, Murilo Andrade e Pedro Luiz Nato. Kappa por código: PRODUTO_DOMINIO 0,90; VERIFICACAO 0,63; QUALIDADE_EQUIPE 0,62; GANHO_CODIGO 0,61; PERDA_COMPREENSAO 0,58; DEPENDENCIA 0,47; PAPEL_SATISFACAO e OUTRO 0,00.

Desvios na codificação:

- Como há só 21 respostas abertas, os dois codificaram as 21 de forma independente, em vez de codificar a restante só depois do consenso, como previa o protocolo; o kappa continua calculado nas primeiras 20.
- Foram incluídos dois códigos emergentes, PAPEL_SATISFACAO e QUALIDADE_EQUIPE, além dos seis pré-registrados. A decisão de usá-los não foi alinhada entre os codificadores antes do início: PAPEL_SATISFACAO foi marcado 6 vezes por um e nenhuma pelo outro, o que explica o kappa de 0,00 nesse código e 6 das 28 divergências. Depois do cálculo do kappa, o grupo manteve o código e deixou sua definição mais precisa no livro de códigos ("mudança de papel": o foco do trabalho sai do código e vai para produto, arquitetura, planejamento ou gestão, ou o contrário).
- Regra de consenso definida pelo grupo depois do kappa: quando a divergência é entre `OUTRO` e um código específico, vale o código específico. A regra resolveu 4 das 28 células divergentes (R014 e R050); as outras 24 foram decididas pelo grupo uma a uma antes de gerar a codificação final.

# Livro de códigos: pergunta aberta A1

Pergunta: "Descreva uma situação em que o uso de IA afetou, para melhor ou para pior, sua compreensão do código ou do produto."

Regras (seção 5 do protocolo):

- Dois integrantes codificam de forma **independente**: cada um usa só a própria planilha e não conversa sobre as respostas antes de terminar.
- Uma resposta pode receber **mais de um código**. Marque 1 na coluna de cada código que se aplica e deixe as outras em branco.
- O kappa de Cohen é calculado nas primeiras 20 respostas (em ordem de ID). Depois, as divergências são resolvidas em consenso.
- Se a resposta não se encaixar em nenhum código, marque `OUTRO` e explique na coluna `observacao`.

## Códigos iniciais (pré-registrados)

| Código | Definição | Aplica quando a resposta… | Não aplica quando… |
| --- | --- | --- | --- |
| `PERDA_COMPREENSAO` | Perda de compreensão do código | diz que a pessoa não entende, não consegue explicar ou não sabe onde está algo no código produzido com IA; o código virou "caixa preta" | a dificuldade é só de ferramenta ou de prazo, sem relação com entender o código |
| `GANHO_CODIGO` | Ganho de compreensão do código | diz que a IA ajudou a entender código, fluxo, arquitetura ou dependências técnicas | o ganho citado é só sobre regras de negócio (use `PRODUTO_DOMINIO`) |
| `PRODUTO_DOMINIO` | Aprendizado do domínio ou do produto | diz que a IA ajudou a entender regras de negócio, requisitos, funcionalidades ou a visão do produto | o ganho é só técnico (use `GANHO_CODIGO`) |
| `DEPENDENCIA` | Dependência da IA | diz que a pessoa precisa da IA para entender ou agir, delega o raciocínio, deixou de revisar, ou sente que só aciona a ferramenta | a pessoa usa a IA, mas descreve controle próprio sobre o resultado |
| `VERIFICACAO` | Estratégias de verificação | descreve uma prática para checar ou entender o código gerado: pedir explicação, revisar, testar, perguntar ao time, escrever à mão | a resposta só menciona testes ou revisão sem dizer que foram usados para verificar |
| `OUTRO` | Outro tema | nenhum código acima se aplica | — |

## Códigos emergentes (decidir antes de começar)

O protocolo permite incluir novos códigos. Ao ler as respostas, dois temas aparecem com frequência e não cabem bem nos códigos iniciais. O grupo decide **antes da codificação** se os usa; se não usar, deixe as colunas em branco e use `OUTRO`.

| Código | Definição | Aplica quando a resposta… |
| --- | --- | --- |
| `PAPEL_SATISFACAO` | Mudança de papel ou de satisfação com o trabalho | fala de mudança no que a pessoa faz (programar menos, pensar mais no produto ou na arquitetura) ou de gostar mais ou menos do trabalho |
| `QUALIDADE_EQUIPE` | Efeitos na qualidade ou no processo da equipe | fala de erros, qualidade, PRs ou comportamento de outras pessoas da equipe ou da empresa, e não da própria compreensão |

Qualquer código incluído depois do início da codificação deve ser registrado em `desvios.md`.

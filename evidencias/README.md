# Evidências da coleta (Parte 2)

O enunciado pede ao menos uma evidência. Usamos **registros digitais**: exportação bruta com data e hora de cada resposta, capturas datadas dos canais de divulgação e acesso ao painel do formulário durante a apresentação. Nenhuma evidência pode expor dados pessoais dos respondentes.

Esta pasta, no repositório público, guarda só este roteiro. Capturas e exportações ficam no Google Drive do grupo, com acesso restrito aos integrantes e ao professor.

## 1. Exportação bruta

| Item | Valor |
| --- | --- |
| Arquivo | `Respostas — Uso de IA e conhecimento do código.xlsx` (Forms → Respostas → Baixar respostas) |
| Exportado em | 26/11/2026, 23:39 |
| Respostas | 50 recebidas, de 15/11/2026 20:29 a 26/11/2026 23:38 |
| SHA-256 | `f7e4e5c51fc001a21f1758825e46ebb402d15a1373f4cb8f5ed5ddf1d7126b83` |

O hash permite mostrar que o arquivo usado no dashboard é o mesmo baixado do Forms (no Windows: `certutil -hashfile "<arquivo>" SHA256`). Se a exportação for refeita, o hash muda: atualize esta tabela.

## 2. Painel do formulário (ao vivo)

Formulário: "Uso de IA e conhecimento do código — pesquisa acadêmica", conta do grupo. Na apresentação, abrir a aba **Respostas** e mostrar:

- o total de respostas, que deve bater com "Respostas recebidas" no dashboard;
- o resumo de uma pergunta (por exemplo P1), para comparar com o perfil da amostra;
- a vista **Individual** de uma resposta, com data e hora.

Antes da apresentação, apagar o formulário "Cópia de Uso de IA e conhecimento do código", que tem 0 respostas, para não haver dúvida sobre qual é o formulário da coleta.

## 3. Capturas datadas da divulgação

Capturas do WhatsApp guardadas no Drive do grupo. No WhatsApp, o separador de data aparece **acima** das mensagens daquele dia; as datas abaixo foram lidas assim.

| Captura | Data e hora | Canal | Como a data aparece |
| --- | --- | --- | --- |
| 1 | Até 17/11, 23:06 | Conversa com o professor de outra disciplina, que se ofereceu para passar o link a alunos de graduação | Separador "18/11/2026" logo abaixo da mensagem: ela é do dia anterior ou antes |
| 2 | 19/11, 18:54 | Grupo de WhatsApp sem alunos desta disciplina ("@all me ajudem… respondam esse quiz rapidinho") | Separador "19/11/2026" acima da mensagem |
| 3 | Sem data visível, 20:11 | Grupo de WhatsApp ("Respondam") | Só o horário; a captura não mostra a data |
| 4 | 26/11, 22:57 | Link repassado por um amigo do grupo a colegas do 6º período ("trabalho de uns amigos meus") | "Yesterday" em captura feita em 27/11 |

**O que as capturas mostram e o que não mostram.** Uma captura não prova quem respondeu nem quando cada pessoa respondeu. Ela prova a partir de quando o link circulou em cada canal: nenhuma resposta daquele canal pode ser anterior à mensagem. É por isso que o enunciado pede capturas datadas.

**Cruzamento com a exportação.** As respostas chegaram em 15/11 (1), 17/11 (9, entre 19:01 e 20:17), 19/11 (1, às 13:50) e 26/11 (39, entre 21:56 e 23:39). A concentração de 26/11 coincide com a captura 4 e com os convites diretos feitos na mesma noite; segundo o grupo, as primeiras respostas daquela noite (16 entre 22:44 e 23:06, a partir de antes do repasse das 22:57) vieram dos convites diretos, dos quais não há captura. A captura 2 (19/11) não foi seguida de respostas até 26/11.

Canais previstos no protocolo sem captura: LinkedIn, Discord, Reddit r/brdev e TabNews. Algumas respostas marcaram LinkedIn (3) e "Discord, Reddit ou fóruns" (3) em P7; se houver publicações nesses canais, acrescentem as capturas, e se não houver, registrem em `dashboard/desvios.md` que esses canais não foram usados pelo grupo.

## 4. Linha do tempo (gerada pelo dashboard)

A página "Perfil da amostra" mostra as respostas ao longo da coleta, com as datas de início e de fim previstas. É ela que mostra a concentração de 38 respostas na noite de 26/11, declarada como ameaça à validade.

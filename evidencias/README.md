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

Uma captura por divulgação, com data e hora visíveis. Antes de guardar, cubra nomes, fotos e números de telefone de outras pessoas.

| Data | Canal | Captura (arquivo no Drive) | Feita? |
| --- | --- | --- | --- |
| 14/11 | LinkedIn dos integrantes | | |
| 14/11 | Grupos de WhatsApp/Telegram | | |
| 14/11 | Discord, Reddit r/brdev, TabNews | | |
| 17/11 | Lembrete | | |
| 20/11 | Lembrete | | |
| 26/11 | Apresentação em sala (professor de outra disciplina) | | |
| 26/11 | Convites diretos a profissionais | | |

Apaguem as linhas dos canais que não foram usados, e registrem em `dashboard/desvios.md` qualquer canal previsto que não tenha sido usado.

## 4. Linha do tempo (gerada pelo dashboard)

A página "Perfil da amostra" mostra as respostas ao longo da coleta, com as datas de início e de fim previstas. É ela que mostra a concentração de 38 respostas na noite de 26/11, declarada como ameaça à validade.

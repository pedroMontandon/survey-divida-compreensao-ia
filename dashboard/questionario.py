"""Especificação do questionário e do protocolo (Parte 1).

Tudo o que o dashboard sabe sobre o instrumento está aqui. Os textos das opções
precisam ser idênticos aos do formulário (formulario/criar_formulario.gs).
Se o pré-teste mudar algum texto, atualize os dois arquivos e declare o desvio
em desvios.md.
"""

from datetime import date

# ---------------------------------------------------------------- protocolo
DATA_INICIO_COLETA = date(2026, 11, 14)   # respostas anteriores = pré-teste (regra D0)
DATA_FIM_COLETA = date(2026, 11, 22)      # prorrogável até 24/11 se n < 50 em 19/11
DATA_ENTREGA_FINAL = date(2026, 11, 27)
META_VALIDAS = 100
MINIMO_VALIDAS = 50
ALFA = 0.05
MIN_SEGMENTO = 5                          # segmentos menores são ocultados

# ---------------------------------------------------------------- opções
SIM_NAO = ["Sim", "Não"]
CONSENTIMENTO_SIM = "Li e concordo em participar"

LIKERT = ["Discordo totalmente", "Discordo", "Nem concordo nem discordo",
          "Concordo", "Concordo totalmente"]
FREQUENCIA = ["Nunca", "Raramente", "Às vezes", "Frequentemente", "Sempre"]
MUDANCA = ["Diminuiu muito", "Diminuiu um pouco", "Não mudou",
           "Aumentou um pouco", "Aumentou muito"]

OPCOES = {
    "P1": ["Menos de 1 ano", "De 1 a 2 anos", "De 3 a 5 anos",
           "De 6 a 9 anos", "10 anos ou mais"],
    "P2": ["Estagiário(a)", "Desenvolvedor(a) júnior", "Desenvolvedor(a) pleno(a)",
           "Desenvolvedor(a) sênior",
           "Liderança técnica (tech lead, especialista ou arquiteto(a))", "Outro"],
    "P3": ["Até 9 pessoas", "10 a 49 pessoas", "50 a 249 pessoas", "250 a 999 pessoas",
           "1.000 pessoas ou mais", "Não sei"],
    "P4": ["Menos de 6 meses", "De 6 a 11 meses", "De 1 a 2 anos",
           "De 3 a 4 anos", "5 anos ou mais"],
    "P5": ["Empresa de produto de software", "Startup", "Consultoria ou fábrica de software",
           "TI interna de empresa de outro setor", "Setor público", "Autônomo(a) ou freelancer",
           "Outro"],
    "P6": ["Sim, sempre", "Sim, em alguns casos", "Não"],
    "P7": ["LinkedIn", "WhatsApp ou Telegram", "Discord, Reddit ou fóruns",
           "Indicação de colega", "Outro"],
    "U1": ["Menos de uma vez por semana", "Algumas vezes por semana", "Diariamente",
           "Várias vezes ao dia"],
    "U2": ["0% a 20%", "21% a 40%", "41% a 60%", "61% a 80%", "81% a 100%"],
    "U3": ["Autocompletar no editor", "Chat (perguntas e trechos de código)",
           "Agentes que editam vários arquivos ou executam tarefas"],
    "U4": ["GitHub Copilot", "ChatGPT", "Claude / Claude Code", "Cursor", "Gemini"],
}
for cod in ("G1", "G2"):
    OPCOES[cod] = MUDANCA
for cod in ("DC1", "DC2", "DC3", "DC4", "DC5", "ATT1", "CP1", "CP2", "CP3", "CP4"):
    OPCOES[cod] = LIKERT
for cod in ("PV1", "PV2", "PV3"):
    OPCOES[cod] = FREQUENCIA

# Itens com escore numérico (posição 1..k na lista de opções)
ORDINAIS = ["P1", "P3", "P4", "U1", "U2", "G1", "G2",
            "DC1", "DC2", "DC3", "DC4", "DC5", "ATT1",
            "CP1", "CP2", "CP3", "CP4", "PV1", "PV2", "PV3"]
NAO_ORDINAL = {"P3": "Não sei"}   # opção sem posição na ordem

ROTULOS = {
    "P1": "Experiência profissional", "P2": "Cargo", "P3": "Porte da empresa",
    "P4": "Tempo na base de código atual", "P5": "Tipo de organização",
    "P6": "Code review obrigatório", "P7": "Canal de recebimento do link",
    "U1": "Frequência de uso de IA", "U2": "Parcela do código gerada por IA",
    "U3": "Forma de uso predominante", "U4": "Ferramentas usadas",
    "G1": "Conhecimento da base de código desde que usa IA",
    "G2": "Conhecimento do produto desde que usa IA",
    "DC1": "Há trechos que entreguei com IA que eu não conseguiria explicar",
    "DC2": "Mais dificuldade de localizar funcionalidades sem a IA",
    "DC3": "Consigo explicar a arquitetura sem consultar ferramentas (R)",
    "DC4": "Preciso da IA para entender bugs em código gerado",
    "DC5": "Conheço a base menos do que conheceria sem IA",
    "CP1": "A IA me ajudou a entender regras de negócio",
    "CP2": "Uso a IA para explorar partes desconhecidas do sistema",
    "CP3": "Compreendo melhor como as funcionalidades se relacionam",
    "CP4": "Respondo dúvidas sobre o produto com mais segurança",
    "PV1": "Leio e entendo todo o código antes de aceitar",
    "PV2": "Peço à IA que explique o código que não entendo",
    "PV3": "Aceito sugestões que funcionam sem entendê-las (R)",
}

# ---------------------------------------------------------------- construtos
CONSTRUTOS = {
    "DC": {"nome": "Dívida de compreensão", "itens": ["DC1", "DC2", "DC3", "DC4", "DC5"],
           "invertidos": ["DC3"], "escala": "Likert"},
    "CP": {"nome": "Conhecimento do produto", "itens": ["CP1", "CP2", "CP3", "CP4"],
           "invertidos": [], "escala": "Likert"},
    "PV": {"nome": "Práticas de verificação", "itens": ["PV1", "PV2", "PV3"],
           "invertidos": ["PV3"], "escala": "Frequência"},
}
ITENS_LINHA_RETA = ["DC1", "DC2", "DC3", "DC4", "DC5", "CP1", "CP2", "CP3", "CP4",
                    "PV1", "PV2", "PV3"]

# Itens obrigatórios para quem passou pela triagem (regra D6)
OBRIGATORIOS = ["P1", "P2", "P3", "P4", "P5", "P6", "P7", "U1", "U2", "U3", "U4",
                "G1", "G2", "DC1", "DC2", "DC3", "ATT1", "DC4", "DC5",
                "CP1", "CP2", "CP3", "CP4", "PV1", "PV2", "PV3"]

# Faixas de experiência pré-registradas (M5)
FAIXAS_EXPERIENCIA = {
    "Menos de 1 ano": "Até 2 anos",
    "De 1 a 2 anos": "Até 2 anos",
    "De 3 a 5 anos": "De 3 a 9 anos",
    "De 6 a 9 anos": "De 3 a 9 anos",
    "10 anos ou mais": "10 anos ou mais",
}
ORDEM_FAIXAS = ["Até 2 anos", "De 3 a 9 anos", "10 anos ou mais"]

REGRAS_DESCARTE = [
    ("D0", "Resposta anterior ao início da coleta (pré-teste)"),
    ("D1", "Não consentiu"),
    ("D2", "Fora da população (não trabalha com desenvolvimento ou não usou IA)"),
    ("D3", "Errou a pergunta de atenção"),
    ("D4", "Respostas em linha reta nos 12 itens DC, CP e PV"),
    ("D5", "Duplicata exata de resposta anterior"),
    ("D6", "Item obrigatório ausente"),
]

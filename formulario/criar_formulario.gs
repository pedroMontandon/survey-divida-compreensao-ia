/**
 * Cria o questionário "Uso de IA e conhecimento do código" no Google Forms.
 *
 * Como usar:
 *   1. Acesse https://script.google.com e crie um projeto novo.
 *   2. Cole este arquivo inteiro no editor (substituindo o conteúdo de Code.gs).
 *   3. Ajuste CONTATO_GRUPO abaixo.
 *   4. Selecione a função criarFormulario e clique em "Executar". Autorize o acesso.
 *   5. Os links do formulário e da planilha aparecem no "Registro de execução".
 *
 * IMPORTANTE: os textos das opções são lidos pelo dashboard (dashboard/questionario.py).
 * Se mudar um texto aqui (por exemplo, após o pré-teste), mude também lá.
 * Cada título começa com o código do item entre colchetes: é assim que o dashboard
 * encontra as colunas na exportação.
 */

const CONTATO_GRUPO = '1515143@pucminas.edu.br';

const OPCOES = {
  sim_nao: ['Sim', 'Não'],
  P1: ['Menos de 1 ano', 'De 1 a 2 anos', 'De 3 a 5 anos',
       'De 6 a 9 anos', '10 anos ou mais'],
  P2: ['Estagiário(a)', 'Desenvolvedor(a) júnior', 'Desenvolvedor(a) pleno(a)',
       'Desenvolvedor(a) sênior', 'Liderança técnica (tech lead, especialista ou arquiteto(a))', 'Outro'],
  P3: ['Até 9 pessoas', '10 a 49 pessoas', '50 a 249 pessoas', '250 a 999 pessoas',
       '1.000 pessoas ou mais', 'Não sei'],
  P4: ['Menos de 6 meses', 'De 6 a 11 meses', 'De 1 a 2 anos',
       'De 3 a 4 anos', '5 anos ou mais'],
  P5: ['Empresa de produto de software', 'Startup', 'Consultoria ou fábrica de software',
       'TI interna de empresa de outro setor', 'Setor público', 'Autônomo(a) ou freelancer', 'Outro'],
  P6: ['Sim, sempre', 'Sim, em alguns casos', 'Não'],
  P7: ['LinkedIn', 'WhatsApp ou Telegram', 'Discord, Reddit ou fóruns', 'Indicação de colega', 'Outro'],
  U1: ['Menos de uma vez por semana', 'Algumas vezes por semana', 'Diariamente', 'Várias vezes ao dia'],
  U2: ['0% a 20%', '21% a 40%', '41% a 60%', '61% a 80%', '81% a 100%'],
  U3: ['Autocompletar no editor', 'Chat (perguntas e trechos de código)',
       'Agentes que editam vários arquivos ou executam tarefas'],
  U4: ['GitHub Copilot', 'ChatGPT', 'Claude / Claude Code', 'Cursor', 'Gemini'],
  mudanca: ['Diminuiu muito', 'Diminuiu um pouco', 'Não mudou', 'Aumentou um pouco', 'Aumentou muito'],
  likert: ['Discordo totalmente', 'Discordo', 'Nem concordo nem discordo', 'Concordo', 'Concordo totalmente'],
  frequencia: ['Nunca', 'Raramente', 'Às vezes', 'Frequentemente', 'Sempre'],
};

const TCLE = [
  'Convidamos você a participar de uma pesquisa acadêmica da disciplina Medição e Experimentação ',
  'em Engenharia de Software, do curso de Engenharia de Software da PUC Minas. O objetivo é entender como o uso ',
  'de assistentes de IA se relaciona com o conhecimento que desenvolvedores têm do código e do ',
  'produto em que trabalham.\n\n',
  '• Quem pode participar: pessoas que trabalham com desenvolvimento de software no Brasil ',
  '(incluindo estágio) e que usaram assistentes de IA em tarefas de código nos últimos 3 meses. ',
  'Se você cursa esta disciplina neste semestre, pedimos que não responda.\n',
  '• Tempo estimado: cerca de 7 minutos.\n',
  '• A participação é voluntária. Para desistir, a qualquer momento, basta fechar a página ',
  'sem enviar as respostas.\n',
  '• Não coletamos nome, e-mail, empresa nem qualquer outro dado que identifique você. Não há ',
  'respostas certas ou erradas; responda com sinceridade.\n',
  '• Os riscos são mínimos, semelhantes aos de atividades do dia a dia. Os dados serão usados ',
  'apenas de forma agregada e para fins acadêmicos, com acesso restrito ao grupo e ao professor, ',
  'conforme a LGPD.\n',
  '• Contato: ' + CONTATO_GRUPO,
].join('');

function criarFormulario() {
  const form = FormApp.create('Uso de IA e conhecimento do código — pesquisa acadêmica');
  form.setDescription('Pesquisa acadêmica sobre o uso de assistentes de IA no desenvolvimento de software. É anônima e leva cerca de 7 minutos.');
  form.setCollectEmail(false);
  form.setLimitOneResponsePerUser(false); // exigiria login e identificaria o respondente
  form.setAllowResponseEdits(false);
  form.setShowLinkToRespondAgain(false);
  form.setProgressBar(true);
  form.setConfirmationMessage(
    'Obrigado por participar! Se puder, repasse o link a outros desenvolvedores que usam IA no trabalho — isso nos ajuda muito.');
  try { form.setRequireLogin(false); } catch (e) { /* disponível só em contas Workspace */ }

  // --- Seção 1: consentimento ---------------------------------------------------
  form.addSectionHeaderItem().setTitle('Termo de consentimento').setHelpText(TCLE);
  const cons = form.addMultipleChoiceItem().setTitle('[CONS] Você concorda em participar?').setRequired(true);

  // --- Seções 2 e 3: triagem (uma pergunta por seção para permitir o desvio) -----
  const pgT1 = form.addPageBreakItem().setTitle('Triagem');
  const t1 = form.addMultipleChoiceItem().setRequired(true)
    .setTitle('[T1] Atualmente, você trabalha com desenvolvimento de software (incluindo estágio)?');
  const pgT2 = form.addPageBreakItem().setTitle('Triagem');
  const t2 = form.addMultipleChoiceItem().setRequired(true)
    .setTitle('[T2] Nos últimos 3 meses, você usou assistentes de IA (como Copilot, ChatGPT, Claude ou Cursor) para programar no trabalho?');

  // --- Seção 4: perfil --------------------------------------------------------------
  const pgPerfil = form.addPageBreakItem().setTitle('Sobre você e seu trabalho');
  escolha(form, '[P1] Há quanto tempo você trabalha com desenvolvimento de software, contando estágio?', OPCOES.P1);
  escolha(form, '[P2] Qual é o seu cargo ou função atual?', OPCOES.P2);
  escolha(form, '[P3] Quantas pessoas trabalham na empresa ou organização onde você atua?', OPCOES.P3);
  escolha(form, '[P4] Há quanto tempo você trabalha no sistema (base de código) em que atua hoje?', OPCOES.P4);
  escolha(form, '[P5] Em que tipo de organização você trabalha?', OPCOES.P5);
  escolha(form, '[P6] Na sua equipe, o código precisa ser revisado por outra pessoa (code review) antes do merge?', OPCOES.P6);
  escolha(form, '[P7] Por onde você recebeu o link deste questionário?', OPCOES.P7);

  // --- Seção 5: uso de IA -------------------------------------------------------------
  form.addPageBreakItem().setTitle('Seu uso de assistentes de IA');
  escolha(form, '[U1] Com que frequência você usa assistentes de IA para programar?', OPCOES.U1);
  escolha(form, '[U2] No último mês, que parte do código que você entregou foi escrita total ou principalmente por IA? (estimativa)', OPCOES.U2);
  escolha(form, '[U3] De que forma você mais usa IA no trabalho?', OPCOES.U3);
  form.addCheckboxItem().setTitle('[U4] Quais ferramentas de IA você usa? (marque todas as que se aplicam)')
    .setChoiceValues(OPCOES.U4).showOtherOption(true).setRequired(true);

  // --- Seção 6: avaliação global (antes dos blocos específicos) -----------------------
  form.addPageBreakItem().setTitle('Avaliação geral')
    .setHelpText('Pense no período desde que você passou a usar assistentes de IA no trabalho.');
  escolha(form, '[G1] Desde que passei a usar IA, meu conhecimento da base de código em que trabalho…', OPCOES.mudanca);
  escolha(form, '[G2] Desde que passei a usar IA, meu conhecimento do produto da empresa (regras de negócio, funcionalidades)…', OPCOES.mudanca);

  // --- Seção 7: compreensão da base de código (DC) + pergunta de atenção --------------
  form.addPageBreakItem().setTitle('Você e a base de código')
    .setHelpText('Indique o quanto você concorda com cada afirmação.');
  escolha(form, '[DC1] Há trechos de código que entreguei com ajuda de IA que eu não conseguiria explicar em detalhe a um colega.', OPCOES.likert);
  escolha(form, '[DC2] Quando preciso alterar algo, tenho mais dificuldade de localizar onde a funcionalidade está implementada sem pedir ajuda à IA.', OPCOES.likert);
  escolha(form, '[DC3] Consigo explicar a arquitetura e o fluxo principal do sistema em que trabalho sem consultar ferramentas.', OPCOES.likert);
  escolha(form, '[ATT1] Para confirmar que você está lendo com atenção, marque "Discordo totalmente" nesta afirmação.', OPCOES.likert);
  escolha(form, '[DC4] Quando surge um bug em código gerado com IA, preciso recorrer à IA para entender o que o código faz.', OPCOES.likert);
  escolha(form, '[DC5] Sinto que conheço a base de código menos do que conheceria se tivesse escrito o código sem IA.', OPCOES.likert);

  // --- Seção 8: conhecimento do produto (CP) ------------------------------------------
  form.addPageBreakItem().setTitle('Você e o produto da empresa')
    .setHelpText('Indique o quanto você concorda com cada afirmação.');
  escolha(form, '[CP1] A IA me ajudou a entender regras de negócio do produto da empresa.', OPCOES.likert);
  escolha(form, '[CP2] Uso a IA para explorar e entender partes do sistema que eu ainda não conhecia.', OPCOES.likert);
  escolha(form, '[CP3] Com o uso de IA, passei a compreender melhor como as funcionalidades do produto se relacionam.', OPCOES.likert);
  escolha(form, '[CP4] Com ajuda da IA, consigo responder dúvidas de colegas ou da área de negócio sobre o produto com mais segurança.', OPCOES.likert);

  // --- Seção 9: práticas de verificação (PV) + aberta --------------------------------
  form.addPageBreakItem().setTitle('Como você lida com o código gerado')
    .setHelpText('Com que frequência você faz cada coisa?');
  escolha(form, '[PV1] Leio e entendo todo o código sugerido pela IA antes de aceitá-lo.', OPCOES.frequencia);
  escolha(form, '[PV2] Peço à IA que explique o código gerado quando não o entendo.', OPCOES.frequencia);
  escolha(form, '[PV3] Aceito sugestões da IA que funcionam mesmo sem entender completamente como funcionam.', OPCOES.frequencia);
  form.addParagraphTextItem().setRequired(false)
    .setTitle('[A1] (Opcional) Descreva uma situação em que o uso de IA afetou, para melhor ou para pior, sua compreensão do código ou do produto.')
    .setHelpText('Não cite nomes de pessoas, empresas ou clientes.');

  // --- Desvios: quem não está na população vai direto ao envio --------------------------
  const FIM = FormApp.PageNavigationType.SUBMIT;
  cons.setChoices([cons.createChoice('Li e concordo em participar', pgT1),
                   cons.createChoice('Não concordo', FIM)]);
  t1.setChoices([t1.createChoice('Sim', pgT2), t1.createChoice('Não', FIM)]);
  t2.setChoices([t2.createChoice('Sim', pgPerfil), t2.createChoice('Não', FIM)]);

  // --- Planilha de respostas ---------------------------------------------------------
  const planilha = SpreadsheetApp.create('Respostas — Uso de IA e conhecimento do código');
  form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());

  try { if (typeof form.setPublished === 'function') form.setPublished(true); } catch (e) { /* versões antigas */ }

  Logger.log('Formulário (editar): ' + form.getEditUrl());
  Logger.log('Formulário (responder): ' + form.getPublishedUrl());
  Logger.log('Planilha de respostas: ' + planilha.getUrl());
}

function escolha(form, titulo, opcoes) {
  return form.addMultipleChoiceItem().setTitle(titulo).setChoiceValues(opcoes).setRequired(true);
}

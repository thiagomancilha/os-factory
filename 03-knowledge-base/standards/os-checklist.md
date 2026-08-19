# .osFactory — Checklist Operacional (os-checklist.md)

## Propósito e princípio

Este checklist transforma as regras normativas de `03-knowledge-base/rules/os-rules.md` em verificações objetivas, aplicáveis a uma Especificação Funcional / Ordem de Serviço concreta.

**O checklist não substitui `os-rules.md`.** `os-rules.md` continua sendo a fonte normativa — define o que é obrigatório, recomendado, permitido ou proibido, e por quê. Este arquivo não repete o texto das 27 regras; converte cada regra aplicável numa pergunta de verificação prática. Sempre que possível, cada item cita o ID da regra correspondente, no formato:

`[ ] Nenhum requisito funcional foi inventado. (OS-CORE-001)`

Quando um item não cita ID, é porque se trata de uma verificação de qualidade documental sem uma regra normativa individual correspondente em `os-rules.md` — ainda assim relevante para decidir se a OS está pronta.

## Uso previsto

Este checklist serve para:

- revisão automática executada pelo `os-validator-agent`;
- revisão humana antes de aprovar uma OS;
- futura validação antes da geração do DOCX;
- revalidação após a correção de findings apontados numa rodada anterior.

---

## 1. Fontes e rastreabilidade

- [ ] Todos os insumos relevantes disponíveis para a demanda foram identificados e considerados. (OS-SOURCE-001)
- [ ] Nenhum insumo relevante foi ignorado silenciosamente. (OS-SOURCE-001)
- [ ] Toda afirmação funcional relevante possui origem identificável (insumo original, `intake.md`, `functional-analysis.md` ou regra registrada). (OS-SOURCE-002)
- [ ] Não existe nenhum requisito classificado como `UNTRACEABLE_REQUIREMENT` sem revisão explícita. (OS-SOURCE-002)
- [ ] A cadeia `intake → análise funcional → OS` permanece coerente e rastreável entre as etapas. (OS-SOURCE-003)

## 2. Problema e situação atual

- [ ] O problema/necessidade original está corretamente representado, sem distorção. (OS-CORE-001)
- [ ] A Situação Atual possui suporte explícito nos insumos. (OS-SOURCE-002)
- [ ] A Situação Atual não descreve, como comportamento vigente, algo que só existirá após a mudança proposta. (OS-FUNC-001)

## 3. Escopo

- [ ] O escopo documentado corresponde à demanda identificada na análise funcional. (OS-SCOPE-001)
- [ ] Não há ampliação de escopo não confirmada pelos insumos. (OS-SCOPE-001)
- [ ] Nenhum requisito importante identificado na análise funcional foi perdido na documentação. (OS-SOURCE-003)
- [ ] Quando aplicável, o Escopo declara explicitamente o comportamento atual, o comportamento futuro e o delta entre eles. (OS-FUNC-001)

## 4. Regras funcionais

- [ ] Regras de negócio confirmadas pelos insumos estão documentadas. (OS-CORE-001)
- [ ] Cada regra deixa clara a condição de disparo. (OS-FUNC-002)
- [ ] Cada regra deixa claro o comportamento esperado do sistema. (OS-FUNC-002)
- [ ] Exceções conhecidas nos insumos foram preservadas na regra correspondente. (OS-FUNC-002)
- [ ] Regras com múltiplas dimensões estão organizadas de forma compreensível, não como lista plana sem agrupamento.

## 5. Mensagens e validações

- [ ] Mensagens fornecidas explicitamente pelos insumos foram preservadas exatamente, sem paráfrase. (OS-FUNC-003)
- [ ] Nenhuma mensagem do sistema foi inventada. (OS-FUNC-003)
- [ ] Mensagens necessárias, mas ainda não definidas nos insumos, permanecem registradas como `OPEN_QUESTION`. (OS-FUNC-003 / OS-UNCERTAINTY-002)

## 6. Integrações

Validar somente quando houver integração aplicável à demanda:

- [ ] A integração documentada possui evidência explícita nos insumos. (OS-FUNC-004)
- [ ] O sistema de origem está claramente identificado. (OS-FUNC-004)
- [ ] A informação ou ação propagada está clara. (OS-FUNC-004)
- [ ] O sistema de destino está claramente identificado. (OS-FUNC-004)
- [ ] O comportamento esperado no destino está documentado. (OS-FUNC-004)

## 7. Premissas e dependências

- [ ] Toda premissa/dependência possui relação concreta e identificável com a demanda. (OS-DOC-001)
- [ ] Nenhuma premissa/dependência é texto boilerplate genérico. (OS-DOC-001)
- [ ] Nenhuma premissa foi utilizada para introduzir escopo novo não confirmado. (OS-SCOPE-001)

## 8. Não Escopo

- [ ] Toda exclusão registrada possui suporte identificável nos insumos. (OS-SCOPE-002)
- [ ] Nenhuma exclusão foi inventada. (OS-SCOPE-002)
- [ ] O texto de Não Escopo não é boilerplate genérico. (OS-SCOPE-002)
- [ ] Não Escopo não contradiz o que foi declarado em Escopo. (OS-QA-001)

## 9. Incertezas

- [ ] Nenhuma `INFERENCE` aparece como `FACT`. (OS-UNCERTAINTY-001)
- [ ] Toda `OPEN_QUESTION` relevante permanece visível até ser respondida por fonte válida. (OS-UNCERTAINTY-002)
- [ ] Todo `CONFLICT` identificado permanece visível até resolução explícita. (OS-UNCERTAINTY-003)
- [ ] Nenhuma lacuna foi fechada silenciosamente. (OS-UNCERTAINTY-002 / OS-UNCERTAINTY-003)

## 10. Esforço

- [ ] O esforço não foi estimado ou inventado pela `.osFactory`. (OS-EFFORT-001)
- [ ] Valores de esforço presentes possuem fonte válida. (OS-EFFORT-001)
- [ ] O formato de apresentação do esforço, quando usado, é coerente com o contexto da demanda. (OS-EFFORT-002)
- [ ] Quando houver total informado, ele é matematicamente consistente com os itens somados.

## 11. Redação e terminologia

- [ ] Nomes oficiais de sistemas, objetos, campos, funcionalidades, botões e opções foram preservados. (OS-STYLE-001)
- [ ] O mesmo elemento é referenciado com o mesmo nome em todo o documento. (OS-STYLE-001)
- [ ] A linguagem é técnica, objetiva e não comercial. (OS-STYLE-002)
- [ ] Não há adjetivos de venda, promessas de benefício não suportadas ou afirmações genéricas sem suporte. (OS-STYLE-002)

## 12. Estrutura documental

- [ ] A estrutura segue, como referência (`SHOULD`, não obrigatoriedade universal), a ordem: Descrição → Situação Atual → Escopo → Premissas e Dependências → Não Escopo → Esforço. (OS-DOC-002)
- [ ] Seções condicionais (Regras, Observações, Validações, Mensagens, Integração, Exceções) aparecem somente quando fazem sentido para a demanda. (OS-DOC-003)
- [ ] Nenhuma seção foi criada artificialmente, preenchida apenas com boilerplate, só para seguir o esqueleto. (OS-DOC-001 / OS-DOC-003)
- [ ] A ordem e a estrutura do documento permanecem compreensíveis para quem revisa.

## 13. Figuras e evidências visuais

- [ ] Toda figura referenciada possui relação real com o texto ao redor.
- [ ] Toda figura possui legenda.
- [ ] Quando há múltiplas figuras, a legenda é numerada.
- [ ] Nenhuma figura ou print originário de documento real de cliente foi incorporado à base de conhecimento pública. (OS-PRIVACY-001)
- [ ] Nenhuma imagem foi adicionada apenas por estética, sem função de evidência.

## 14. Controle documental

Quando aplicável:

- [ ] O identificador da demanda está correto e consistente com a origem da solicitação.
- [ ] A versão do documento está correta.
- [ ] Uma nova revisão não reutiliza silenciosamente o mesmo número de versão da revisão anterior.
- [ ] Data, autoria e responsáveis só aparecem quando há informação válida disponível. (OS-CORE-001)
- [ ] Nenhum campo de controle documental foi preenchido com valor fictício. (OS-CORE-001)

## 15. Privacidade

- [ ] Nenhum dado real de cliente foi levado para arquivos versionados da factory. (OS-PRIVACY-001 / OS-PRIVACY-002)
- [ ] Não existem nomes pessoais, números de contrato, identificadores reais ou prints de cliente em `02-agents/`, `03-knowledge-base/` ou `04-templates/`. (OS-PRIVACY-001 / OS-PRIVACY-002)
- [ ] Exemplos versionados são genéricos/sanitizados, sem conteúdo proprietário desnecessário. (OS-PRIVACY-001)

---

## Gate de aprovação

A OS deve ser classificada como `BLOCKED` se existir pelo menos uma das condições abaixo:

- [ ] `UNTRACEABLE_REQUIREMENT` presente. (OS-SOURCE-002 / OS-QA-001)
- [ ] Requisito inventado, sem suporte nos insumos. (OS-CORE-001 / OS-QA-001)
- [ ] Ampliação de escopo não confirmada. (OS-SCOPE-001 / OS-QA-001)
- [ ] `OPEN_QUESTION` crítica ainda sem resposta. (OS-UNCERTAINTY-002 / OS-QA-001)
- [ ] `CONFLICT` funcional relevante não resolvido. (OS-UNCERTAINTY-003 / OS-QA-001)
- [ ] Regra necessária para implementação ainda indefinida. (OS-QA-001)
- [ ] Esforço inventado ou sem origem válida. (OS-EFFORT-001 / OS-QA-001)
- [ ] Violação relevante de privacidade (dado de cliente em área versionada). (OS-PRIVACY-001 / OS-PRIVACY-002)

Qualquer uma dessas condições, isoladamente, é suficiente para bloquear a aprovação — não é necessário acumular mais de uma.

## Classificação final

A execução deste checklist deve permitir chegar a uma das três classificações já definidas no `os-validator-agent`:

- **`PASS`** — nenhum bloqueio do Gate de aprovação e nenhum problema relevante pendente nas 15 dimensões.
- **`PASS_WITH_WARNINGS`** — nenhum bloqueio do Gate de aprovação, mas existem ajustes não impeditivos identificados nas 15 dimensões.
- **`BLOCKED`** — existe pelo menos uma condição do Gate de aprovação presente.

---

## Checklist mínimo de fechamento

Versão resumida para uso rápido, após a verificação completa acima já ter sido feita pelo menos uma vez:

- [ ] Problema corretamente representado
- [ ] Situação atual suportada
- [ ] Escopo rastreável
- [ ] Nenhum escopo adicional
- [ ] Regras funcionais preservadas
- [ ] Mensagens preservadas quando fornecidas
- [ ] Integrações documentadas quando aplicáveis
- [ ] Premissas/dependências específicas
- [ ] Não Escopo suportado
- [ ] Nenhuma inferência apresentada como fato
- [ ] Open Questions tratadas corretamente
- [ ] Conflitos explicitados
- [ ] Esforço não inventado
- [ ] Terminologia consistente
- [ ] Documento testável
- [ ] Privacidade preservada
- [ ] Nenhuma condição bloqueante presente

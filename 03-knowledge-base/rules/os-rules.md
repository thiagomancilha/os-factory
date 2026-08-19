# .osFactory — Regras Permanentes

Este documento consolida as regras oficiais da `.osFactory`. Todos os agentes — atuais e futuros — devem carregar e respeitar estas regras durante intake, análise funcional, documentação, validação, aprendizado de padrões e futura geração de outputs.

## Propósito

Ser a fonte normativa central da `.osFactory`: o lugar onde qualquer agente pode consultar o que pode afirmar, o que precisa perguntar, como controlar escopo, como documentar regras e quando bloquear uma OS. Nenhum agente deve reimplementar, por conta própria, um princípio já definido aqui.

## Escopo de aplicação

Aplica-se a todos os agentes hoje existentes — `os-intake-agent`, `os-functional-analyst-agent`, `os-documenter-agent`, `os-validator-agent`, `os-pattern-learner-agent` — e a qualquer agente ou mecanismo de geração de output que venha a ser criado. Regras específicas de um único agente continuam vivendo no arquivo desse agente; este documento reúne apenas as regras transversais, válidas em mais de uma etapa do pipeline.

## Convenção dos IDs

Cada regra recebe um identificador `OS-<CATEGORIA>-<NNN>`, com `NNN` de três dígitos, sequencial dentro da categoria. IDs não devem ser reaproveitados nem renumerados quando uma regra for descontinuada — descontinuar uma regra é registrado como decisão explícita, não como remoção silenciosa.

## Classificação normativa das regras

Cada regra recebe uma classificação normativa, indicando sua força de aplicação:

- `MUST` — obrigatório. Violação é motivo de bloqueio (ver `OS-QA-001`).
- `SHOULD` — fortemente recomendado; desvio é aceitável quando justificado e registrado, mas não é o padrão esperado.
- `MAY` — permitido, à discrição do agente ou do contexto, sem exigir justificativa.
- `MUST_NOT` — proibido. Violação é motivo de bloqueio (ver `OS-QA-001`).

Esta classificação normativa (`MUST`/`SHOULD`/`MAY`/`MUST_NOT`) é distinta da classificação usada em `01-analysis/_os-models/pattern-analysis.md` (`MUST`/`SHOULD`/`OPTIONAL`/`CANONICAL_CANDIDATE`/`DO_NOT_ADOPT`), que descreve o quão bem suportado um achado empírico está pela amostra de modelos analisada. Quando uma regra deste arquivo deriva de um achado marcado como `CANONICAL_CANDIDATE`, sua classificação normativa aqui é `SHOULD`, nunca `MUST` — reservamos `MUST` para princípios já defensáveis independentemente do tamanho da amostra. Isso preserva, dentro deste arquivo, a distinção que o `os-pattern-learner-agent` fez entre frequência e obrigatoriedade.

## Origem de cada regra

Cada regra registra uma origem:

- `FACTORY_PRINCIPLE` — princípio de governança da `.osFactory` como um todo, não amarrado a um único agente.
- `AGENT_CONTRACT` — já estava definido, em algum grau, no contrato de um ou mais agentes existentes; este arquivo o formaliza como regra transversal.
- `EMPIRICAL_PATTERN` — deriva de achado registrado em `01-analysis/_os-models/pattern-analysis.md`. Quando a origem for empírica, o texto da regra nunca cita nome de cliente, arquivo real ou identificador de demanda — apenas o padrão.
- `QUALITY_IMPROVEMENT` — melhoria de qualidade deliberada, sem estar literalmente escrita em um agente nem derivada diretamente da amostra de modelos, mas justificada pelo objetivo da `.osFactory`.

---

## OS-CORE — Princípios centrais e governança

### OS-CORE-001 — Não inventar requisitos

**Classificação:** `MUST`

**Objetivo:** Garantir que toda afirmação funcional da `.osFactory` tenha origem real, nunca origem no próprio modelo.

**Regra:** Nenhum agente pode criar comportamento funcional, regra de negócio, validação, mensagem ou integração sem suporte identificável nos insumos (documentos, imagens, e-mails, prints, planilhas ou qualquer material fornecido para a demanda).

**Evitar:** Preencher lacunas com suposições plausíveis apresentadas como se fossem fato; completar uma regra incompleta "para o documento parecer pronto"; usar conhecimento genérico de domínio como substituto de evidência específica da demanda.

**Justificativa:** É o princípio fundador de toda a factory — está presente, com redação equivalente, em todos os cinco agentes já criados. Sem ele, a OS deixa de ser confiável como fonte de verdade do que foi pedido.

**Origem:** `AGENT_CONTRACT`

### OS-CORE-002 — Responsabilidade delimitada por agente

**Classificação:** `MUST`

**Objetivo:** Preservar a separação de responsabilidades entre as etapas do pipeline, evitando que um agente absorva silenciosamente a função de outro.

**Regra:** Cada agente deve operar somente dentro do papel definido em seu próprio arquivo em `02-agents/`. Em especial: o `os-intake-agent` não decide comportamento nem redige a OS; o `os-functional-analyst-agent` não redige o documento final; o `os-documenter-agent` não refaz a análise funcional nem resolve `OPEN_QUESTION` por conta própria; o `os-validator-agent` não reescreve a OS; o `os-pattern-learner-agent` não transforma achado em regra sem passar pelo fluxo de `OS-CORE-003`.

**Evitar:** Um agente "adiantar o trabalho" da etapa seguinte para parecer mais completo; um agente corrigir, por iniciativa própria, uma inconsistência que é responsabilidade de outro agente identificar.

**Justificativa:** A divisão em cinco agentes existe para que cada etapa seja auditável isoladamente. Se um agente ultrapassa seu papel, a rastreabilidade entre intake, análise, documentação e validação se perde.

**Origem:** `AGENT_CONTRACT`

### OS-CORE-003 — Aprendizado evolutivo de padrões

**Classificação:** `MUST`

**Objetivo:** Impedir que um padrão observado em poucos exemplos vire regra definitiva sem revisão humana.

**Regra:** Novos padrões encontrados pelo `os-pattern-learner-agent` em modelos futuros não se tornam regra automaticamente. Devem passar pelo fluxo: `observação → análise → recomendação → aprovação → inclusão em os-rules.md`. Somente após aprovação explícita um achado pode alterar este arquivo.

**Evitar:** Editar `os-rules.md` diretamente a partir de um `pattern-analysis.md` sem uma etapa de decisão explícita; tratar frequência alta numa amostra pequena como prova suficiente de obrigatoriedade.

**Justificativa:** Amostras de modelos reais tendem a ser pequenas e homogêneas (mesmo cliente, mesmo template). Promover automaticamente qualquer recorrência a regra universal arrisca fixar hábitos de um único cliente como se fossem padrão da `.osFactory`.

**Origem:** `FACTORY_PRINCIPLE`

### OS-CORE-004 — Este arquivo é fonte normativa obrigatória

**Classificação:** `MUST`

**Objetivo:** Garantir que todos os agentes consultem uma única fonte de verdade para regras transversais, em vez de reinterpretar princípios de forma divergente.

**Regra:** Todo agente da `.osFactory`, ao operar, deve considerar `os-rules.md` como referência carregada e vigente, junto das regras específicas do seu próprio arquivo em `02-agents/`. Quando houver conflito entre uma regra deste arquivo, uma regra específica de um agente, ou duas instruções normativas aplicáveis à mesma situação, o conflito deve ser registrado como `CONFLICT` — a mesma classificação usada para contradições entre insumos — e encaminhado para decisão explícita antes de seguir, sempre que o conflito afetar o resultado. `OPEN_DECISION` não deve ser usada nesse contexto: essa classificação é específica do processo de aprendizado/evolução de padrões do `os-pattern-learner-agent` (ver `OS-CORE-003`), não do pipeline operacional de intake, análise, documentação e validação.

**Evitar:** Agentes operando com entendimento próprio e divergente de um mesmo princípio (por exemplo, dois agentes com critérios diferentes do que conta como `OPEN_QUESTION`); classificar conflito normativo como `OPEN_DECISION`; resolver o conflito silenciosamente sem registrá-lo.

**Justificativa:** Consistência entre etapas depende de que todos os agentes compartilhem a mesma definição de conceitos centrais. O pipeline operacional já usa `FACT`/`INFERENCE`/`OPEN_QUESTION`/`CONFLICT` como vocabulário padrão (ver `OS-UNCERTAINTY-001` a `OS-UNCERTAINTY-003`); usar `OPEN_DECISION` para um caso fora do previsto pelo `os-pattern-learner-agent` misturaria dois vocabulários com propósitos distintos.

**Origem:** `FACTORY_PRINCIPLE`

---

## OS-SOURCE — Uso de insumos e rastreabilidade

### OS-SOURCE-001 — Leitura suficiente das fontes obrigatórias

**Classificação:** `MUST`

**Objetivo:** Evitar conclusões baseadas em leitura parcial ou superficial dos insumos, sem exigir leitura sequencial de conteúdo manifestamente irrelevante para a demanda.

**Regra:** Todos os insumos disponíveis para a etapa devem ser identificados e considerados. O agente deve ler integralmente o conteúdo relevante para sua etapa — não apenas nomes de arquivo, sumários, primeira página ou fragmentos insuficientes. Quando um documento for extenso, o agente pode localizar primeiro as partes relevantes, mas deve ler contexto suficiente ao redor delas para sustentar a conclusão. Nenhum insumo relevante pode ser ignorado silenciosamente. Isso vale tanto para os insumos originais em `00-inbox/<demanda>/` quanto para os artefatos intermediários gerados pelas etapas anteriores (`intake.md`, `functional-analysis.md`, `OS-<demanda>.md`).

**Evitar:** Concluir um padrão ou uma regra com base apenas no título de um documento ou na primeira página; descartar um insumo por parecer redundante sem antes considerá-lo; tratar uma leitura fragmentada e insuficiente como equivalente à leitura do conteúdo relevante; ignorar um insumo relevante sem registrar por que ele foi considerado não aplicável.

**Justificativa:** Todos os cinco agentes já declaram, em algum grau, a obrigação de ler suas fontes com profundidade; formalizar isso aqui evita tanto a leitura superficial quanto a exigência impraticável de leitura sequencial integral de documentos extensos com conteúdo majoritariamente irrelevante para a demanda.

**Origem:** `AGENT_CONTRACT`

### OS-SOURCE-002 — Rastreabilidade de toda afirmação relevante

**Classificação:** `MUST`

**Objetivo:** Garantir que qualquer leitor consiga verificar de onde veio cada afirmação funcional relevante da OS.

**Regra:** Toda afirmação funcional relevante — regra de negócio, comportamento esperado, integração, premissa, exclusão de escopo — deve poder ser relacionada a pelo menos uma fonte: um insumo original, o `intake.md`, o `functional-analysis.md`, ou uma regra explicitamente registrada nesta base de conhecimento. Quando não for possível localizar a origem, a afirmação deve ser classificada como `UNTRACEABLE_REQUIREMENT` (ver `OS-QA-001`).

**Evitar:** Afirmações funcionais "soltas", sem nenhuma fonte identificável, mesmo que pareçam plausíveis.

**Justificativa:** Rastreabilidade é o que permite auditar, mais tarde, se a OS final ainda representa fielmente o que foi pedido.

**Origem:** `FACTORY_PRINCIPLE`

### OS-SOURCE-003 — Cadeia de rastreabilidade entre etapas

**Classificação:** `SHOULD`

**Objetivo:** Preservar a rastreabilidade não só até o insumo original, mas também entre os artefatos intermediários de cada etapa.

**Regra:** Sempre que viável, cada artefato produzido por um agente (`intake.md`, `functional-analysis.md`, `OS-<demanda>.md`, `validation.md`) deve indicar de qual artefato da etapa anterior uma informação específica foi herdada, além da fonte original.

**Evitar:** Reescrever uma informação em uma nova etapa sem manter o vínculo com a etapa anterior, forçando quem revisa a recomeçar a busca pela origem do zero.

**Justificativa:** Reduz o custo de auditoria e de revisão humana ao longo do pipeline `intake → análise → documentação → validação`.

**Origem:** `AGENT_CONTRACT`

---

## OS-SCOPE — Escopo e controle de ampliação indevida

### OS-SCOPE-001 — Não ampliar escopo

**Classificação:** `MUST`

**Objetivo:** Impedir que uma necessidade limitada se transforme, ao longo do pipeline, em uma solução mais abrangente do que a demanda original.

**Regra:** A OS não pode transformar uma necessidade limitada em uma solução mais abrangente sem confirmação explícita nos insumos. Qualquer ampliação de escopo identificada em qualquer etapa deve ser registrada como `OPEN_QUESTION` ou `CONFLICT`, nunca incorporada silenciosamente ao escopo.

**Evitar:** Generalizar uma regra pontual em uma regra ampla "porque faz sentido"; estender uma mudança pedida para um cenário específico a cenários semelhantes não mencionados; usar analogia técnica para justificar escopo não solicitado.

**Justificativa:** Ampliação de escopo não confirmada é uma das causas mais diretas de retrabalho, estouro de esforço e insatisfação do solicitante.

**Origem:** `AGENT_CONTRACT`

### OS-SCOPE-002 — Não Escopo sem boilerplate

**Classificação:** `MUST`

**Objetivo:** Fazer da seção de Não Escopo uma ferramenta real de alinhamento de expectativa, não um texto de preenchimento.

**Regra:** Não inventar exclusões que não tenham relação com a demanda. Não utilizar texto genérico ("mudanças de cenário serão tratadas no fluxo usual de melhorias" ou equivalente) como substituto de uma análise real do que está fora do escopo desta demanda específica. Quando os insumos não permitirem definir não escopo específico, isso deve ser sinalizado como lacuna para revisão, não preenchido com texto artificial.

**Evitar:** Copiar, de demanda para demanda, o mesmo texto de "Não Escopo" independentemente do conteúdo técnico da demanda.

**Justificativa:** Em modelos reais analisados, a seção de Não Escopo apareceu em 100% dos casos, mas com conteúdo idêntico e genérico entre demandas tecnicamente muito diferentes — um anti-padrão que reduz o valor real da seção como instrumento de alinhamento.

**Origem:** `EMPIRICAL_PATTERN`

---

## OS-FUNC — Regras de especificação funcional

### OS-FUNC-001 — Delta funcional explícito

**Classificação:** `MUST`

**Objetivo:** Tornar o escopo da mudança inequívoco, mostrando não só o que passa a existir, mas o que já existia.

**Regra:** O Escopo deve, sempre que aplicável, deixar claro: o comportamento atual; o comportamento futuro; e o que efetivamente muda entre um e outro.

**Evitar:** Descrever apenas o comportamento futuro, deixando implícito o que já era possível antes; omitir o contraste quando ele é conhecido pelos insumos.

**Justificativa:** Nos três modelos reais analisados, o Escopo sempre declarou esse contraste explicitamente — é o padrão de redação mais consistente encontrado, e aumenta diretamente a testabilidade da especificação.

**Origem:** `EMPIRICAL_PATTERN`

### OS-FUNC-002 — Regras descritas como condição → comportamento → exceção

**Classificação:** `SHOULD`

**Objetivo:** Tornar cada regra de negócio verificável e reduzir ambiguidade de interpretação.

**Regra:** Sempre que os insumos permitirem, regras de negócio devem ser descritas no formato: condição de disparo → comportamento esperado do sistema → exceção (quando aplicável).

**Evitar:** Descrever regras como afirmações vagas sem condição explícita; misturar múltiplas condições e comportamentos no mesmo parágrafo sem separá-los.

**Justificativa:** É o padrão de redação de regras encontrado de forma consistente nos modelos reais analisados, e reduz a chance de desenvolvimento e QA interpretarem a regra de formas diferentes.

**Origem:** `EMPIRICAL_PATTERN`

### OS-FUNC-003 — Fidelidade das mensagens do sistema

**Classificação:** `MUST`

**Objetivo:** Preservar exatamente o que o sistema deve comunicar ao usuário, sem introduzir variação não autorizada.

**Regra:** Quando os insumos definirem explicitamente uma mensagem que o sistema deve apresentar (erro, bloqueio, confirmação), a OS deve preservar esse texto exatamente — não reinterpretar, não "melhorar" a redação, não parafrasear. Quando uma mensagem for necessária para a especificação, mas ainda não estiver definida nos insumos, ela deve ser registrada como `OPEN_QUESTION`, nunca inventada.

**Evitar:** Reescrever uma mensagem de erro "para ficar mais claro"; supor o texto de uma mensagem ainda não definida; omitir a necessidade de uma mensagem só porque ela não foi fornecida.

**Justificativa:** Mensagens de sistema costumam ser objeto de teste e de homologação direta; qualquer variação não autorizada gera divergência entre o que foi especificado e o que será implementado.

**Origem:** `EMPIRICAL_PATTERN`

### OS-FUNC-004 — Integrações apenas com evidência

**Classificação:** `SHOULD`

**Objetivo:** Impedir que integrações entre sistemas sejam descritas com base em suposição.

**Regra:** Integrações só devem ser documentadas quando houver evidência explícita nos insumos. Quando houver fluxo entre sistemas, o texto deve deixar claro: origem → informação/ação → destino → comportamento esperado.

**Evitar:** Presumir que uma mudança "provavelmente" afeta outro sistema sem evidência; descrever integração apenas do lado de quem envia a informação, omitindo o comportamento esperado do lado que recebe.

**Justificativa:** Nos modelos reais, integração é uma seção condicional — só aparece quando a demanda de fato propaga dado a um sistema externo — e sempre segue esse fluxo de dois movimentos (origem e destino).

**Origem:** `EMPIRICAL_PATTERN`

---

## OS-DOC — Estrutura e conteúdo documental

### OS-DOC-001 — Premissas e dependências sem boilerplate

**Classificação:** `MUST`

**Objetivo:** Fazer da seção de Premissas e Dependências um registro real de risco e dependência, não um texto de preenchimento.

**Regra:** Não utilizar texto boilerplate genérico apenas para preencher a seção de Premissas e Dependências. Toda premissa ou dependência registrada deve possuir relação concreta e identificável com a demanda específica sendo documentada.

**Evitar:** Repetir, de demanda para demanda, o mesmo texto genérico sobre "possibilidade de mudança de protótipo" ou "necessidade de revisar esforço em caso de alteração", sem premissas específicas da demanda em questão.

**Justificativa:** Nos três modelos reais analisados, o conteúdo desta seção era idêntico entre demandas tecnicamente muito diferentes — presença estrutural alta, mas sem nenhum valor analítico real. É o anti-padrão mais claro encontrado na amostra.

**Origem:** `EMPIRICAL_PATTERN`

### OS-DOC-002 — Estrutura canônica provisória

**Classificação:** `SHOULD`

**Objetivo:** Dar aos agentes um esqueleto documental de referência, sem prematuramente declará-lo definitivo.

**Regra:** A seguinte estrutura é registrada como `CANONICAL_CANDIDATE` — referência inicial da `.osFactory`, e não como regra universal fechada: `1. Descrição → 2. Situação Atual → 3. Escopo → 4. Premissas e Dependências → 5. Não Escopo → 6. Esforço`. Deve ser usada como padrão por padrão até que novos modelos, de outras origens além da amostra já analisada, permitam confirmar ou evoluir essa estrutura.

**Evitar:** Tratar esta ordem como imutável; adicionar ou remover seções da estrutura sem registrar a mudança como `OPEN_DECISION` para uma futura revisão deste arquivo.

**Justificativa:** A estrutura foi observada de forma consistente (3/3) numa amostra pequena e homogênea (mesmo cliente, mesmo template). Consistência interna alta não substitui validação externa — ver `OS-CORE-003`.

**Origem:** `EMPIRICAL_PATTERN`

### OS-DOC-003 — Seções condicionais existem apenas quando fazem sentido

**Classificação:** `SHOULD`

**Objetivo:** Evitar documentos inflados por seções vazias criadas só para seguir um template.

**Regra:** Subseções como Regras, Observações, Validações, Mensagens, Integração e Exceções devem existir somente quando fizerem sentido para a demanda em questão, com conteúdo real.

**Evitar:** Criar uma subseção vazia, ou preenchida com "não se aplica", apenas para manter a aparência de completude do template.

**Justificativa:** Nos modelos reais, o nome e a presença dessas subseções variavam conforme a natureza de cada demanda — nenhuma delas era universal; forçar sua presença sem conteúdo reduz a clareza do documento.

**Origem:** `EMPIRICAL_PATTERN`

---

## OS-STYLE — Redação e terminologia

### OS-STYLE-001 — Preservar terminologia oficial

**Classificação:** `MUST`

**Objetivo:** Evitar ambiguidade causada por nomes diferentes para o mesmo elemento.

**Regra:** Preservar os nomes oficiais usados nos insumos para sistemas, objetos, campos, funcionalidades, botões, opções e integrações. O mesmo elemento deve ter o mesmo nome em toda a OS.

**Evitar:** Traduzir, sinonimizar ou "melhorar" o nome de um elemento já nomeado nos insumos; usar dois nomes diferentes para o mesmo objeto em seções diferentes da OS.

**Justificativa:** Já é regra explícita em pelo menos três dos cinco agentes existentes (`os-intake-agent`, `os-functional-analyst-agent`, `os-documenter-agent`); formalizar aqui garante que futuros agentes herdem o mesmo compromisso.

**Origem:** `AGENT_CONTRACT`

### OS-STYLE-002 — Linguagem técnica, objetiva e não comercial

**Classificação:** `SHOULD`

**Objetivo:** Manter a OS como documento técnico de especificação, distinto de uma peça comercial.

**Regra:** A OS deve usar linguagem técnica e objetiva. Evitar linguagem de marketing, adjetivos de venda, promessas de benefício não suportadas pelos insumos e afirmações genéricas de valor.

**Evitar:** Frases como "solução robusta e inovadora"; benefícios de negócio não solicitados nem confirmados; qualquer redação que pareça peça de proposta comercial em vez de especificação técnica.

**Justificativa:** A `.osFactory` gera documentos internos/contratuais de escopo técnico, não peças de venda — diferente, por desenho, do padrão de redação comercial observado em uma factory irmã voltada a propostas.

**Origem:** `QUALITY_IMPROVEMENT`

---

## OS-UNCERTAINTY — Tratamento de OPEN_QUESTION, DISCOVERY_ITEM, INFERENCE e CONFLICT

### OS-UNCERTAINTY-001 — Separação entre fato e interpretação

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que uma interpretação razoável seja lida como se fosse um fato confirmado.

**Regra:** `INFERENCE` nunca pode ser apresentada como `FACT`. Toda informação relevante deve ser classificada como `FACT`, `INFERENCE`, `OPEN_QUESTION`, `DISCOVERY_ITEM` ou `CONFLICT`, conforme já definido nos agentes de intake e análise funcional (ver `OS-UNCERTAINTY-004` para o critério específico de `DISCOVERY_ITEM`).

**Evitar:** Redigir uma inferência com o mesmo tom afirmativo de um fato; omitir a marcação de incerteza "para o documento parecer mais pronto".

**Justificativa:** É a base do princípio central do `os-intake-agent`: primeiro compreender e registrar o que sabemos, depois identificar o que ainda precisamos descobrir.

**Origem:** `AGENT_CONTRACT`

### OS-UNCERTAINTY-002 — Open Questions permanecem visíveis

**Classificação:** `MUST`

**Objetivo:** Garantir que lacunas relevantes não desapareçam do documento antes de serem respondidas.

**Regra:** Lacunas relevantes devem permanecer explícitas, como `OPEN_QUESTION`, até serem efetivamente respondidas por uma fonte válida. Nenhum agente pode remover uma `OPEN_QUESTION` apenas para tornar a análise ou a OS aparentemente completa.

**Evitar:** Fechar uma `OPEN_QUESTION` por inferência silenciosa; omitir uma `OPEN_QUESTION` da versão final da OS só porque ela não foi respondida a tempo; reclassificar uma `OPEN_QUESTION` como `DISCOVERY_ITEM` apenas para que ela pareça resolvida ou para evitar bloqueio na validação (ver `OS-UNCERTAINTY-004`).

**Justificativa:** É regra explícita do `os-functional-analyst-agent` e do `os-documenter-agent`, e é o oposto direto do que se observou nos modelos reais analisados (documentos finais homologados, sem nenhuma marcação de incerteza) — a `.osFactory` decide, deliberadamente, expor a incerteza em vez de escondê-la.

**Origem:** `AGENT_CONTRACT`

### OS-UNCERTAINTY-003 — Conflitos nunca são resolvidos silenciosamente

**Classificação:** `MUST_NOT`

**Objetivo:** Preservar a visibilidade de contradições entre fontes até que sejam resolvidas de forma explícita.

**Regra:** Informações contraditórias entre diferentes insumos não podem ser resolvidas silenciosamente por um agente. Todo `CONFLICT` identificado deve ser registrado e permanecer visível até resolução explícita. Sempre que houver evidência suficiente, o `CONFLICT` deve ser classificado em um dos subtipos definidos em `OS-UNCERTAINTY-005` (`FUNCTIONAL_CONFLICT`, `ARCHITECTURAL_CONFLICT`, `DOCUMENTAL_CONFLICT`); na ausência dessa evidência, usar `CONFLICT_UNCLASSIFIED`.

**Evitar:** Escolher, sem justificativa registrada, qual das duas fontes contraditórias "deve estar certa"; omitir um conflito da OS final por parecer inconveniente; classificar o subtipo de um conflito por conveniência em vez de pelo impacto real da divergência (ver `OS-UNCERTAINTY-005`).

**Justificativa:** Resolver conflito silenciosamente equivale a inventar qual fonte é confiável — viola `OS-CORE-001` por decisão indireta.

**Origem:** `AGENT_CONTRACT`

### OS-UNCERTAINTY-004 — DISCOVERY_ITEM: diferimento controlado

**Classificação:** `MUST`

**Objetivo:** Distinguir formalmente uma lacuna que precisa ser respondida para fechar a especificação (`OPEN_QUESTION`) de uma informação cuja descoberta já está prevista, pelos próprios insumos, como parte de uma etapa futura do trabalho — evitando tanto o bloqueio desnecessário de demandas com fase de descoberta legítima quanto o uso indevido da classificação para mascarar decisões pendentes.

**Regra:** Uma pendência só pode ser classificada como `DISCOVERY_ITEM` quando todos os critérios abaixo forem satisfeitos: (1) existe evidência nos insumos de que uma etapa de descoberta, engenharia reversa ou refinamento faz parte do trabalho; (2) a informação pendente é exatamente do tipo que essa etapa está prevista para descobrir; (3) a ausência dessa informação não impede definir o objetivo e o limite funcional atual da demanda; (4) a informação não está sendo simplesmente omitida por falta de levantamento; (5) existe clareza suficiente sobre quando ou em qual etapa ela será resolvida. Quando possível, registrar também: etapa responsável pela descoberta, impacto esperado, condição de resolução e fallback conhecido (sem inventar um fallback que os insumos não definem). `DISCOVERY_ITEM` não é bloqueante automaticamente: o `os-validator-agent` deve avaliar cada item individualmente conforme o critério definido em seu próprio contrato, podendo manter `PASS` ou `PASS_WITH_WARNINGS` quando o item for válido e controlado, ou reclassificá-lo como `OPEN_QUESTION`/`CONFLICT` (gerando finding, e `BLOCKED` se crítico) quando não for.

**Evitar:** Classificar como `DISCOVERY_ITEM` uma decisão sobre comportamento do sistema, regra de negócio, cenário de escopo, mensagem obrigatória, integração, fonte contraditória a adotar, ou opção arquitetural necessária para fechar a contratação; transformar uma `OPEN_QUESTION` em `DISCOVERY_ITEM` apenas para que a OS passe pela validação; tratar um `CONFLICT` entre fontes como `DISCOVERY_ITEM`; inventar um fallback não suportado pelos insumos.

**Justificativa:** Identificada no primeiro teste ponta a ponta real da `.osFactory`: o vocabulário `FACT`/`INFERENCE`/`OPEN_QUESTION`/`CONFLICT` não distinguia uma lacuna que exige decisão humana de uma informação deliberadamente diferida para uma etapa de descoberta já prevista no próprio escopo da demanda (por exemplo, engenharia reversa de um banco legado). Sem essa distinção, demandas legitimamente exploratórias corriam o risco de ser bloqueadas por pendências que, na verdade, já fazem parte do trabalho planejado.

**Origem:** `QUALITY_IMPROVEMENT`

### OS-UNCERTAINTY-005 — Taxonomia de CONFLICT e gate por tipo

**Classificação:** `MUST`

**Objetivo:** Diferenciar o impacto de um `CONFLICT` no gate da OS conforme sua natureza, em vez de tratar toda divergência entre fontes com o mesmo peso.

**Regra:** Todo `CONFLICT` identificado deve, sempre que houver evidência suficiente, ser classificado em um dos três subtipos: `FUNCTIONAL_CONFLICT` — divergência que afeta diretamente regra de negócio, comportamento esperado, escopo, condição, exceção, validação, mensagem obrigatória, fluxo funcional ou critério de aceite; sempre `BLOCKED` enquanto não houver resolução explícita, sem que o agente escolha sozinho qual fonte prevalece. `ARCHITECTURAL_CONFLICT` — divergência sobre tecnologia, linguagem, framework, serviço dedicado versus módulo existente, componente, arquitetura, mecanismo técnico de integração ou autenticação, persistência, infraestrutura ou estratégia de implantação; pode permanecer `PASS_WITH_WARNINGS` quando o comportamento funcional estiver claro, a decisão técnica puder ser tomada em etapa de arquitetura/refinamento já prevista, ambas as alternativas atenderem ao escopo funcional atual e o esforço/prazo contratado não depender materialmente da escolha; deve ser `BLOCKED` quando a escolha alterar materialmente o escopo, mudar interfaces contratadas, alterar responsabilidades entre sistemas/equipes, alterar esforço ou prazo de forma relevante, contradizer premissa contratual já confirmada, ou quando a implementação não puder iniciar sem a decisão e não existir etapa anterior prevista para resolvê-la. `DOCUMENTAL_CONFLICT` — divergência em informação documental ou administrativa sem impacto funcional direto (datas, responsável, versão, identificação de documento, nomenclatura administrativa, referência de contrato, status documental, autoria); normalmente `PASS_WITH_WARNINGS`, podendo bloquear quando a informação for necessária para formalização ou aprovação da própria OS. Quando não houver informação suficiente para classificar, usar `CONFLICT_UNCLASSIFIED`, que nunca permite `PASS` e deve gerar finding para classificação antes da aprovação final; se a classificação for necessária para determinar o impacto, o resultado deve ser `BLOCKED`.

**Evitar:** Classificar um conflito funcional como arquitetural ou documental (ou vice-versa) apenas para evitar `BLOCKED` — a classificação deve considerar o impacto real da divergência, não apenas o assunto aparente (ex.: divergência sobre tecnologia normalmente é `ARCHITECTURAL_CONFLICT`, mas se uma tecnologia específica estiver contratualmente obrigatória e a outra fonte exigir outra arquitetura, o conflito pode ter impacto de escopo/contrato e tornar-se bloqueante); deixar um `CONFLICT_UNCLASSIFIED` sem finding associado; tratar `ARCHITECTURAL_CONFLICT` ou `DOCUMENTAL_CONFLICT` como automaticamente não bloqueante sem avaliar o critério específico.

**Justificativa:** Identificada após o primeiro teste real da `.osFactory` e a introdução de `DISCOVERY_ITEM`: nem todo `CONFLICT` tem o mesmo impacto no gate — um conflito puramente arquitetural (ex.: onde implementar um serviço) não deveria bloquear a OS da mesma forma que um conflito sobre o comportamento que o sistema deve ter, mas ambos precisam permanecer visíveis e nunca ser resolvidos silenciosamente.

**Origem:** `QUALITY_IMPROVEMENT`

---

## OS-EFFORT — Tratamento de esforço

### OS-EFFORT-001 — Nunca estimar ou inventar esforço

**Classificação:** `MUST`

**Objetivo:** Impedir que a `.osFactory` assuma, por conta própria, um papel de estimativa que não lhe cabe nesta fase.

**Regra:** A `.osFactory` não deve estimar ou inventar esforço durante a geração da especificação. Somente valores provenientes de fonte válida (por exemplo, uma estimativa formal já aprovada e informada como insumo) podem aparecer como esforço confirmado na OS.

**Evitar:** Preencher a tabela de esforço com valores "razoáveis" na ausência de fonte; usar a complexidade percebida da demanda como base para inventar um número.

**Justificativa:** Já é regra explícita do `os-documenter-agent` e condição de bloqueio do `os-validator-agent`; os três modelos reais analisados corroboram a prática — em nenhum deles o esforço estava preenchido na fase de especificação.

**Origem:** `AGENT_CONTRACT`

### OS-EFFORT-002 — Formato de tabela de esforço como referência inicial

**Classificação:** `SHOULD`

**Objetivo:** Padronizar a apresentação de esforço sem travar prematuramente um formato único.

**Regra:** Quando uma tabela de esforço for necessária, usar como referência inicial (`CANONICAL_CANDIDATE`) as linhas observadas na amostra analisada: Análise e Especificação, Desenvolvimento, Testes Internos, Gestão, Total.

**Evitar:** Tratar este formato específico de tabela como obrigatório e fechado; descartar o formato sem justificativa quando ele for adequado ao contexto.

**Justificativa:** É um padrão observado de forma consistente na amostra disponível, mas — assim como a estrutura canônica de `OS-DOC-002` — carece de validação com modelos de outras origens antes de virar regra fechada.

**Origem:** `EMPIRICAL_PATTERN`

---

## OS-CODE — Identidade documental, código da OS e aceite

### OS-CODE-001 — Código da OS é estável e nunca reatribuído

**Classificação:** `MUST`

**Objetivo:** Garantir que cada demanda tenha um código de OS (`OS-<AAAA>-<NNNN>`) rastreável, estável entre regenerações, e nunca reutilizado para outra demanda.

**Regra:** O código da OS é resolvido por `tools/os_registry.py`, com a seguinte ordem de autoridade: (1) código explicitamente informado/confirmado pelo usuário (`--os-code`); (2) código já existente no registry local (`01-analysis/_runtime/os-registry.json`) para a mesma demanda; (3) geração automática do próximo sequencial do ano corrente. O sequencial reinicia a cada ano. Um código já atribuído a uma demanda nunca pode ser reatribuído a outra.

**Evitar:** Gerar um novo código apenas porque a OS foi regenerada; permitir que dois demandas diferentes compartilhem o mesmo código; versionar o registry (ele é dado de runtime, não conhecimento de padrão — ver `OS-PRIVACY-003`).

**Justificativa:** Um código de OS que muda a cada regeneração quebra a rastreabilidade documental e comercial (e-mails, aceite, cobrança) que o código deveria garantir.

**Origem:** `QUALITY_IMPROVEMENT`

### OS-CODE-002 — Configuração institucional é centralizada e nunca hardcoded por script

**Classificação:** `MUST`

**Objetivo:** Evitar que valores institucionais (Contratante, Executor, Autor, método de aceite) fiquem espalhados e divergentes entre scripts.

**Regra:** Os defaults institucionais da factory (Contratante padrão, Executor padrão, Autor padrão, formato do código, método padrão de aceite) vivem exclusivamente em `config/os-factory.json`, versionado. `tools/build_os_docx.py` lê esse arquivo e aplica os valores na capa da OS. O campo Autor, quando existente no documento (por exemplo, na tabela de Controle de versão), é normalizado para o Autor padrão no momento da materialização — isto é uma exceção deliberada e documentada à regra geral de "nunca reescrever conteúdo" (ver `OS-CORE-002`), porque Autor/Executor/Contratante são metadados de controle documental, não conteúdo funcional.

**Evitar:** Hardcodar "Thiago Mancilha", "Tria" ou "E-mail" diretamente em `tools/build_os_docx.py` ou em qualquer outro script; deixar o `os-documenter-agent` inventar um valor de Autor diferente do configurado.

**Justificativa:** Centralizar em um único arquivo de configuração permite alterar esses defaults no futuro (por exemplo, um segundo executor) sem refatorar o gerador.

**Origem:** `QUALITY_IMPROVEMENT`

### OS-CODE-003 — Aceite e aprovação nunca são inferidos

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que a `.osFactory` declare, mesmo implicitamente, que uma OS foi aceita ou aprovada sem confirmação explícita.

**Regra:** O Status documental da OS é sempre um entre `Em elaboração`, `Para aceite` ou `Aprovada`. `Em elaboração` e `Para aceite` podem ser calculados automaticamente a partir da prontidão documental/comercial (ver `OS-QA-004`). `Aprovada`, junto com Data do aceite, Aprovado por e Referência do aceite, só pode aparecer mediante confirmação explícita do usuário (`--approved` + `--approved-by`) — nunca inferido a partir de PASS funcional, de todas as condições comerciais estarem preenchidas, ou de qualquer outro sinal indireto. O método de aceite padrão da v1 é E-mail (ver `config/os-factory.json`), formalizado na seção ACEITE da OS com redação que nunca declara que o aceite já ocorreu antes de haver confirmação.

**Evitar:** Marcar `Status: Aprovada` porque a validação funcional é `PASS`; preencher Data do aceite ou Aprovado por sem confirmação explícita; redigir a seção ACEITE de forma que pareça que o aceite já aconteceu.

**Justificativa:** Aceite e aprovação têm efeito contratual/comercial — inferi-los automaticamente exporia a factory e o cliente a um risco que a `.osFactory` não tem competência para assumir sozinha.

**Origem:** `QUALITY_IMPROVEMENT`

---

## OS-COMMERCIAL — Condição comercial: hierarquia e política padrão

### OS-COMMERCIAL-001 — Hierarquia da condição comercial

**Classificação:** `MUST`

**Objetivo:** Garantir que Horas contratadas, Valor total da OS e Forma/condição de pagamento sejam sempre resolvidos pela mesma ordem de autoridade, nunca por decisão ad hoc de um script ou de uma OS específica.

**Regra:** Cada campo comercial (Horas contratadas, Valor total da OS, Forma/condição de pagamento) é resolvido por `tools/os_commercial.py` segundo a seguinte ordem de autoridade, do mais para o menos autoritativo: (1) condição comercial explicitamente confirmada pelo usuário na execução corrente (`--horas-contratadas`, `--valor-total-os`, `--forma-pagamento-marcos`); (2) condição comercial específica presente e válida nos insumos/Markdown da OS (ausente de `OPEN_QUESTION`); (3) condição comercial já confirmada e registrada para a mesma OS em execução anterior (`01-analysis/_runtime/os-commercial.json`, dado de runtime, nunca versionado — ver `OS-PRIVACY-003`); (4) política comercial padrão da Tria (`config/os-commercial-policy.json`, ver `OS-COMMERCIAL-002`). Uma condição de nível mais autoritativo sempre substitui (supersede) uma de nível inferior para a mesma OS — isso nunca é tratado como `CONFLICT`, pois a hierarquia já resolve a precedência de forma determinística. Quando uma confirmação explícita substitui um valor antes presente nos insumos, o tratamento aplicado deve ficar rastreável exclusivamente em artefatos internos (ver `OS-COMMERCIAL-003`) — nunca na própria OS final —, e o documento fonte original nunca é alterado ou apagado.

**Evitar:** Aplicar a política padrão da Tria quando os insumos já trazem uma condição específica; tratar uma confirmação explícita posterior como conflito com o insumo original; deixar um script aplicar sua própria ordem de precedência divergente desta.

**Justificativa:** Sem uma hierarquia única e centralizada, cada regeneração da OS correria o risco de aplicar uma condição comercial diferente, ou de um script decidir por conta própria qual fonte prevalece — quebrando a previsibilidade que a `.osFactory` exige de toda informação comercial.

**Origem:** `QUALITY_IMPROVEMENT`

### OS-COMMERCIAL-002 — Política comercial padrão da Tria e distribuição por marcos

**Classificação:** `MUST`

**Regra:** A política comercial padrão da Tria vive exclusivamente em `config/os-commercial-policy.json`, versionado, e nunca contém dado específico de cliente ou de demanda — apenas política institucional (limite de horas para aplicação do padrão, parcelas padrão, marcos sugeridos de referência). Para serviços até o limite de horas definido na política (padrão: 80 horas), quando nenhuma condição comercial específica é fornecida (nem explícita, nem nos insumos, nem já registrada), aplica-se o padrão de parcelamento da política (padrão: 50% no aceite da OS, 50% na entrega final). Quando o valor total da OS está disponível, os valores de cada parcela são calculados automaticamente (`tools/os_commercial.compute_installments`, aritmética com `Decimal`), e a soma das parcelas sempre reconcilia exatamente com o valor total — a última parcela absorve qualquer resíduo de arredondamento. Para demandas acima do limite de horas da política, ou com múltiplas fases/marcos de execução relevantes (sinalizados explicitamente nos insumos, nunca inferidos por heurística de conteúdo), o parcelamento padrão 50/50 não é aplicado automaticamente — a factory sinaliza `PAYMENT_BY_MILESTONES_RECOMMENDED` e pode identificar marcos naturais já presentes no escopo (por exemplo: aceite/kick-off, conclusão de Discovery, entrega de fase, homologação, entrega final) apenas como referência, mas nunca inventa percentual, valor, número de parcelas ou condição de vencimento. Nesse caso, a Forma/condição de pagamento permanece `[OPEN_QUESTION: definir a distribuição do pagamento entre os marcos da Ordem de Serviço.]` até que uma condição específica seja fornecida.

**Evitar:** Aplicar 50%/50% automaticamente acima do limite de horas da política ou quando há múltiplas fases relevantes; inventar percentual, valor, quantidade de parcelas ou condição de vencimento para pagamento por marcos; espalhar a política comercial (limite de horas, parcelas padrão) em mais de um script; deixar a soma das parcelas divergir do valor total por erro de arredondamento.

**Justificativa:** Um padrão comercial centralizado e auditável evita tanto o retrabalho de decidir a forma de pagamento a cada OS quanto o risco de a factory inventar uma distribuição por marcos que só o time comercial pode legitimamente definir.

**Origem:** `QUALITY_IMPROVEMENT`

### OS-COMMERCIAL-003 — Documento externo apresenta apenas a condição comercial vigente

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que uma condição comercial superseded (por exemplo, uma estimativa de horas anterior a uma confirmação explícita do usuário) apareça no documento que será encaminhado para aceite, mesmo como nota de rastreabilidade ou justificativa de mudança.

**Regra:** A OS final (Markdown em `05-output/<demanda>/` e o DOCX materializado a partir dele) apresenta, nas seções Identificação, ESFORÇO e CONDIÇÕES COMERCIAIS, exclusivamente a condição comercial vigente resolvida pela hierarquia (ver `OS-COMMERCIAL-001`). Quando uma condição comercial é substituída (um nível mais autoritativo supersede um nível inferior), o valor superseded nunca é citado no documento externo — nem como "valor anterior", nem como justificativa da mudança, nem em nota de rodapé ou parágrafo de "registro para rastreabilidade". A rastreabilidade da supersessão (valor anterior, fonte, valor vigente, data/forma da confirmação) é preservada exclusivamente em artefatos internos: `01-analysis/<demanda>/validation.md`, demais materiais de `01-analysis/<demanda>/`, e o registry de runtime (`01-analysis/_runtime/os-commercial.json`, campo `nota`) — nenhum dos quais é versionado fora do escopo previsto por `OS-PRIVACY-003`, nem incluído no documento final.

**Evitar:** Escrever "substitui o valor de X informado em `<fonte>`" na OS final; manter um parágrafo de "registro para rastreabilidade interna" dentro do Markdown/DOCX que será entregue ao cliente; citar o nome de um insumo cujo valor comercial foi superseded, no contexto desse valor, dentro da OS final; remover ou alterar o insumo original só porque seu valor foi superseded (ver `OS-COMMERCIAL-001`).

**Justificativa:** A OS final é um documento comercial externo, não um relatório de auditoria — expor uma estimativa antiga e já substituída introduz ambiguidade e risco de leitura equivocada por quem vai aceitar a Ordem de Serviço, mesmo quando a intenção é apenas transparência. A rastreabilidade interna (`validation.md`, `01-analysis/`, registry de runtime) já cumpre esse papel sem contaminar o documento externo.

**Origem:** `QUALITY_IMPROVEMENT`

---

## OS-QA — Validação e critérios bloqueantes

### OS-QA-001 — Condições que bloqueiam a conclusão da OS

**Classificação:** `MUST_NOT`

**Objetivo:** Definir, de forma objetiva, quando uma OS não pode ser considerada pronta.

**Regra:** A OS não pode ser considerada pronta quando houver: requisito sem rastreabilidade (`UNTRACEABLE_REQUIREMENT`); ampliação de escopo não confirmada; `FUNCTIONAL_CONFLICT` relevante não resolvido; `ARCHITECTURAL_CONFLICT` ou `DOCUMENTAL_CONFLICT` que atenda ao critério de bloqueio da própria subseção em `os-validator-agent.md`; `CONFLICT_UNCLASSIFIED` cuja classificação seja necessária para determinar o impacto; `OPEN_QUESTION` crítica ainda sem resposta; regra necessária para implementação ainda indefinida; esforço inventado/sem origem válida; ou `DISCOVERY_ITEM` que não atenda aos critérios de `OS-UNCERTAINTY-004` (sem etapa de resolução prevista, mascarando decisão de negócio, ou correspondendo na prática a um conflito entre fontes). Um `DISCOVERY_ITEM` válido e controlado, ou um `ARCHITECTURAL_CONFLICT`/`DOCUMENTAL_CONFLICT` não bloqueante, por si só, não são condição de bloqueio.

**Evitar:** Marcar uma OS como concluída "com ressalvas" quando uma dessas condições ainda está presente; tratar essas condições como sugestões em vez de bloqueio; bloquear automaticamente uma OS só por conter `DISCOVERY_ITEM` válido ou `ARCHITECTURAL_CONFLICT`/`DOCUMENTAL_CONFLICT` não bloqueante; aceitar um `DISCOVERY_ITEM` sem evidência de etapa prevista como se não bloqueasse; deixar um `CONFLICT_UNCLASSIFIED` sem classificação apenas para não bloquear.

**Justificativa:** É a formalização, neste arquivo, das condições de classificação `BLOCKED` já definidas no `os-validator-agent` — reunidas aqui para que qualquer agente, não só o validador, saiba reconhecer esses sinais de bloqueio antes mesmo da etapa de validação.

**Origem:** `AGENT_CONTRACT`

### OS-QA-002 — Classificação de resultado e severidade da validação

**Classificação:** `MUST`

**Objetivo:** Garantir que toda validação produza um veredito consistente e granular, não apenas uma aprovação binária.

**Regra:** Toda validação de uma OS deve produzir uma classificação de resultado dentre `PASS`, `PASS_WITH_WARNINGS` ou `BLOCKED`, e cada problema encontrado deve receber uma severidade dentre `CRITICAL`, `MAJOR`, `MINOR` ou `INFO`, conforme já definido no `os-validator-agent`.

**Evitar:** Validações informais que apenas dizem "está bom" ou "está ruim" sem classificação estruturada; misturar severidades diferentes num único apontamento genérico.

**Justificativa:** Granularidade de severidade permite priorizar correções e decidir com objetividade se uma pendência é ou não bloqueante.

**Origem:** `AGENT_CONTRACT`

### OS-QA-003 — FUNCTIONAL_BLOCKED e OUTPUT_BLOCKED nunca se misturam

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que uma falha de conteúdo/especificação (a OS ainda não está funcionalmente pronta) seja confundida com uma falha de materialização (a OS está funcionalmente pronta, mas o DOCX não pôde ser gerado ou está visualmente inconsistente) — e vice-versa.

**Regra:** `FUNCTIONAL_BLOCKED` é usado exclusivamente pelo `os-validator-agent`, antes de qualquer tentativa de materialização, para problemas de conteúdo (`OPEN_QUESTION` crítica, `FUNCTIONAL_CONFLICT` relevante, requisito não rastreável, escopo indefinido, e demais condições já cobertas por `OS-QA-001`). `OUTPUT_BLOCKED` é usado exclusivamente pelas ferramentas de materialização (`tools/build_os_docx.py`, `tools/audit_os_visual_format.py`, `tools/render_docx_with_word.ps1`) para falhas que ocorrem depois que o conteúdo já foi considerado `PASS` ou `PASS_WITH_WARNINGS` (template ausente, figura referenciada e ausente, erro ao salvar o DOCX, ou auditoria visual com finding bloqueante). Um resultado `BLOCKED` do `os-validator-agent` impede a própria tentativa de materialização — o orquestrador (`99-prompts/gerar-os.md`) não deve invocar `build_os_docx.py` nesse caso, e o script recusa a execução caso seja invocado mesmo assim com o status de validação informado.

**Evitar:** Reportar uma falha de template ausente ou figura ausente como se fosse uma pendência de conteúdo; reportar uma `OPEN_QUESTION` crítica não respondida como se fosse um problema de materialização; gerar um DOCX "mesmo assim" quando a validação funcional retornou `BLOCKED`, apresentando-o como documento final aprovado.

**Justificativa:** A materialização DOCX introduziu uma nova classe de falha (visual/técnica) que não existia quando só havia Markdown. Sem essa separação explícita, um problema de geração de arquivo poderia ser tratado como se fosse um problema da especificação (ou o inverso), levando a correções na etapa errada do pipeline.

**Origem:** `QUALITY_IMPROVEMENT`

---

### OS-QA-004 — Prontidão para aceite é separada do gate funcional

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que uma pendência comercial/documental (por exemplo, valor da OS ainda não informado) seja confundida com, ou transformada automaticamente em, uma falha funcional.

**Regra:** A avaliação de prontidão para aceite (`READY_FOR_ACCEPTANCE` / `NOT_READY_FOR_ACCEPTANCE`, calculada por `tools/build_os_docx.py`) é estritamente separada do resultado da validação funcional (`PASS` / `PASS_WITH_WARNINGS` / `BLOCKED`, produzido pelo `os-validator-agent`). `NOT_READY_FOR_ACCEPTANCE` nunca transforma uma especificação funcionalmente válida em `FUNCTIONAL_BLOCKED`, e nunca impede a geração do DOCX — apenas mantém o Status documental como `Em elaboração` em vez de `Para aceite`. `READY_FOR_ACCEPTANCE` exige, cumulativamente: validação funcional diferente de `BLOCKED`; código da OS, versão, Contratante e Executor presentes; Horas contratadas, Valor total da OS e Forma/condição de pagamento presentes (sem `OPEN_QUESTION`); e DOCX materializado sem `OUTPUT_BLOCKED`. A ausência de valor ou de forma de pagamento nos insumos deve ser registrada como `OPEN_QUESTION` na seção CONDIÇÕES COMERCIAIS — nunca como `DISCOVERY_ITEM` (que é reservado a descoberta técnica com etapa de resolução prevista, ver `OS-UNCERTAINTY-004`) e nunca inventada.

**Evitar:** Bloquear a geração do DOCX por falta de valor comercial; classificar ausência de valor/forma de pagamento como `DISCOVERY_ITEM`; tratar `READY_FOR_ACCEPTANCE` como sinônimo de aprovação (ver `OS-CODE-003`).

**Justificativa:** A materialização introduziu uma OS com identidade comercial (valor, pagamento, aceite) além da especificação funcional pura — sem essa separação explícita, uma pendência puramente comercial poderia indevidamente barrar uma especificação funcional já pronta, ou o inverso.

**Origem:** `QUALITY_IMPROVEMENT`

---

## OS-PRIVACY — Proteção de dados de clientes e modelos reais

### OS-PRIVACY-001 — Modelos reais servem só como fonte de aprendizado

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que dado real de cliente vaze para dentro de áreas versionadas do repositório.

**Regra:** Documentos reais em `00-inbox/_os-models/` (ou em qualquer outra área ignorada pelo Git) servem exclusivamente como fonte de aprendizado de padrão. Nunca copiar para arquivos versionados: nomes de clientes; nomes de pessoas; números de contrato; identificadores de demanda; conteúdo proprietário que não seja necessário para representar um padrão; imagens; prints; ou trechos extensos copiados literalmente.

**Evitar:** Citar, mesmo que "só como exemplo", um nome de cliente ou de sistema real dentro de `03-knowledge-base/`, `04-templates/` ou qualquer outro diretório versionado; incluir uma captura de tela real como ilustração de padrão.

**Justificativa:** É regra explícita e central do `os-pattern-learner-agent`; sem ela, a base de conhecimento pública da `.osFactory` corre risco de expor informação confidencial de clientes.

**Origem:** `AGENT_CONTRACT`

### OS-PRIVACY-002 — Proteção geral de dados de cliente fora das áreas ignoradas

**Classificação:** `MUST_NOT`

**Objetivo:** Reforçar que a proteção de dado de cliente não se limita aos modelos de aprendizado — vale para toda demanda em andamento.

**Regra:** Nenhum conteúdo específico de cliente proveniente de `00-inbox/<demanda>/`, `01-analysis/<demanda>/` ou `05-output/<demanda>/` (áreas de runtime de uma demanda, ignoradas pelo Git — ver `OS-PRIVACY-003` — com exceção de `01-analysis/_os-models/`) deve ser copiado, resumido ou referenciado em detalhe dentro de `02-agents/`, `03-knowledge-base/` ou `04-templates/`.

**Evitar:** Usar uma demanda real em andamento como exemplo ilustrativo dentro de um arquivo de regra ou template.

**Justificativa:** Confirma e generaliza, para todo o repositório, a mesma convenção de `.gitignore` (`/00-inbox/`, `/05-output/`, `/01-analysis/*` com exceção de `/01-analysis/_os-models/`) já adotada pela `.osFactory` e observada também na factory irmã de propostas.

**Origem:** `EMPIRICAL_PATTERN`

### OS-PRIVACY-003 — Artefatos operacionais de uma demanda não são versionados

**Classificação:** `MUST_NOT`

**Objetivo:** Impedir que artefatos intermediários gerados durante o processamento de uma demanda real — que podem conter nome de cliente, responsável, valores, identificadores de requisição e outros dados específicos — sejam versionados no Git.

**Regra:** Os artefatos gerados em `01-analysis/<demanda>/` (`intake.md`, `functional-analysis.md`, `validation.md` e demais arquivos específicos de uma demanda) são dados de runtime, tal como os insumos em `00-inbox/<demanda>/` e a saída em `05-output/<demanda>/`, e devem permanecer fora do controle de versão (`.gitignore`). A única exceção é `01-analysis/_os-models/`, que contém conhecimento já sanitizado e aprovado para versionamento, produzido pelo `os-pattern-learner-agent` conforme `OS-PRIVACY-001`.

**Evitar:** Tratar `01-analysis/<demanda>/` como uma área segura para versionamento só porque não contém arquivo binário ou imagem; assumir que a ausência de um campo específico (como nome de cliente) dispensa a regra — o conjunto do artefato pode ser suficiente para identificar a demanda.

**Justificativa:** Identificada no primeiro teste ponta a ponta real da `.osFactory`: os artefatos de `01-analysis/<demanda>/` continham nome de cliente, responsável e identificadores reais de requisição, mas `01-analysis/<demanda>/` não estava coberto pela mesma proteção de `.gitignore` já aplicada a `00-inbox/` e `05-output/`. Esta regra formaliza a correção dessa lacuna, preservando `01-analysis/_os-models/` como exceção deliberada.

**Origem:** `QUALITY_IMPROVEMENT`


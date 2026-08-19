# Análise de Padrões de OS

> Executado por: `os-pattern-learner-agent`. Fonte: 3 modelos reais em `00-inbox/_os-models/` (área ignorada pelo Git). Este arquivo não contém nome de cliente, número de contrato, nome de solicitante/autor, nome de sistema proprietário, código de demanda, título original de arquivo, prints ou texto extenso copiado literalmente dos modelos — apenas padrão estrutural e metodológico, conforme a regra de confidencialidade do agente.

## Legenda de classificação

Usada na tabela final ("Próximos padrões recomendados"):

- `MUST` — princípio forte, já defensável independentemente do tamanho da amostra (geralmente por reforçar "nunca inventar").
- `SHOULD` — boa prática recorrente, recomendada, mas não bloqueante.
- `OPTIONAL` — variação aceitável, fica a critério da demanda ou da organização.
- `CANONICAL_CANDIDATE` — padrão observado de forma consistente nesta amostra e adotado como **referência inicial** da `.osFactory`, mas ainda sujeito a revisão quando novos modelos de outras origens forem analisados. Não deve ser tratado como regra universal confirmada.
- `DO_NOT_ADOPT` — comportamento observado que não deve ser reproduzido.

## 1. Modelos analisados

- `Modelo A`
- `Modelo B`
- `Modelo C`

A correspondência entre estes rótulos e os arquivos reais existe apenas localmente em `00-inbox/_os-models/` (área ignorada pelo Git) e não é registrada neste documento.

Os três modelos pertencem à mesma família de template (mesmo cliente, mesmo par de autores/revisores, mesmo projeto de origem). Essa homogeneidade é relevante para interpretar as conclusões: os achados têm boa consistência interna, mas amostra pequena e pouco diversa — ver seção 14.

## 2. Estrutura recorrente

Os três modelos seguem, sem exceção, a mesma ordem macro:

`Capa/título → Bloco de identificação (tabela) → Bloco de controle de versão (tabela) → Sumário → 1. Descrição → 2. Situação Atual → 3. Escopo (+ subseção condicional) → 4. Premissas e Dependências → 5. Não Escopo → 6. Esforço (tabela)`

O documento é curto (4 a 6 páginas), com parágrafos curtos, uso extensivo de bullets e nenhuma seção de encerramento ou narrativa comercial — é um documento técnico de especificação, não uma peça de apresentação.

Esta ordem é tratada, nesta etapa, como `CANONICAL_CANDIDATE` da `.osFactory` (ver detalhamento e ressalva na seção 3), não como estrutura universal confirmada.

## 3. Seções obrigatórias candidatas

Presentes, na mesma ordem, nos 3 modelos:

- Bloco de identificação (projeto, contrato, identificador da demanda, anexos, solicitante, aprovação, esforço resumido).
- Bloco de controle de versão (versão, autor, descrição da revisão, data).
- Sumário com paginação.
- `1. Descrição`
- `2. Situação Atual`
- `3. Escopo`
- `4. Premissas e Dependências`
- `5. Não Escopo`
- `6. Esforço` (tabela)

Classificação: `CANONICAL_CANDIDATE`. É o padrão canônico observado nesta família de documentos e será utilizado como referência inicial da `.osFactory`, mas ainda poderá evoluir quando novos modelos de outras origens forem analisados. Frequência de 3/3 nesta amostra **não** é declarada aqui como obrigatoriedade universal — ver Open Decisions (seção 14) e a ressalva de qualidade de conteúdo nas seções 8, 9 e 12.

Os campos específicos do bloco de identificação (projeto, contrato, solicitante, aprovação, anexos, esforço resumido) são tratados como padrão observado, não como obrigatoriedade universal: podem variar conforme o contexto da organização que utiliza a `.osFactory` (ver seção 15 e tabela final, item 2).

## 4. Seções condicionais identificadas

- Uma subseção sob `3. Escopo` está presente nos 3 modelos, mas com **título e profundidade variáveis** conforme a natureza da mudança: em dois casos é uma observação pontual em texto corrido/bullets simples; no caso com mais regras de negócio, vira um bloco nomeado e estruturado por categoria de regra. Ou seja, "existir uma subseção de detalhamento" é quase universal nesta amostra, mas o nome e a forma não são fixos.
- `Integração` — aparece como subseção própria em apenas 1 dos 3 modelos, exatamente quando a mudança precisa propagar dado para um sistema externo. É condicional ao tipo de demanda, não um padrão universal.
- "Validações e Mensagens" **nunca** aparece como seção própria nos 3 modelos — sempre que existe uma regra de bloqueio, a mensagem do sistema é citada em linha, dentro do texto de Escopo, não em seção separada.
- Figuras ilustrativas aparecem nos 3 modelos, mas em quantidade variável (1 a 2), sempre com legenda numerada e sempre dentro de "Situação Atual" e/ou "Escopo" (nunca em seção própria de anexo visual).

## 5. Padrões de redação

- **Descrição**: sempre um único parágrafo curto, no formato "especificação funcional elaborada/redigida para atendimento de uma [melhoria/solicitação] no sistema, para que [resultado esperado]". Não descreve regra nem situação atual — só a finalidade do documento.
- **Situação Atual**: um parágrafo curto descrevendo objetivamente a limitação ou regra vigente, por vezes seguido de uma figura mostrando a limitação na prática (uma tentativa bloqueada, por exemplo).
- **Escopo**: abre sempre declarando explicitamente o delta em relação ao que já funcionava — não apenas o que passa a ser possível, mas também o que já era possível antes, lado a lado. Esse contraste explícito aparece nos 3 modelos.
- **Regras**: redigidas com verbos deônticos ("deverá", "deverão", "será", "poderá(ão)"), sempre no formato condição → comportamento esperado → (quando aplicável) exceção com mensagem de erro.
- Registro sempre técnico-direto; nenhum dos 3 modelos usa linguagem comercial, adjetivos de valor ou tom de venda.

## 6. Padrões de regras funcionais

Estrutura recorrente de cada regra: **[elemento/atributo afetado] → condição de disparo → comportamento esperado do sistema → (opcional) exceção e mensagem de erro**.

Quando há mais de uma regra na mesma demanda, elas são agrupadas por categoria nomeada (por exemplo, por atributo afetado, por tipo de objeto, por cenário de aplicação) em vez de uma lista plana — esse agrupamento só aparece no modelo com maior densidade de regras, sugerindo que a estrutura de agrupamento escala com a complexidade da demanda, não é fixa por padrão.

Toda condição de disparo é declarada de forma explícita (o valor ou estado exato que ativa a regra), nunca fica implícita.

## 7. Padrões de integrações

Só aparece quando a demanda precisa propagar uma mudança a um sistema externo (1 dos 3 modelos). Quando aparece, segue sempre dois movimentos: (1) o que o sistema de origem deve fazer/enviar ao ser acionado pelo usuário; (2) o que o sistema externo deve fazer ao receber essa informação. Não existe seção separada de "Impactos" — impacto e integração são tratados juntos, como um único fluxo narrado.

## 8. Padrões de premissas e dependências

Achado relevante: nos 3 modelos, o conteúdo da seção "Premissas e Dependências" é **idêntico** entre si — duas frases-modelo genéricas (uma sobre a necessidade de revisar o esforço em caso de alteração do documento, outra sobre a possibilidade de o protótipo mudar). Nenhuma das três demandas — tecnicamente bastante distintas entre si — tem uma premissa específica registrada (dependência de dado, de ambiente, de outro time, de acesso, etc.).

Isso indica que a seção existe estruturalmente (3/3), mas na prática funciona como bloco de boilerplate herdado do template, não como conteúdo analítico da demanda. Ver anti-padrão na seção 12.

## 9. Padrões de não escopo

Mesmo achado da seção anterior: o texto de "Não Escopo" é praticamente idêntico nos 3 modelos — uma frase genérica dizendo que mudanças de comportamento em cenários diferentes dos descritos serão tratadas no "fluxo usual de melhorias" e não devem impedir a homologação do escopo atual. Nenhum dos 3 modelos registra uma exclusão específica e concreta da própria demanda.

## 10. Padrões de esforço

Tabela com linhas fixas — Análise e Especificação, Desenvolvimento, Testes Internos, Gestão, Total — e uma única coluna de horas. Nos 3 modelos, **todos** os valores estão em branco (placeholder), inclusive o campo resumido de esforço no bloco de identificação da capa (também placeholder).

Dois achados distintos aqui, com força diferente:

- O **formato específico da tabela** (essas linhas, nesta ordem) é um padrão observado nesta amostra, tratado como `CANONICAL_CANDIDATE`/`SHOULD` — não como formato universal `MUST`, até que modelos de outras origens sejam analisados.
- A **regra de não preencher esforço na fase de especificação** é um princípio mais forte e independente do formato da tabela: a `.osFactory` não deve inventar ou estimar horas durante a geração da especificação quando o esforço não tiver sido informado por uma fonte válida. Este é tratado como `MUST`.

## 11. Regras de qualidade candidatas

- Escopo deve declarar explicitamente o delta relativo à situação atual (o que já funcionava versus o que passa a funcionar) — presente 3/3, aumenta testabilidade e reduz ambiguidade.
- Quando os insumos definirem explicitamente uma mensagem apresentada pelo sistema (erro, bloqueio, confirmação), a OS deve preservá-la exatamente, sem parafrasear. Quando a mensagem necessária ainda não estiver definida nos insumos, ela deve ser tratada como lacuna (`OPEN_QUESTION`) e nunca inventada. **Não** se trata de exigir que toda validação possua mensagem de erro — apenas de nunca inventar uma quando ela não existir na fonte.
- Quando há múltiplas regras de negócio numa mesma demanda, elas devem ser agrupadas por categoria nomeada, não listadas de forma plana.
- Toda figura referenciada no texto deve ter legenda numerada e ser citada explicitamente no parágrafo que a antecede ou sucede.
- A tabela de esforço deve manter as linhas observadas nesta amostra como candidata inicial (`CANONICAL_CANDIDATE`), mas a regra que não pode enfraquecer é: nunca preencher esforço na fase de especificação sem fonte válida (`MUST` — já coberto pela regra do `os-documenter-agent` de não estimar esforço nesta etapa, e agora com respaldo empírico).

## 12. Anti-padrões encontrados

- **Boilerplate em "Premissas e Dependências" e em "Não Escopo"**: as duas seções aparecem em 100% dos modelos, mas com texto genérico e repetido entre demandas tecnicamente muito diferentes, sem relação com a especificidade de cada uma. Isso é o exemplo mais claro do princípio "frequência não significa obrigatoriedade" — a **presença estrutural** da seção é um bom candidato a padrão, mas o **conteúdo boilerplate observado não deve ser reproduzido** como prática; pelo contrário, deve virar regra de qualidade que proíbe conteúdo genérico nessas seções.
- **Controle de versão sem incremento real**: nos 3 modelos, a entrada "Versão Inicial" e a entrada "Revisão" estão registradas com o mesmo número de versão (1.0), mesmo sendo edições distintas em datas diferentes. Isso quebra a utilidade do bloco de controle de versão como mecanismo de rastreabilidade.
- **Campo "Aprovação" sempre vazio**: presente no bloco de identificação dos 3 modelos, mas nunca preenchido em nenhum deles — não há evidência de como (ou se) o processo de aprovação formal é de fato registrado no documento.
- **Ausência de marcação de incerteza**: nenhum dos 3 modelos distingue fato confirmado de inferência ou pergunta em aberto — tudo é apresentado como fato consolidado. Isso é esperado, pois são especificações já homologadas (documento de saída, não de intake), mas não deve ser copiado como prática para os estágios de intake/análise da `.osFactory`, que precisam expor `OPEN_QUESTION`, `INFERENCE` e `CONFLICT` de forma visível.

## 13. Variações entre os modelos

- O título e a forma da subseção de detalhamento sob "Escopo" variam conforme a natureza da regra (observação simples versus bloco de regras nomeado versus integração).
- A quantidade de figuras varia entre 1 e 2 por documento.
- A extensão e a estrutura interna de "Escopo" crescem proporcionalmente à quantidade de regras de negócio envolvidas na demanda.
- Apenas 1 dos 3 modelos contém subseção de "Integração"; os outros dois não têm nenhuma menção a sistemas externos.

## 14. Open Decisions

- A amostra é pequena (3 documentos) e homogênea (mesmo cliente, mesmo template, mesma dupla de autoria/revisão). Isso dá boa consistência interna aos achados, mas baixa validação externa — por isso a estrutura de 6 seções, os campos de identificação e o formato da tabela de esforço são tratados como `CANONICAL_CANDIDATE`, não como regra fechada, até que modelos de outras origens/domínios sejam analisados.
- Nenhum dos modelos mostra como representar `OPEN_QUESTION`, `INFERENCE` ou `CONFLICT` no corpo de uma OS finalizada, pois são documentos já homologados, sem histórico do processo de elaboração. A forma como o `os-documenter-agent` deve materializar esses marcadores na OS final não tem, portanto, respaldo em exemplo real — precisa ser decidida sem base empírica dos modelos.
- Não há evidência de como o campo "Anexos" é preenchido quando existem anexos de fato (nos 3 modelos está sempre vazio).
- Não há evidência de como o documento trataria múltiplas mensagens de erro para a mesma regra, nem mensagens de sucesso/confirmação — só há exemplos de mensagem de erro/bloqueio.
- Não há evidência do padrão de identificador de demanda fora do formato observado — pode ser específico da origem destes modelos e não deve virar regra universal sem confirmação de outras fontes.

## 15. Recomendações para a `.osFactory`

Estes achados deveriam futuramente alimentar:

- **`03-knowledge-base/rules/os-rules.md`**: estrutura canônica candidata (`CANONICAL_CANDIDATE`) das 6 seções, a ser usada como referência inicial, não como regra universal fechada (item 3); proibição de conteúdo boilerplate em "Premissas e Dependências" e "Não Escopo" (item 12); regra de declarar o delta em Escopo (item 11); regra de preservar mensagem exata quando informada pelos insumos e tratar mensagem ausente como `OPEN_QUESTION`, nunca inventar (item 11); regra forte de não preencher/estimar esforço sem fonte válida na fase de especificação (item 10, `MUST`, já coberta pelo `os-documenter-agent`, agora com respaldo empírico).
- **`03-knowledge-base/standards/os-style-guide.md`**: padrão de redação por seção (item 5); padrão de agrupamento de regras por categoria (item 6); padrão de dois movimentos para integrações (item 7); uso de verbos deônticos.
- **`03-knowledge-base/standards/os-checklist.md`**: item que barra "Premissas e Dependências"/"Não Escopo" genéricos; item que exige preservar mensagem exata quando existir nos insumos e registrar `OPEN_QUESTION` quando não existir; item que exige incremento real de versão a cada revisão; item que exige legenda numerada em toda figura referenciada.
- **`04-templates/os-template.md`**: esqueleto candidato (`CANONICAL_CANDIDATE`) de 6 seções na ordem observada, mais bloco de identificação e bloco de controle de versão (corrigindo o anti-padrão de versão fixa) no topo do documento — campos do bloco de identificação sujeitos a adaptação por organização.

Este agente não cria nem altera nenhum desses quatro arquivos nesta etapa.

## Próximos padrões recomendados

| # | Recomendação | Classificação | Destino |
|---|---|---|---|
| 1 | Estrutura candidata de 6 seções nomeadas (Descrição, Situação Atual, Escopo, Premissas e Dependências, Não Escopo, Esforço), nesta ordem, como referência inicial da `.osFactory` | `CANONICAL_CANDIDATE` | `04-templates/os-template.md` |
| 2 | Bloco de identificação (projeto, contrato, demanda, anexos, solicitante, aprovação, esforço resumido) no topo do documento — campos específicos podem depender do contexto organizacional | `CANONICAL_CANDIDATE` | `04-templates/os-template.md` |
| 3 | Bloco de controle de versão (versão, autor, descrição, data), com regra explícita de incremento a cada revisão | `SHOULD` | `04-templates/os-template.md` + `03-knowledge-base/rules/os-rules.md` |
| 4 | Escopo deve declarar explicitamente o delta em relação à situação atual | `MUST` | `03-knowledge-base/rules/os-rules.md` |
| 5 | Preservar exatamente a mensagem do sistema quando definida pelos insumos; quando não estiver definida, tratar como `OPEN_QUESTION` e nunca inventar | `MUST` | `03-knowledge-base/rules/os-rules.md` |
| 6a | Tabela de esforço com as linhas observadas nesta amostra (Análise e Especificação / Desenvolvimento / Testes Internos / Gestão / Total) | `CANONICAL_CANDIDATE` | `04-templates/os-template.md` |
| 6b | Nunca inventar ou estimar horas de esforço na geração da especificação quando não informado por fonte válida | `MUST` | `03-knowledge-base/rules/os-rules.md` (já coberto conceitualmente pelo `os-documenter-agent`) |
| 7 | Proibir conteúdo boilerplate genérico em "Premissas e Dependências" e "Não Escopo"; exigir conteúdo específico da demanda | `MUST` | `03-knowledge-base/rules/os-rules.md` + `03-knowledge-base/standards/os-checklist.md` |
| 8 | Regras com múltiplas dimensões devem ser agrupadas por categoria nomeada, não em lista plana | `SHOULD` | `03-knowledge-base/standards/os-style-guide.md` |
| 9 | Subseção de "Integração" só quando a demanda envolver sistema externo, seguindo o padrão de dois movimentos (origem → destino) | `SHOULD` | `03-knowledge-base/standards/os-style-guide.md` |
| 10 | Toda figura referenciada deve ter legenda numerada e ser citada explicitamente no texto | `SHOULD` | `03-knowledge-base/standards/os-checklist.md` |
| 11 | Nome da subseção de detalhamento sob Escopo pode variar conforme o conteúdo (Observações/Regras/Integração), em vez de nome fixo único | `OPTIONAL` | `03-knowledge-base/standards/os-style-guide.md` |
| 12 | Sumário automático com paginação no início do documento | `OPTIONAL` | `04-templates/os-template.md` (nível DOCX) |
| 13 | Reproduzir o texto boilerplate genérico observado em "Premissas e Dependências" e "Não Escopo" como conteúdo padrão | `DO_NOT_ADOPT` | — |
| 14 | Manter o mesmo número de versão (ex.: "1.0") em revisões distintas | `DO_NOT_ADOPT` | — |
| 15 | Deixar o campo "Aprovação" sempre vazio sem processo definido de preenchimento | `DO_NOT_ADOPT` | — |
| 16 | Herdar qualquer nome de sistema, cliente, contrato, pessoa, código de demanda ou título original de arquivo dos modelos reais para arquivos versionados | `DO_NOT_ADOPT` | — |
| 17 | Tratar a estrutura de 6 seções e os demais achados classificados como `CANONICAL_CANDIDATE` como regra universal fechada antes de validar com modelos de outras origens/domínios | `DO_NOT_ADOPT` (por ora) | — (ver Open Decisions) |
| 18 | Exigir que toda validação possua mensagem de erro (em vez de preservar a mensagem apenas quando os insumos a definirem) | `DO_NOT_ADOPT` | — |

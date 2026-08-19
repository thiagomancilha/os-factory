# Guia de Estilo de Redação da OS (`os-style-guide.md`)

## Propósito

Este documento define **como escrever** uma Especificação Funcional / Ordem de Serviço (OS) clara, técnica, objetiva e testável a partir de uma análise funcional já validada (`functional-analysis.md`). Ele não define **o que** a OS deve conter — essa é a função de `os-rules.md` — nem **como verificar** se uma OS está correta — essa é a função de `os-checklist.md`. Este guia orienta principalmente o `os-documenter-agent`, mas se aplica a qualquer agente ou pessoa que redija ou revise texto de uma OS.

O princípio geral é simples: a OS é lida por pessoas de áreas diferentes (negócio, desenvolvimento, QA) que precisam extrair exatamente a mesma regra do mesmo texto. Redação ambígua, prolixa ou comercial atrapalha esse objetivo, mesmo quando o conteúdo funcional está correto.

Este guia não substitui o julgamento do agente ou da pessoa que redige. Ele descreve o padrão esperado e os motivos por trás dele, para que desvios conscientes e justificados continuem possíveis.

## Princípios de escrita

### 1. Clareza antes de formalismo

Prefira a frase mais simples que comunique a regra corretamente. Formalismo excessivo, jargão desnecessário ou construções rebuscadas não tornam a OS mais profissional — tornam mais difícil de revisar e mais fácil de mal interpretar. Se uma frase precisa ser lida duas vezes para ser entendida, ela deve ser reescrita.

### 2. Uma afirmação funcional por vez

Cada frase ou item deve conter uma única regra, condição ou comportamento. Frases que acumulam múltiplas condições, exceções e consequências em um único período dificultam a verificação e a rastreabilidade individual de cada afirmação. Quando uma regra tiver mais de uma condição relevante, ela deve ser dividida em itens.

### 3. Situação atual ≠ escopo

SITUAÇÃO ATUAL descreve como o sistema funciona hoje, sem prescrever nada sobre a mudança. ESCOPO descreve o que deve ser construído ou alterado. Misturar as duas — por exemplo, descrever o comportamento atual já embutindo o comportamento futuro dentro da mesma frase — quebra a rastreabilidade entre "o que existia" e "o que está sendo pedido" e dificulta a validação do delta funcional.

### 4. Delta funcional explícito (hoje → mudança → comportamento futuro)

Sempre que a demanda alterar um comportamento existente, o texto deve deixar explícitos os três elementos: o que acontece hoje, o que muda, e o que passa a acontecer depois da mudança. Omitir qualquer um dos três obriga o leitor a inferir o que não foi dito, o que é exatamente o que a OS deve evitar.

### 5. Regras funcionais no formato condição → comportamento → exceção

Regras de negócio devem ser redigidas de forma que a condição de disparo, o comportamento esperado e as exceções aplicáveis fiquem claramente identificáveis — juntos ou como itens separados. Esse formato torna a regra diretamente testável: cada condição vira um caso de teste, cada exceção vira um caso de teste adicional.

### 6. Verbos normativos

Regras confirmadas pela análise funcional devem ser escritas com verbos normativos e afirmativos: "deverá", "deve", "será permitido", "não deverá permitir", "deverá apresentar", "deverá enviar", "deverá atualizar". Evite verbos que introduzem incerteza onde não há incerteza real: "poderia", "talvez", "provavelmente", "idealmente". Se a regra ainda não está confirmada, o texto não deve fingir certeza com um verbo normativo — deve usar `[OPEN_QUESTION: ...]` ou `[INFERENCE: ...]` em vez de suavizar a redação com hedging.

### 7. Terminologia

Nomes de campos, telas, status, papéis, sistemas e entidades devem ser preservados exatamente como aparecem nos insumos — mesma grafia, mesma capitalização, mesma abreviação. Não substitua por sinônimos "mais claros" e não varie a forma de nomear a mesma coisa ao longo do documento. Consistência terminológica importa mais do que variedade estilística: o leitor deve poder confiar que o mesmo termo sempre se refere à mesma coisa.

### 8. Mensagens do sistema

Mensagens de validação, erro, confirmação ou notificação devem ser reproduzidas exatamente como definidas na fonte, entre aspas, sem correções gramaticais, sem paráfrase e sem tentativa de "melhorar" o texto. Se a mensagem exata não foi definida em nenhum insumo, o texto não deve inventar uma — deve registrar `[OPEN_QUESTION: definir mensagem apresentada ao usuário]`.

### 9. Incerteza

Toda incerteza deve ser marcada com um dos três marcadores padronizados: `[OPEN_QUESTION: ...]` para lacunas a esclarecer, `[INFERENCE: ...]` para conclusões razoáveis não confirmadas explicitamente, `[CONFLICT: ...]` para contradições entre insumos. Esses marcadores nunca devem ser omitidos ou escondidos durante a elaboração do documento para "parecer mais completo". Uma OS aprovada pelo `os-validator-agent` não deve conter marcadores bloqueantes sem resolução — mas durante a redação, marcar a incerteza é sempre preferível a resolvê-la silenciosamente.

### 10. Premissas e dependências

Cada item de premissas e dependências deve declarar uma condição ou dependência concreta, o responsável por ela quando conhecido, e o impacto caso não seja satisfeita. Evite premissas genéricas que poderiam ser copiadas para qualquer demanda ("o ambiente de homologação deve estar disponível", "a equipe deve estar alinhada") sem relação específica com o conteúdo desta OS.

### 11. Não escopo

Cada item de NÃO ESCOPO deve seguir o formato "Não faz parte desta demanda: `<item específico>`." — direto, específico, sem justificativas longas. Esta seção não é um lugar para registrar premissas não satisfeitas, lacunas de informação ou dúvidas — isso pertence a PREMISSAS E DEPENDÊNCIAS ou aos marcadores de incerteza. NÃO ESCOPO existe apenas para deixar explícito o que foi deliberadamente excluído.

### 12. Integrações

Regras de integração devem ser descritas no formato origem → ação/dado → destino → comportamento esperado. Quando houver mais de um aspecto relevante (envio, recebimento, tratamento de erro, atualização de estado), cada um deve ser tratado separadamente em vez de comprimido em uma única frase. Nunca invente protocolo, formato de API, payload ou detalhe de arquitetura que não esteja presente nos insumos — a ausência dessa informação deve virar `[OPEN_QUESTION: ...]`.

### 13. Figuras

Imagens só devem ser incluídas quando cumprem função informativa — explicam algo que o texto sozinho não comunica com a mesma clareza. Devem ser posicionadas próximas ao texto que explicam, ter legenda, e ser numeradas quando houver mais de uma. Toda figura deve ser referenciada explicitamente no texto. Imagens decorativas não devem ser incluídas. Identidade visual do documento é uma decisão de template futuro, não deste guia.

### 14. Tabelas

Use tabelas apenas quando elas melhoram a legibilidade ou a comparação em relação ao texto corrido — por exemplo, a tabela de esforço, matrizes simples de comparação, ou listas de campo/valor tabulares. Não converta regras narrativas em tabelas apenas por preferência de formato: regras com condição, comportamento e exceção geralmente são mais claras em texto ou em itens do que espremidas em células.

### 15. Tamanho dos parágrafos

Parágrafos devem ser curtos. Um parágrafo que acumula múltiplas regras, condições e exceções deve ser quebrado em parágrafos menores ou convertido em itens. Parágrafos longos escondem informação relevante no meio do texto, onde é mais fácil de ser ignorada na revisão.

### 16. Repetição

Não repita a mesma regra em seções diferentes do documento. Se uma regra já foi declarada em ESCOPO e é relevante para PREMISSAS E DEPENDÊNCIAS ou NÃO ESCOPO, faça referência a ela em vez de reescrevê-la. Repetição aumenta o risco de as duas versões divergirem ao longo de revisões futuras.

### 17. Linguagem comercial

A OS é um documento técnico, não uma proposta comercial. Evite expressões de caráter comercial ou promocional como "solução robusta", "solução inovadora", "ganho significativo", "melhoria expressiva", "experiência aprimorada", "maior eficiência" — a menos que esses termos façam parte literal da demanda (por exemplo, citados por quem solicitou). Prefira descrever o comportamento concreto em vez de qualificá-lo com adjetivos de valor.

## Orientação por seção

Esta seção detalha o que cada bloco da estrutura canônica (`OS-DOC-002`, `CANONICAL_CANDIDATE`) deve e não deve conter, em termos de redação.

### DESCRIÇÃO

**Objetivo:** situar o leitor sobre do que se trata a demanda, em poucas frases.

**Deve conter:** um resumo direto do que está sendo solicitado e por quê, em nível suficiente para alguém sem contexto prévio entender do que o documento trata.

**Não deve conter:** detalhamento de regras funcionais, estimativa de esforço, descrição de solução técnica, ou narrativa extensa sobre o histórico da demanda. Esses conteúdos pertencem a outras seções; DESCRIÇÃO não deve antecipá-los.

### SITUAÇÃO ATUAL

**Objetivo:** responder "como o sistema funciona hoje?" e "qual limitação ou lacuna motiva esta demanda?".

**Deve conter:** o comportamento existente relevante para a demanda, e a limitação específica que gera a necessidade de mudança.

**Não deve conter:** o comportamento futuro ou desejado — isso pertence a ESCOPO. Misturar os dois nesta seção quebra a leitura do delta funcional (ver Princípio 3 e 4).

### ESCOPO

**Objetivo:** descrever, de forma testável, o que deve ser construído ou alterado.

**Deve conter:** as regras funcionais no formato condição → comportamento → exceção (Princípio 5), o delta funcional explícito quando aplicável (Princípio 4), e subseções condicionais quando a natureza da demanda justificar (por exemplo, regras agrupadas por tipo de objeto, por operação — criação/edição/exclusão —, ou por camada — comportamento de atributo, validação, integração). Esta é tipicamente a seção mais extensa e detalhada da OS.

**Não deve conter:** descrição do comportamento atual (pertence a SITUAÇÃO ATUAL), itens que foram deliberadamente excluídos (pertence a NÃO ESCOPO), ou estimativa de esforço.

### PREMISSAS E DEPENDÊNCIAS

**Objetivo:** registrar condições concretas que precisam ser verdadeiras para que o escopo descrito seja executável como especificado.

**Deve conter:** apenas itens concretos e específicos a esta demanda, com responsável (quando conhecido) e impacto caso a premissa não se confirme.

**Não deve conter:** premissas genéricas preenchidas apenas porque a estrutura do documento tem esta seção (ver `OS-DOC-001`, `OS-SCOPE-002`). Quando não houver premissas ou dependências reais para a demanda, a seção deve indicar isso explicitamente em vez de ser preenchida artificialmente.

### NÃO ESCOPO

**Objetivo:** deixar explícito o que foi deliberadamente excluído da demanda, para evitar expectativas equivocadas.

**Deve conter:** itens específicos, no formato "Não faz parte desta demanda: `<item específico>`." (Princípio 11).

**Não deve conter:** exclusões inventadas sem base nos insumos, boilerplate reaproveitado de outras demandas, ou conteúdo que na verdade é uma premissa não satisfeita ou uma lacuna de informação.

### ESFORÇO

**Objetivo:** apresentar o esforço estimado da demanda, quando essa informação estiver disponível nos insumos.

**Deve conter:** apenas valores de esforço explicitamente informados pela fonte (cliente, gestor, responsável técnico). O formato de tabela (`Descrição` / `Esforço`, com linhas para Análise e Especificação, Desenvolvimento, Testes Internos, Gestão, TOTAL) é uma referência inicial (`OS-EFFORT-002`, `SHOULD`), não uma obrigação rígida.

**Não deve conter:** esforço estimado, calculado ou inferido pela `.osFactory` ou por qualquer agente. A `.osFactory` não calcula esforço (`OS-EFFORT-001`, `MUST`); quando o valor não estiver disponível, a célula ou o campo correspondente deve permanecer em branco ou marcado como `[OPEN_QUESTION: ...]`, nunca preenchido com uma estimativa criada pelo agente.

## Exemplos genéricos

Os exemplos abaixo são inteiramente fictícios e genéricos — não fazem referência a nenhum cliente, sistema, projeto ou demanda real. Servem apenas para ilustrar o padrão de redação esperado.

**Regra vaga vs. regra testável**

- Evitar: "O sistema deve validar corretamente os dados antes de salvar."
- Preferir: "Ao salvar o registro, o sistema deverá validar que o campo `Código` não está vazio. Se estiver vazio, o sistema não deverá permitir o salvamento e deverá apresentar a mensagem `\"Código é obrigatório\"`."

**Situação atual misturada com escopo vs. separada**

- Evitar (em uma única seção): "Atualmente o campo `Status` só pode ser alterado manualmente, mas com esta demanda ele passará a ser atualizado automaticamente quando a condição X ocorrer."
- Preferir:
  - Em SITUAÇÃO ATUAL: "O campo `Status` só pode ser alterado manualmente pelo usuário responsável."
  - Em ESCOPO: "Quando a condição X ocorrer, o sistema deverá atualizar o campo `Status` automaticamente, sem exigir ação manual."

**Premissa genérica vs. premissa concreta**

- Evitar: "O ambiente de testes deve estar disponível."
- Preferir: "A integração com o sistema `Y` depende da disponibilização de credenciais de acesso ao ambiente de homologação pela equipe responsável por `Y`. Sem essas credenciais, a validação da integração descrita em ESCOPO não pode ser concluída."

**Mensagem inventada vs. mensagem marcada como incerta**

- Evitar: "O sistema deverá exibir uma mensagem informando que o cadastro foi concluído com sucesso." *(quando o texto exato da mensagem não foi definido em nenhum insumo)*
- Preferir: "O sistema deverá exibir uma mensagem de confirmação ao usuário. `[OPEN_QUESTION: definir mensagem apresentada ao usuário]`."

## Anti-padrões de redação

1. **Frase acumuladora:** uma única frase com múltiplas condições, comportamentos e exceções misturados, exigindo releitura para separar cada afirmação.
2. **Hedging desnecessário:** uso de "poderia", "talvez", "poderá" (no sentido de incerteza, não de permissão) para uma regra já confirmada pela análise funcional.
3. **Sinônimo variável:** nomear o mesmo campo, tela ou entidade de formas diferentes ao longo do documento.
4. **Mensagem parafraseada:** reescrever ou "corrigir" o texto de uma mensagem do sistema em vez de reproduzi-la exatamente.
5. **Situação atual disfarçada de escopo:** descrever o comportamento atual já embutido dentro de uma frase de ESCOPO, sem separação clara do delta.
6. **Não Escopo como depósito:** usar NÃO ESCOPO para registrar premissas não satisfeitas, dúvidas ou lacunas de informação em vez de exclusões deliberadas.
7. **Boilerplate de premissas:** preencher PREMISSAS E DEPENDÊNCIAS com texto genérico reaproveitável em qualquer demanda, sem relação específica com o conteúdo da OS.
8. **Esforço inventado:** preencher a tabela de esforço com um valor estimado pelo agente quando a fonte não informou esforço algum.
9. **Incerteza escondida:** omitir `[OPEN_QUESTION: ...]`, `[INFERENCE: ...]` ou `[CONFLICT: ...]` para que o documento "pareça" mais completo ou definitivo do que os insumos permitem.
10. **Regra repetida:** declarar a mesma regra funcional em mais de uma seção com o risco de as versões divergirem em revisões futuras.
11. **Linguagem promocional:** usar adjetivos de valor comercial ("solução robusta", "melhoria expressiva", "experiência aprimorada") em vez de descrever o comportamento concreto.

## Relação com os outros artefatos

- `os-rules.md` é a fonte normativa: define **o que** toda OS deve, deveria, pode ou não pode conter.
- `os-style-guide.md` (este documento) define **como escrever** o conteúdo de forma clara, técnica e testável.
- `os-checklist.md` define **como verificar** se uma OS específica atende às regras e ao padrão de redação esperado.
- `os-documenter-agent.md` é **quem aplica** este guia — o agente responsável por transformar a análise funcional validada em uma OS redigida segundo os princípios aqui descritos.

## Princípio central

Escrever apenas o necessário para que negócio, desenvolvimento e QA entendam a mesma regra da mesma forma.

<!--
AVISO PARA AGENTES — NÃO REMOVER

Este Markdown define exclusivamente a estrutura e o conteúdo da OS. A identidade
visual, paginação, estilos, cabeçalhos, rodapés e demais elementos gráficos serão
definidos pelo template DOCX oficial (a criar futuramente).

Este arquivo é o esqueleto de referência inicial (`CANONICAL_CANDIDATE`, ver
`OS-DOC-002`) usado pelo `os-documenter-agent`. Ele não substitui `os-rules.md`
(fonte normativa), `os-style-guide.md` (como escrever) nem `os-checklist.md`
(como verificar) — consulte os três ao preencher cada seção. Comentários HTML
como este são instruções para quem preenche o documento e nunca devem aparecer
na OS final entregue.
-->

# Documento de Especificação Funcional

## Identificação

<!--
Campos opcionais — preencher somente quando houver fonte válida para o valor.
Não preencher com "XX", "TBD", "N/A" ou qualquer valor fictício apresentado como
se fosse informação confirmada. Quando a ausência de um campo precisar ser
resolvida antes da aprovação da OS, usar `[OPEN_QUESTION: ...]` em vez de
inventar ou deixar um placeholder genérico. Ver OS-CORE-001.
-->

- Código / Identificador da demanda:
- Nome da demanda:
- Projeto:
- Contrato:
- Solicitante:
- Aprovação:
- Responsável:
- Data:
- Versão:
- Esforço total:
- Anexos:

## Controle de versão

<!--
Cada revisão formal deve receber uma versão coerente com a anterior — não
reutilizar silenciosamente o mesmo número de versão para revisões distintas
(ver recomendação 3 de `pattern-analysis.md` e OS-CORE-001). Não inventar autor
ou data quando não houver fonte válida; nesse caso, deixar a célula em branco
ou usar `[OPEN_QUESTION: ...]`.
-->

| Versão | Data | Autor | Descrição |
| ------ | ---- | ----- | --------- |

## 1. DESCRIÇÃO

<!--
Objetivo: explicar em poucas frases a finalidade da demanda — o que está sendo
solicitado e por quê. Deve cobrir: finalidade da demanda; funcionalidade ou
processo afetado; resultado geral pretendido.
Curto e objetivo. Não incluir aqui regra detalhada, estimativa de esforço,
solução técnica ou narrativa extensa — ver `os-style-guide.md`, seção
"DESCRIÇÃO".
-->

## 2. SITUAÇÃO ATUAL

<!--
Descrever: o comportamento vigente relevante para a demanda; a limitação
conhecida que motiva a mudança; o contexto necessário para compreendê-la.
Não misturar comportamento futuro nesta seção — isso pertence a ESCOPO (ver
`os-style-guide.md`, Princípio 3). Permitir figura quando ela for evidência
útil da limitação (ver marcador de figura abaixo).
-->

## 3. ESCOPO

<!--
Seção principal da especificação. Quando aplicável, deixar explícito o delta:
Situação Atual → Mudança → Comportamento Futuro (ver OS-FUNC-001).

Subseções desta seção são DINÂMICAS: criar somente as necessárias para a
demanda, com conteúdo real. Não gerar subseção vazia apenas para seguir este
template (ver OS-DOC-003). Exemplos de possíveis subseções — nenhum título
abaixo é obrigatório nem exaustivo:

### 3.x Regras Funcionais
### 3.x Observações
### 3.x Validações
### 3.x Mensagens
### 3.x Integração
### 3.x Exceções
### 3.x Comportamento de atributos
### 3.x Criação / Edição / Exclusão

O `os-documenter-agent` decide, para cada demanda, quais desses agrupamentos
fazem sentido (ou nenhum deles, se a demanda for simples o bastante para texto
corrido).
-->

<!--
Padrão para regras: dentro do Escopo, documentar regras preferencialmente como:

**Condição:**
...

**Comportamento esperado:**
...

**Exceção:**
...

Este formato não precisa ser aplicado mecanicamente a regras simples — pode
virar bullet ou frase única quando isso melhorar a legibilidade (ver
`os-style-guide.md`, Princípio 5 e OS-FUNC-002).
-->

<!--
Mensagens: quando os insumos definirem explicitamente uma mensagem do sistema,
reproduzi-la exatamente, entre aspas, sem alterar a redação:

> "Texto exato fornecido pelos insumos"

Quando a mensagem for necessária, mas ainda não estiver definida:

`[OPEN_QUESTION: definir mensagem apresentada ao usuário]`

Nunca inventar o texto de uma mensagem (ver OS-FUNC-003).
-->

<!--
Integrações: documentar somente quando houver evidência explícita nos
insumos. Estrutura: sistema/origem → evento ou ação → informação propagada →
sistema/destino → comportamento esperado no destino → exceções conhecidas.
Não inventar API, protocolo, payload ou tecnologia não presente nos insumos —
a ausência vira `[OPEN_QUESTION: ...]` (ver OS-FUNC-004).
-->

<!--
Figuras: quando houver imagem relevante, usar um marcador conceitual
consistente, por exemplo:

`[FIGURA: descrição da evidência visual | fonte: <arquivo>]`

O marcador permite que o futuro gerador DOCX saiba onde inserir a imagem
correspondente. Não copiar a imagem para o Markdown. Não exigir figura quando
ela não tiver valor funcional (ver `os-style-guide.md`, Princípio 13).
-->

## 4. PREMISSAS E DEPENDÊNCIAS

<!--
Registrar somente condições concretas e específicas desta demanda. Quando
possível, para cada item: premissa/dependência; responsável, se conhecido;
impacto caso não seja atendida. Não usar boilerplate genérico (ver OS-DOC-001
e OS-SCOPE-002). Se não houver informação válida, não inventar conteúdo — e
não preencher a seção apenas porque o template a possui.
-->

## 5. NÃO ESCOPO

<!--
Registrar exclusões concretas e suportadas pelos insumos, no formato:

- Não faz parte desta demanda: `<item específico>`.

Não inventar itens. Não usar texto genérico apenas para preencher a seção
(ver OS-SCOPE-002).
-->

## 6. ESFORÇO

<!--
Preencher somente quando houver informação proveniente de fonte válida. Esta
tabela é `CANONICAL_CANDIDATE` (OS-EFFORT-002) — o agente pode adaptar o
formato quando uma fonte válida fornecer estrutura diferente. A `.osFactory`
nunca calcula ou inventa esforço nesta etapa (OS-EFFORT-001, MUST). Quando o
esforço ainda não tiver sido definido e isso não bloquear a especificação, a
seção pode permanecer sem valores confirmados.
-->

| Descrição               | Esforço |
| ------------------------ | ------: |
| Análise e Especificação  |         |
| Desenvolvimento          |         |
| Testes Internos          |         |
| Gestão                   |         |
| **TOTAL**                |         |

## 7. CONDIÇÕES COMERCIAIS

<!--
Preencher somente com informação proveniente de fonte válida dos insumos.
Campos mínimos: Horas contratadas; Valor total da OS; Forma/condição de
pagamento. Campos opcionais, quando houver fonte: Prazo de pagamento;
Validade da OS; Início previsto; Prazo de execução. Ausência de valor ou de
forma de pagamento é `[OPEN_QUESTION: ...]` — nunca `[DISCOVERY_ITEM: ...]`
nem estimativa inventada (OS-QA-004, OS-EFFORT-001). Código da OS, Contratante
e Executor NÃO são preenchidos aqui — são resolvidos e exibidos na capa pela
materialização (`tools/build_os_docx.py`), a partir do registry e de
`config/os-factory.json` (OS-CODE-001 / OS-CODE-002).
-->

- Horas contratadas:
- Valor total da OS:
- Forma / condição de pagamento:

## 8. ACEITE

<!--
Texto padrão informando o método de aceite (E-mail, na v1 — ver
`config/os-factory.json`). Não declarar que o aceite já ocorreu (OS-CODE-003).
Data do aceite, Aprovado por e Referência do aceite só existem mediante
confirmação explícita, preenchida na capa pela materialização — não redigir
esses campos livremente aqui.
-->

- Método de aceite: E-mail.

O aceite desta Ordem de Serviço poderá ser formalizado por meio de resposta de concordância ao e-mail utilizado para encaminhamento deste documento. Para fins de rastreabilidade, o aceite deverá referenciar o código e a versão da Ordem de Serviço, indicados na capa e no Controle de versão deste documento.

## Marcadores de incerteza

Durante a elaboração, use os marcadores padronizados sempre que necessário:

- `[OPEN_QUESTION: ...]` — lacuna a esclarecer, cuja resposta é necessária para fechar a especificação.
- `[DISCOVERY_ITEM: ...]` — informação ainda não conhecida, mas cuja descoberta já está prevista pelos insumos como parte de uma etapa futura (Discovery, Engenharia Reversa, Refinamento, Levantamento técnico, Mapeamento, Validação em ambiente, inspeção de sistema existente). Não é a mesma coisa que `OPEN_QUESTION` — ver OS-UNCERTAINTY-004. Não há seção obrigatória de "Discovery Items" nesta OS; o marcador aparece onde for funcionalmente relevante.
- `[INFERENCE: ...]` — conclusão razoável, ainda não confirmada explicitamente.
- `[FUNCTIONAL_CONFLICT: ...]` — contradição entre insumos que afeta regra de negócio, comportamento, escopo, condição, exceção, validação, mensagem obrigatória, fluxo funcional ou critério de aceite.
- `[ARCHITECTURAL_CONFLICT: ...]` — contradição entre insumos sobre tecnologia, framework, componente, arquitetura, mecanismo técnico ou estratégia de implantação.
- `[DOCUMENTAL_CONFLICT: ...]` — contradição entre insumos em informação documental ou administrativa (data, responsável, versão, referência de contrato), sem impacto funcional direto.
- `[CONFLICT_UNCLASSIFIED: ...]` — contradição entre insumos ainda sem informação suficiente para classificar o tipo.

Eles são temporários: uma OS classificada como `PASS` pelo `os-validator-agent`
não deve conter condição bloqueante ainda não resolvida (ver OS-UNCERTAINTY-001
a 005 e OS-QA-001). Um `DISCOVERY_ITEM` válido e controlado, ou um
`ARCHITECTURAL_CONFLICT`/`DOCUMENTAL_CONFLICT` não bloqueante, não são, por si
só, condição bloqueante. `FUNCTIONAL_CONFLICT` relevante e
`CONFLICT_UNCLASSIFIED` permanecem pendência até classificação/resolução.

## Relação com o DOCX

1. Este Markdown é a representação canônica de conteúdo da OS.
2. `04-templates/docx/os-padrao.docx` é a fonte de verdade visual (identidade
   Tria: cores, fonte, cabeçalho, capa) — ver `os-documenter-agent.md` e
   `tools/build_os_docx.py`.
3. O gerador DOCX (`tools/build_os_docx.py`) preserva a hierarquia semântica
   deste arquivo e nunca reinterpreta conteúdo funcional; a capa (Código da
   OS, Contratante, Executor, Data de emissão, Versão, Status) e o Autor da
   tabela de Controle de versão são resolvidos/normalizados na materialização,
   não escritos livremente neste Markdown (OS-CODE-002).
4. Alterações visuais não devem alterar o significado funcional do conteúdo.
5. Imagens são inseridas nos pontos indicados pelos marcadores de figura
   (`[FIGURA: ...]`).

## Princípio central

> O template fornece estrutura para a informação disponível; nunca força a criação de informação ausente.

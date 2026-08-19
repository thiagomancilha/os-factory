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

## Marcadores de incerteza

Durante a elaboração, use os marcadores padronizados sempre que necessário:

- `[OPEN_QUESTION: ...]` — lacuna a esclarecer.
- `[INFERENCE: ...]` — conclusão razoável, ainda não confirmada explicitamente.
- `[CONFLICT: ...]` — contradição entre insumos.

Eles são temporários: uma OS classificada como `PASS` pelo `os-validator-agent`
não deve conter condição bloqueante ainda não resolvida (ver OS-UNCERTAINTY-001
a 003 e OS-QA-001).

## Relação com o DOCX

1. Este Markdown é a representação canônica de conteúdo da OS.
2. O futuro template DOCX será a fonte de verdade visual.
3. O gerador DOCX deverá preservar a hierarquia semântica deste arquivo.
4. Alterações visuais não devem alterar o significado funcional do conteúdo.
5. Imagens deverão ser inseridas nos pontos indicados pelos marcadores de
   figura (`[FIGURA: ...]`).

## Princípio central

> O template fornece estrutura para a informação disponível; nunca força a criação de informação ausente.

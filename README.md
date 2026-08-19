# .osFactory

Factory baseada em agentes para geração padronizada de **Especificações Funcionais / Ordens de Serviço (OS)**.

## Objetivo

A `.osFactory` tem como objetivo transformar uma descrição inicial de problema ou necessidade em uma Especificação Funcional / Ordem de Serviço estruturada.

A entrada pode ser complementada por documentos, imagens, prints, e-mails, regras de negócio e outras evidências relevantes para o entendimento da demanda.

A factory deverá apoiar progressivamente o processo de:

* entendimento do problema;
* análise dos insumos;
* identificação da situação atual;
* definição do escopo;
* detalhamento de regras e comportamentos;
* identificação de premissas e dependências;
* definição de não escopo;
* estimativa de esforço;
* validação da consistência da especificação;
* geração do documento final.

## Conceito de entrada

O input mínimo é uma descrição textual do problema ou necessidade.

Exemplo:

```text
Atualmente o sistema permite excluir legenda apenas de Trecho Primário
e Trecho Secundário.

Precisamos permitir também a exclusão da legenda de postes.
```

Opcionalmente, a demanda pode conter:

* documentos;
* imagens;
* prints de tela;
* e-mails;
* regras de negócio;
* requisitos;
* referências técnicas;
* exemplos;
* outras evidências relevantes.

## Conceito de saída

O resultado esperado é uma **Ordem de Serviço** — com identidade visual Tria (capa, código rastreável `OS-<AAAA>-<NNNN>`, Contratante/Executor, condições comerciais e aceite), não apenas uma especificação funcional — construída a partir dos insumos fornecidos e das regras, padrões, templates e exemplos mantidos pela própria factory. Quando a validação retornar `PASS` ou `PASS_WITH_WARNINGS`, a OS é materializada também em **DOCX**, a partir do template oficial (`04-templates/docx/os-padrao.docx`); em `BLOCKED`, nenhum DOCX é gerado como documento final. A prontidão para aceite (`READY_FOR_ACCEPTANCE`/`NOT_READY_FOR_ACCEPTANCE`) é avaliada separadamente do gate funcional — pendências comerciais (valor, forma de pagamento) nunca bloqueiam a especificação funcional.

A factory não deve inventar informações ausentes ou ampliar silenciosamente o escopo informado.

## Uso

```text
Gerar OS para <demanda>
```

Entrada: `00-inbox/<demanda>/`
Saída: `05-output/<demanda>/`

Pipeline: intake → análise → documentação → validação → DOCX

Ver `99-prompts/gerar-os.md` para o fluxo completo (agentes, gate de validação e materialização DOCX).

## Estrutura

```text
.osFactory/
├── 00-inbox/
├── 01-analysis/
│   └── _runtime/          # os-registry.json (local, ignorado pelo Git)
├── 02-agents/
├── 03-knowledge-base/
│   ├── standards/
│   ├── rules/
│   └── examples/
├── 04-templates/
│   └── docx/
│       └── os-padrao.docx
├── 05-output/
├── config/
│   └── os-factory.json    # Contratante/Executor/Autor/método de aceite padrão
├── tools/
├── tests/
├── requirements.txt
└── README.md
```

### `00-inbox/`

Entrada das demandas e seus respectivos insumos.

### `01-analysis/`

Artefatos intermediários produzidos durante o entendimento e análise da demanda.

### `02-agents/`

Agentes especializados responsáveis pelas diferentes etapas do processo de geração da OS.

### `03-knowledge-base/`

Base de conhecimento utilizada pelos agentes.

#### `standards/`

Padrões para elaboração das especificações.

#### `rules/`

Regras que devem ser respeitadas durante análise e geração dos documentos.

#### `examples/`

Exemplos reais utilizados como referência para evolução dos padrões da factory.

### `04-templates/`

Templates utilizados para geração dos documentos, incluindo `docx/os-padrao.docx` — fonte de verdade **visual** da OS (o Markdown continua sendo a fonte de verdade de **conteúdo**).

### `05-output/`

Artefatos finais produzidos pela `.osFactory` (Markdown, DOCX e preview de renderização).

### `tools/`

Scripts genéricos de materialização e auditoria: `build_os_docx.py` (Markdown → DOCX, resolve código da OS e dados institucionais), `os_registry.py` (registry local demanda → código da OS), `audit_os_visual_format.py` (auditoria estrutural do DOCX) e `render_docx_with_word.ps1` (DOCX → PDF → PNG via Word COM, para inspeção visual real). Nenhum script é específico de cliente ou demanda.

### `config/`

`os-factory.json` — defaults institucionais versionados (Contratante, Executor, Autor, formato do código, método de aceite). Nunca contém dado de cliente ou de demanda.

## Princípio

> O usuário descreve o problema e fornece os insumos disponíveis. A `.osFactory` transforma essas informações progressivamente em uma especificação funcional clara, consistente, rastreável e pronta para evolução, estimativa e execução.

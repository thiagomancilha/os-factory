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

O resultado esperado é uma **Especificação Funcional / Ordem de Serviço padronizada**, construída a partir dos insumos fornecidos e das regras, padrões, templates e exemplos mantidos pela própria factory.

A factory não deve inventar informações ausentes ou ampliar silenciosamente o escopo informado.

## Estrutura

```text
.osFactory/
├── 00-inbox/
├── 01-analysis/
├── 02-agents/
├── 03-knowledge-base/
│   ├── standards/
│   ├── rules/
│   └── examples/
├── 04-templates/
├── 05-output/
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

Templates utilizados para geração dos documentos.

### `05-output/`

Artefatos finais produzidos pela `.osFactory`.

## Princípio

> O usuário descreve o problema e fornece os insumos disponíveis. A `.osFactory` transforma essas informações progressivamente em uma especificação funcional clara, consistente, rastreável e pronta para evolução, estimativa e execução.

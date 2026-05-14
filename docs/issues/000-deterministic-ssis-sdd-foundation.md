# Issue Draft: Consolidar gerador deterministico de SDD para SSIS

## Titulo sugerido

Consolidar gerador deterministico de SDD para projetos SSIS

## Contexto

O projeto evoluiu de um scaffold inicial para uma aplicacao capaz de processar artefatos SQL Server Integration Services e gerar documentacao SDD em Markdown, alem de uma saida JSON canonica para consumo futuro por IA ou ferramentas externas.

Esta issue registra o estado atual anterior ao trabalho da especializacao de IA.

## Objetivo

Consolidar a base deterministica da aplicacao, garantindo que ela consiga:

- receber como parametro o caminho real da pasta SSIS;
- detectar o nome do projeto SSIS;
- processar pacotes `.dtsx`;
- extrair metadados tecnicos;
- gerar SDD Markdown com estrutura propria para SSIS;
- gerar `project.json` e `packages/*.json`;
- organizar os resultados por execucao.

## Escopo entregue

- CLI com `--ssis-folder`, mantendo `--project-folder` como alias legado.
- Saida em subpasta `NOME_PROJETO_yyyyMMdd_HHmmss`.
- Descoberta do nome do projeto por `.dtproj`, `.sln` ou `.ispac`.
- Parsers iniciais para `.dtsx`, `.conmgr` e `.ispac`.
- Extractors para conexoes, variaveis, SQL, Control Flow e Data Flow.
- Mascaramento de segredos em connection strings.
- Estrutura SDD revisada para SSIS:
  - specification metadata;
  - package purpose;
  - execution contract;
  - technical inventory;
  - data contract;
  - control flow specification;
  - data flow specification;
  - SQL specification;
  - business rules;
  - operational requirements;
  - risks, gaps and open questions;
  - implementation backlog.
- JSON canonico deterministico:
  - `project.json`;
  - `packages/*.json`.
- Testes automatizados para CLI, parsers, SDD e JSON.
- README, TEST_PLAN e checklist atualizados.

## Fora de escopo

- Enriquecimento por IA.
- Especialista IA em SSIS SDD.
- Structured Outputs.
- Validacao anti-alucinacao.
- Geracao automatica de projeto SSIS executavel.

## Branch

```text
deterministic-ssis-sdd-foundation
```

## Criterios de aceite

- [ ] A CLI processa uma pasta SSIS informada por `--ssis-folder`.
- [ ] A saida e criada em subpasta com nome real do projeto e timestamp.
- [ ] O Markdown segue estrutura SDD propria para SSIS.
- [ ] `project.json` e gerado na pasta da execucao.
- [ ] `packages/*.json` e gerado por pacote.
- [ ] Segredos sao mascarados no Markdown e no JSON.
- [ ] Suite de testes passa.

## Validacao atual

```text
python -m unittest discover -v
python -m compileall app tests
```

Resultado esperado:

```text
9 tests passed
compileall passed
```

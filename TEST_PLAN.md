# Test Plan

Plano de testes para validar que a solucao gera SDD tecnico aplicavel a projetos SSIS.

## 1. Objetivo

Validar que a solucao consegue ler artefatos SSIS, extrair metadados tecnicos relevantes e gerar documentacao SDD em Markdown com qualidade suficiente para apoiar implementacao, manutencao ou modernizacao do projeto SSIS.

## 2. Escopo

Inclui:

- leitura de `.dtsx`;
- leitura de `.conmgr`;
- inspecao de `.ispac`;
- extracao de conexoes, variaveis, parametros, control flow, data flow e SQL;
- mascaramento de segredos;
- geracao de Markdown SDD;
- geracao de JSON canonico deterministico;
- geracao de indice para multiplos pacotes;
- execucao via CLI.

Nao inclui:

- recomendacoes Microsoft Fabric;
- scoring de migracao;
- arquitetura de destino;
- validacao funcional do pacote SSIS em runtime.

## 3. Testes unitarios

### `DtsxParser`

- [ ] Pacote valido com namespace SSIS.
- [ ] Pacote com nome, creator, package id e versao.
- [ ] Pacote com connection manager embutido.
- [ ] Pacote com variavel.
- [ ] Pacote com parametro.
- [ ] Pacote com Execute SQL Task.
- [ ] Pacote com Data Flow Task.
- [ ] XML invalido.

### `ConnectionManagerParser`

- [ ] Conexao OLE DB.
- [ ] Conexao ADO.NET.
- [ ] Conexao Flat File.
- [ ] Conexao Excel.
- [ ] Connection string com senha.
- [ ] Connection string sem senha.
- [ ] Arquivo `.conmgr` invalido.

### `IspacParser`

- [ ] `.ispac` com `.dtsx`.
- [ ] `.ispac` com `.conmgr`.
- [ ] `.ispac` com `.params`.
- [ ] Arquivo que nao e zip valido.

### Extractors

- [ ] `ConnectionsExtractor`: tipo, servidor, database, provider e file path.
- [ ] `VariablesExtractor`: nome, namespace, tipo, valor e expression.
- [ ] `SqlExtractor`: SQL literal, SQL dinamico, objetos referenciados e variaveis referenciadas.
- [ ] `ControlFlowExtractor`: tasks conhecidas, tasks desconhecidas, constraints e containers.
- [ ] `DataFlowExtractor`: source, destination, lookup, derived column, conditional split e mappings.

## 4. Testes de seguranca

Garantir que nenhum segredo seja exposto no SDD.

Valores sensiveis a validar:

```text
Password=abc
Pwd=abc
Token=abc
Access Token=abc
Secret=abc
Client Secret=abc
AccountKey=abc
SharedAccessKey=abc
```

Critérios:

- [ ] Markdown final contem `***` para valores sensiveis.
- [ ] Markdown final nao contem o valor real do segredo.
- [ ] Connection strings em tabelas ou listas tambem ficam mascaradas.

## 5. Testes de geracao do SDD

Validar que o Markdown gerado contem:

- [ ] `# SDD: ...`
- [ ] `## 1. Specification Metadata`
- [ ] `## 2. Package Purpose`
- [ ] `## 3. Execution Contract`
- [ ] `## 4. Technical Inventory`
- [ ] `## 5. Data Contract`
- [ ] `## 6. Control Flow Specification`
- [ ] `## 7. Data Flow Specification`
- [ ] `## 8. SQL Specification`
- [ ] `## 9. Business Rules`
- [ ] `## 10. Operational Requirements`
- [ ] `## 11. Risks, Gaps, And Open Questions`
- [ ] `## 12. Implementation Backlog`

Validar tambem:

- [ ] tabelas Markdown validas;
- [ ] blocos SQL com fenced code block;
- [ ] secoes vazias com mensagem padronizada;
- [ ] nomes de arquivos seguros;
- [ ] pasta de execucao no formato `NOME_PROJETO_yyyyMMdd_HHmmss`;
- [ ] `index.md` dentro da pasta de execucao quando houver multiplos pacotes;
- [ ] ausencia de recomendacoes Fabric ou de outra plataforma no SDD.

## 6. Testes de JSON canonico

- [ ] `project.json` e gerado dentro da pasta da execucao.
- [ ] `packages/*.json` e gerado para cada pacote processado.
- [ ] `project.json` contem `schema_version`.
- [ ] `project.json` contem nome do projeto SSIS.
- [ ] `project.json` contem resumo da execucao.
- [ ] `project.json` contem lista de pacotes processados.
- [ ] JSON por pacote contem conexoes, parametros, variaveis, tasks, data flows e SQL.
- [ ] JSON nao contem segredos em claro nas connection strings.

## 7. Testes de CLI

Comandos principais:

```bash
python -m app.main --help
python -m app.main --ssis-folder ./input --output-folder ./output
python -m app.main --ssis-folder ./tests/fixtures --output-folder ./output
python -m app.main --ssis-folder "C:/SSIS/My Project" --output-folder ./output
```

Casos:

- [ ] `--help` retorna codigo `0`.
- [ ] Pasta vazia retorna codigo `1` e mensagem clara.
- [ ] Pasta inexistente retorna codigo `1`.
- [ ] Pasta com `.dtsx` valido retorna codigo `0`.
- [ ] Caminho absoluto para pasta SSIS retorna codigo `0`.
- [ ] Caminho com espacos funciona quando informado entre aspas.
- [ ] Alias legado `--project-folder` continua funcionando.
- [ ] Pasta com multiplos `.dtsx` gera multiplos Markdown e `index.md` dentro da pasta de execucao.
- [ ] Arquivo invalido nao impede processamento dos demais.
- [ ] Logs mostram pacotes lidos, arquivos gerados, avisos e erros.

## 8. Testes de integracao

Validar o fluxo completo:

```text
input SSIS -> parser -> extractors -> package_data -> MarkdownWriter -> output SDD
```

Cenarios:

- [ ] um pacote simples;
- [ ] multiplos pacotes;
- [ ] pacote com `.conmgr`;
- [ ] pacote com Data Flow;
- [ ] pacote com SQL dinamico;
- [ ] pacote com Script Task;
- [ ] pacote com Sequence Container ou Foreach Loop;
- [ ] pacote com arquivo invalido misturado.

## 9. Fixtures recomendadas

Fixtures sinteticas e anonimizadas:

```text
tests/fixtures/
|-- simple_execute_sql.dtsx
|-- data_flow_basic.dtsx
|-- variables_and_parameters.dtsx
|-- script_task.dtsx
|-- containers_and_precedence.dtsx
|-- flat_file_connection.conmgr
|-- excel_connection.conmgr
|-- invalid_xml.dtsx
|-- sample_project.ispac
```

Cada fixture deve testar um comportamento especifico.

## 10. Testes manuais com projeto real

Checklist manual:

- [ ] Identificar o caminho real da pasta do projeto SSIS.
- [ ] Rodar CLI usando `--ssis-folder`.
- [ ] Abrir Markdown gerado.
- [ ] Conferir nome do pacote.
- [ ] Conferir conexoes.
- [ ] Conferir variaveis e parametros.
- [ ] Conferir tasks.
- [ ] Conferir SQL.
- [ ] Conferir Data Flow.
- [ ] Confirmar que senhas foram mascaradas.
- [ ] Validar se o SDD e util para alguem implementar ou manter o pacote.
- [ ] Registrar divergencias como novas fixtures automatizadas.

## 11. Criterios de aceite

A solucao passa quando:

- [ ] todos os testes automatizados passam;
- [ ] a CLI processa pacotes reais ou sinteticos;
- [ ] o SDD contem informacoes tecnicas suficientes;
- [ ] nenhum segredo aparece no output;
- [ ] erros sao reportados de forma clara;
- [ ] multiplos pacotes geram indice;
- [ ] todos os arquivos gerados ficam dentro de uma pasta por execucao;
- [ ] JSON canonico e gerado junto do Markdown;
- [ ] o documento nao inclui recomendacoes Fabric ou de outra plataforma.

## 12. Comandos de validacao

```bash
python -m compileall app tests
python -m unittest discover -v
```

Validacoes opcionais:

```bash
python -m black --check app tests
python -m ruff check app tests
```

## 13. Proximos testes prioritarios

- [ ] Pacote com multiplos `.dtsx` para validar `index.md`.
- [ ] Fixture com XML invalido misturado com pacote valido.
- [ ] Fixture com secrets variados.
- [ ] Fixture com Sequence Container ou Foreach Loop.
- [ ] Fixture com Data Flow mais realista.

# Implementation Checklist

Memoria viva das pendencias do projeto. Marque cada item conforme avancarmos e registre observacoes curtas quando uma decisao tecnica mudar o caminho.

## 1. Fundacao do fluxo de execucao

- [x] Implementar CLI em `app/main.py` com `--project-folder` e `--output-folder`.
- [x] Integrar `app/config.py` ao fluxo principal, respeitando variaveis de ambiente e argumentos CLI.
- [x] Validar existencia dos diretorios de entrada e saida antes da execucao.
- [x] Adicionar mensagens de erro claras para entrada ausente, pasta vazia ou extensoes nao suportadas.
- [x] Configurar logging com `loguru` usando `LOG_LEVEL`.
- [x] Registrar resumo final da execucao: pacotes lidos, arquivos gerados, avisos e erros.

## 2. Modelos de dominio

- [x] Definir `SSISProject` com pacotes, conexoes compartilhadas e metadados do projeto.
- [x] Definir `SSISPackage` com nome, caminho, conexoes, variaveis, parametros, tasks, data flows e SQLs.
- [x] Definir `SSISTask` com identificador, nome, tipo, ordem/dependencias e propriedades relevantes.
- [x] Definir `SSISConnection` com nome, tipo, connection string, provider, servidor, database e atributos sensiveis mascarados.
- [x] Decidir se os modelos serao `dataclasses`, `pydantic` ou classes simples.
- [x] Garantir serializacao simples dos modelos para uso no builder de Markdown.

## 3. Parsing de arquivos SSIS

- [x] Evoluir `DtsxParser` para lidar corretamente com namespaces XML do SSIS.
- [x] Extrair metadados basicos do pacote `.dtsx`: nome, versao, creator, creation date e package id quando disponiveis.
- [x] Implementar leitura de connection managers embutidos em `.dtsx`.
- [x] Implementar `ConnectionManagerParser` para arquivos `.conmgr`.
- [x] Implementar `IspacParser` para abrir `.ispac` como zip e localizar `.dtsx`, `.conmgr`, project params e manifestos.
- [x] Tratar XML invalido, arquivos corrompidos e pacotes parcialmente legiveis sem interromper toda a execucao.

## 4. Extractors essenciais

- [x] Implementar `ConnectionsExtractor`.
- [x] Implementar `VariablesExtractor`.
- [x] Implementar `SqlExtractor`.
- [x] Implementar `ControlFlowExtractor`.
- [x] Implementar `DataFlowExtractor`.
- [x] Normalizar saidas dos extractors para alimentar `SSISPackage`.
- [x] Preservar informacoes desconhecidas relevantes em campos genericos para diagnostico.

## 5. Extracao de conexoes e variaveis

- [x] Identificar conexoes OLE DB, ADO.NET, Flat File, Excel e outras comuns.
- [x] Mascarar senhas, tokens e segredos em connection strings.
- [x] Extrair parametros de projeto e pacote quando existirem.
- [x] Extrair variaveis, escopo, namespace, tipo e valor default quando disponivel.
- [x] Relacionar variaveis e parametros ao uso em SQL, conexoes e expressions.

## 6. Extracao de Control Flow

- [x] Identificar tasks principais: Execute SQL Task, Data Flow Task, Script Task, File System Task, FTP/SFTP, Sequence Container e Foreach Loop.
- [x] Capturar precedencias entre tasks.
- [x] Capturar constraints, expressions e condicoes de execucao.
- [x] Representar containers e tarefas aninhadas.
- [x] Registrar tasks desconhecidas como itens analisaveis, sem descarta-las.

## 7. Extracao de Data Flow

- [x] Identificar fontes, destinos e transformacoes.
- [x] Capturar mapeamentos de colunas quando disponiveis.
- [x] Capturar componentes de lookup, derived column, conditional split, aggregate, sort, merge e union all.
- [x] Relacionar data flows com conexoes usadas.
- [x] Registrar possiveis gargalos de migracao, como script components e transformacoes customizadas.

## 8. Extracao de SQL

- [x] Extrair comandos SQL de Execute SQL Tasks.
- [x] Extrair queries de sources e lookups em Data Flow.
- [x] Diferenciar SQL literal, SQL por expression e SQL em variavel.
- [x] Detectar stored procedures, tabelas, views e comandos DDL/DML quando possivel.
- [x] Guardar SQL formatado em blocos Markdown seguros.
- [x] Registrar SQL dinamico como risco de migracao.

## 9. Geracao de SDD Markdown

- [x] Enriquecer `PACKAGE_TEMPLATE` com estrutura final de SDD.
- [x] Atualizar `SpecBuilder` para preencher todas as secoes com dados reais.
- [x] Gerar secoes de Inputs, Outputs, Connections, Parameters and Variables, Control Flow, Data Flow e SQL Commands.
- [x] Adicionar secao de Business Rules inferidas a partir de SQL, constraints e transformacoes.
- [x] Adicionar secao de Risks and Attention Points.
- [x] Gerar nomes de arquivo estaveis e seguros para sistemas de arquivos.
- [x] Criar indice geral do projeto quando houver multiplos pacotes.

## 10. Limite de escopo para assessments externos

- [x] Remover recomendacoes especificas de Microsoft Fabric do SDD principal.
- [x] Manter backlog neutro de implementacao no SDD.
- [x] Documentar que assessments de plataforma devem ser feitos por aplicacao separada.
- [x] Preservar dados tecnicos suficientes para uma aplicacao externa consumir o SDD futuramente.

## 11. Testes e fixtures

- [x] Criar estrutura de testes.
- [x] Adicionar fixtures pequenas para `.dtsx`.
- [x] Adicionar fixture para `.conmgr`.
- [x] Adicionar fixture ou mock para `.ispac`.
- [x] Testar CLI com diretorio de entrada e saida temporarios.
- [x] Testar parsing de XML com namespaces.
- [x] Testar mascaramento de segredos.
- [x] Testar geracao Markdown.
- [x] Testar comportamento com arquivos invalidos ou incompletos.

## 12. Documentacao

- [x] Atualizar README com comandos reais.
- [x] Documentar formato de entrada suportado.
- [x] Documentar estrutura de saida.
- [x] Adicionar exemplo de Markdown gerado.
- [x] Registrar limitacoes conhecidas.
- [x] Detalhar metodologia de geracao de SDD em `docs/sdd-generation-methodology.md`.
- [x] Expandir specs em `specs/` conforme o comportamento implementado.

## 13. Qualidade operacional

- [x] Definir padrao de formatacao e lint.
- [x] Adicionar comandos de desenvolvimento ao README.
- [x] Revisar dependencias em `requirements.txt`.
- [x] Avaliar se `pandas` e `openpyxl` sao realmente necessarios no escopo inicial.
- [x] Adicionar `.gitignore` para ambientes virtuais, caches e saidas geradas.
- [x] Garantir que `input/.gitkeep` e `output/.gitkeep` sejam preservados.

## 14. Evolucao para SDD enriquecido por IA

### Fase 1: JSON canonico deterministico

- [x] Definir schema canonico `project.json` para representar o projeto SSIS processado.
- [x] Incluir no JSON metadados do projeto, pacotes, conexoes, parametros, variaveis, control flow, data flow, SQL, riscos e gaps.
- [x] Gerar `project.json` dentro da pasta de saida da execucao.
- [x] Gerar um JSON por pacote, quando util, para facilitar analise incremental.
- [x] Garantir que o Markdown continue sendo gerado a partir dos dados deterministico-extraidos.
- [x] Adicionar testes para validar estrutura minima do JSON.
- [x] Documentar o contrato do `project.json`.

### Fase 2: Enriquecimento por IA com Structured Outputs

- [ ] Adicionar dependencia/configuracao opcional para OpenAI API sem tornar IA obrigatoria.
- [ ] Definir schema de saida da IA para campos como `package_purpose`, `execution_summary`, `business_rules`, `reconstruction_notes`, `open_questions` e `implementation_backlog`.
- [ ] Criar modulo de enriquecimento que consome o JSON canonico e retorna JSON estruturado validado.
- [ ] Usar `gpt-5.4` como modelo padrao configuravel.
- [ ] Permitir configurar modelo via `.env` ou parametro CLI.
- [ ] Adicionar parametro CLI para habilitar IA explicitamente, por exemplo `--enhance-with-ai`.
- [ ] Garantir fallback deterministico quando IA estiver desabilitada ou falhar.
- [ ] Registrar no Markdown quais secoes foram geradas por IA.

### Fase 3: Revisao opcional de qualidade

- [ ] Adicionar etapa opcional de revisao final usando modelo mais forte, como `gpt-5.5`.
- [ ] Criar prompt de revisao para verificar clareza, completude, lacunas e capacidade de reconstrucao.
- [ ] Gerar secao `Reconstruction Notes` no SDD.
- [ ] Gerar secao `Open Questions For Package Owner` no SDD.
- [ ] Permitir executar revisao apenas quando solicitada por parametro CLI.

### Fase 4: Validacao anti-alucinacao

- [ ] Validar que a IA nao cita conexoes, tasks, variaveis, parametros, componentes ou SQL inexistentes no JSON canonico.
- [ ] Marcar afirmacoes inferidas como inferidas, nao como fatos extraidos.
- [ ] Adicionar testes com saidas simuladas da IA.
- [ ] Falhar ou alertar quando a resposta da IA violar o schema esperado.
- [ ] Registrar divergencias no SDD em uma secao de `AI Validation Notes`.

### Fase 5: Preparacao para reproducibilidade de projeto SSIS

- [ ] Identificar lacunas que impedem reconstruir um pacote SSIS equivalente.
- [ ] Expandir parser para event handlers, expressions, package configurations, logging e propriedades avancadas.
- [ ] Expandir Data Flow para mapeamento detalhado de colunas, external metadata columns e error outputs.
- [ ] Gerar uma secao `Rebuild Checklist` por pacote.
- [ ] Avaliar uma saida futura em formato de especificacao executavel ou scaffold de projeto.

## Registro de avancos

Use esta secao para registrar marcos importantes durante a codificacao.

| Data | Avanco | Observacoes |
| --- | --- | --- |
| 2026-05-14 | Checklist inicial criado | Baseado na leitura da estrutura atual do projeto. |
| 2026-05-14 | Fundacao do fluxo de execucao implementada | CLI, configuracao, validacao de entrada, logging e resumo final adicionados. Verificacao por execucao ficou bloqueada pelo launcher Python local. |
| 2026-05-14 | Modelos de dominio definidos | `SSISProject`, `SSISPackage`, `SSISTask` e `SSISConnection` implementados como `dataclasses` serializaveis. |
| 2026-05-14 | Parsing basico implementado | `DtsxParser` extrai metadados e conexoes embutidas; `ConnectionManagerParser` e `IspacParser` ganharam implementacao inicial. |
| 2026-05-14 | Extractors essenciais conectados | Conexoes, variaveis, SQL, control flow e data flow passam a alimentar `SSISPackage` com saidas normalizadas. |
| 2026-05-14 | SDD Markdown enriquecido | Builder agora renderiza metadados, conexoes mascaradas, variaveis, parametros, control flow, data flow, SQL, regras inferidas, riscos e recomendacao inicial. |
| 2026-05-14 | Validacao basica executada | Dependencias instaladas, `compileall app` passou, `--help` funcionou e entrada vazia retornou erro controlado. |
| 2026-05-14 | Testes automatizados adicionados | Suite `unittest` cobre CLI, parsers DTSX/CONMGR/ISPAC, mascaramento de segredos e geracao Markdown; 7 testes passaram. |
| 2026-05-14 | Documentacao e dependencias revisadas | README, metodologia e specs foram atualizados; dependencias nao usadas no escopo inicial foram removidas de `requirements.txt`. |
| 2026-05-14 | Padrao de lint e formatacao definido | `pyproject.toml` configurado para Black e Ruff; comandos documentados no README. |
| 2026-05-14 | Escopo reposicionado para SDD SSIS | Assessment Fabric removido do core; aplicacoes de assessment ficam como consumidoras externas do SDD gerado. |
| 2026-05-14 | Plano de testes registrado | `TEST_PLAN.md` criado com estrategia de testes para parsers, extractors, SDD, CLI, seguranca e fixtures futuras. |
| 2026-05-14 | Entrada SSIS por parametro adicionada | CLI passou a aceitar `--ssis-folder` para apontar diretamente para a pasta real do projeto SSIS, mantendo `--project-folder` como alias legado. |
| 2026-05-14 | Saida por execucao organizada | Arquivos gerados agora ficam em subpasta `NOME_PROJETO_yyyyMMdd_HHmmss` dentro do diretorio de saida. |
| 2026-05-14 | Estrutura SDD para SSIS revisada | Template reorganizado para contrato de execucao, inventario tecnico, contrato de dados, especificacoes de fluxo, requisitos operacionais, riscos e backlog. |
| 2026-05-14 | Nome real do projeto SSIS na pasta de saida | Nome da pasta de execucao agora prioriza `.dtproj`, depois `.sln`, depois `.ispac`, antes de usar o nome da pasta informada. |
| 2026-05-14 | Roadmap de IA registrado | Pendencias organizadas em fases: JSON canonico, enriquecimento com Structured Outputs, revisao, validacao anti-alucinacao e reproducibilidade SSIS. |
| 2026-05-14 | Fase 1 concluida | `project.json` e `packages/*.json` canonicos adicionados como saida deterministica para consumo futuro por IA ou ferramentas externas. |

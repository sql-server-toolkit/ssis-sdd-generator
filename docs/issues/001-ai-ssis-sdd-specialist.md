# Issue Draft: Implementar especialista IA em SSIS SDD

## Titulo sugerido

Implementar especialista IA para enriquecimento de SDD de projetos SSIS

## Contexto

A aplicacao ja gera SDD Markdown e JSON canonico deterministico (`project.json` e `packages/*.json`) a partir de projetos SQL Server Integration Services.

O resultado deterministico e util como inventario tecnico, mas ainda nao atinge sozinho o nivel desejado de um SDD orientado a entrega, capaz de apoiar reconstrucao, manutencao ou evolucao de um projeto SSIS com alto grau de clareza.

Para melhorar a qualidade do SDD sem comprometer rastreabilidade, a IA deve atuar como uma camada especializada de enriquecimento, consumindo o JSON canonico e produzindo uma saida estruturada validada.

## Objetivo

Criar uma especializacao de IA chamada `SSIS SDD Specialist`, responsavel por transformar metadados extraidos de pacotes SSIS em secoes narrativas e verificaveis de SDD, separando fatos extraidos, inferencias e lacunas.

## Escopo

- Criar prompt versionado para especialista em entrega de projetos SSIS usando Spec Driven Development.
- Definir schema estruturado para saida da IA.
- Criar arquivos `*.ai.json` com enriquecimento por pacote.
- Preparar integracao futura com OpenAI Structured Outputs.
- Manter fallback deterministico quando IA estiver desabilitada.
- Garantir que o Markdown indique secoes enriquecidas por IA quando aplicavel.

## Fora de escopo

- Fine-tuning.
- Recomendacoes de Microsoft Fabric ou outra plataforma de destino.
- Reescrita do parser SSIS.
- Geracao automatica de projeto SSIS executavel.
- Validacao anti-alucinacao completa; esta ficara para fase posterior.

## Proposta de arquitetura

```text
SSIS XML
  -> parser deterministico
  -> project.json / packages/*.json
  -> SSIS SDD Specialist
  -> packages/*.ai.json
  -> Markdown SDD enriquecido
```

## Estrutura sugerida

```text
app/ai/
|-- __init__.py
|-- schemas.py
|-- sdd_enricher.py
|-- mock_enricher.py
|-- openai_enricher.py
`-- prompts/
    `-- ssis_sdd_specialist.md
```

## Schema inicial sugerido

```json
{
  "package_purpose": {
    "text": "...",
    "confidence": "low|medium|high",
    "evidence": []
  },
  "execution_summary": {
    "text": "...",
    "evidence": []
  },
  "business_rules": [
    {
      "rule": "...",
      "type": "filter|load|validation|transformation|orchestration",
      "confidence": "low|medium|high",
      "evidence": []
    }
  ],
  "reconstruction_notes": [
    {
      "note": "...",
      "evidence": []
    }
  ],
  "open_questions": [
    {
      "question": "...",
      "reason": "..."
    }
  ],
  "implementation_backlog": [
    {
      "item": "...",
      "priority": "low|medium|high",
      "source": "extracted|inferred"
    }
  ]
}
```

## Criterios de aceite

- [ ] Existe prompt versionado `ssis_sdd_specialist.md`.
- [ ] Existe schema Python para a saida esperada da IA.
- [ ] Existe interface `SddEnricher`.
- [ ] Existe `MockSddEnricher` para testes sem chamada externa.
- [ ] CLI possui parametro opt-in para enriquecimento, por exemplo `--enhance-with-ai`.
- [ ] Execucao sem IA continua funcionando sem mudancas obrigatorias.
- [ ] Quando enriquecimento estiver habilitado, arquivos `packages/*.ai.json` sao gerados.
- [ ] Markdown consegue consumir enriquecimento opcional.
- [ ] Testes automatizados cobrem schema, mock e merge no Markdown.

## Branch sugerida

```text
ai-ssis-sdd-specialist
```

## Comando para criar issue no GitHub depois da autenticacao

```powershell
gh issue create `
  --title "Implementar especialista IA para enriquecimento de SDD de projetos SSIS" `
  --body-file docs/issues/001-ai-ssis-sdd-specialist.md
```

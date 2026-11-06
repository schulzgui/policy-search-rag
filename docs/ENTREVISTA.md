# Decisões para discutir

São 12 consultas suportadas e quatro fora de escopo. Recall@3 e MRR consideram apenas as suportadas; acurácia final considera as 16, incluindo abstinências. Os métodos são comparados no mesmo conjunto. RRF usa constante 60; o gate exige score lexical de pelo menos 1,5 no documento escolhido. Esse limiar é heurístico e não representa probabilidade calibrada.

**Não há LLM, embeddings neurais ou geração de linguagem.** O nome RAG indica a arquitetura para a qual este componente de recuperação pode ser usado. As respostas são cópias de trechos do corpus.

## Demonstração

1. Consulte “comida estragada” e confira a fonte P03.
2. Consulte “xyzzy quux” e observe a abstinência.
3. Consulte “previsão de ações na bolsa” e explique o falso positivo conhecido.
4. Mostre que o híbrido empatou com o baseline.

## Limitações

- Corpus e avaliação pequenos; resultado perfeito de ranking não demonstra qualidade empresarial.
- BM25 e híbrido empataram: não há ganho demonstrado pela fusão.
- “previsão de ações na bolsa” gera fonte indevida por sobreposição em “previsão”.
- Uma citação autêntica pode ser irrelevante.
- Não há entendimento semântico robusto, detecção geral de ataques ou suporte multilíngue.
- Alterar o limiar depois de observar o teste exige novo conjunto de avaliação.

## Próximo experimento

Avaliar paráfrases independentes, adicionar recuperação neural e reranker, ampliar políticas versionadas e estudar geração com verificação de citações, custo e latência.

Explique o código com suas próprias palavras e informe o uso de assistência de IA. Este repositório não representa trabalho realizado no iFood.

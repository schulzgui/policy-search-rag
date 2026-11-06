# Data card — Policy Search RAG

**100% sintético; licença MIT.**

Seis políticas fictícias em `policies.json`: atraso, item ausente, segurança alimentar, cobrança duplicada, endereço e cancelamento. `queries.json` contém 16 perguntas e IDs esperados, ou `null` para fora de escopo. Textos e rótulos são sintéticos e criados pelo mesmo autor do laboratório; não constituem avaliação independente. Nenhuma política possui validade contratual.

Gerador: `src/policy_search/data.py`. Semente base 42, sem dados externos, scraping, nomes de clientes ou operação real.

- Corpus e avaliação pequenos; resultado perfeito de ranking não demonstra qualidade empresarial.
- BM25 e híbrido empataram: não há ganho demonstrado pela fusão.
- “previsão de ações na bolsa” gera fonte indevida por sobreposição em “previsão”.
- Uma citação autêntica pode ser irrelevante.
- Não há entendimento semântico robusto, detecção geral de ataques ou suporte multilíngue.
- Alterar o limiar depois de observar o teste exige novo conjunto de avaliação.

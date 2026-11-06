# Policy Search RAG

**Recuperação híbrida de políticas com BM25, trigramas, fusão de rankings, respostas extrativas citadas e abstinência.**

Guilherme Schulz · Portfólio técnico independente · Python 3.10+ · Licença MIT

> Todos os dados e políticas são sintéticos. Não há vínculo com o iFood, implantação empresarial ou impacto comercial medido. Projeto desenvolvido com assistência de IA; implementação, testes e limitações estão disponíveis para revisão.

## Problema e objetivo

Equipes precisam localizar uma política relevante sem receber respostas inventadas. Este projeto implementa e avalia o componente de recuperação de uma arquitetura RAG, usando seis políticas fictícias.

## O que está implementado

- Tokenização com normalização de acentos e stopwords.
- Ranking BM25 com frequência de termos e raridade no corpus.
- Canal de trigramas por similaridade de Jaccard.
- Reciprocal Rank Fusion (RRF) para combinar rankings.
- Resposta extrativa com ID da fonte e gate lexical de abstinência.
- Ablação BM25 versus híbrido e erros por consulta.

## Executar localmente

Este repositório é independente: não exige o monorepositório original nem os outros dois projetos. Não requer chave de API, serviço pago ou dependências Python de execução. Extraia o ZIP e abra um terminal na raiz de `policy-search-rag`.

macOS / Linux:

```bash
export PYTHONPATH=src
python3 -m policy_search.cli run
python3 -m unittest discover -s tests -v
python3 -m policy_search.cli serve
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m policy_search.cli run
python -m unittest discover -s tests -v
python -m policy_search.cli serve
```

Abra [a demo local](http://127.0.0.1:8002). Encerre com Ctrl+C. Para outra porta, use `serve --port 9000`. Execute na raiz do repositório; `--base CAMINHO` permite escolher outro diretório de dados/artefatos.

Opcional: `python3 -m pip install -e .` instala o comando `policy-search-rag`. Após a instalação, use `policy-search-rag run` ou `policy-search-rag serve`. A instalação requer obter o build backend se ele não estiver instalado; a execução por `PYTHONPATH` funciona sem esse passo.

## Arquitetura

```text
Políticas fictícias → BM25 + trigramas → RRF → gate de evidência → trecho literal + fonte ou abstinência
Perguntas rotuladas → Recall@3 / MRR / acurácia / abstinência → comparação entre métodos
```

`retrieval.py`: BM25, gate e avaliação; `hybrid.py`: trigramas e RRF; `data.py`: corpus e perguntas.

## Método e avaliação

São 12 consultas suportadas e quatro fora de escopo. Recall@3 e MRR consideram apenas as suportadas; acurácia final considera as 16, incluindo abstinências. Os métodos são comparados no mesmo conjunto. RRF usa constante 60; o gate exige score lexical de pelo menos 1,5 no documento escolhido. Esse limiar é heurístico e não representa probabilidade calibrada.

**Não há LLM, embeddings neurais ou geração de linguagem.** O nome RAG indica a arquitetura para a qual este componente de recuperação pode ser usado. As respostas são cópias de trechos do corpus.

Resultados observados e contagens de testes: [relatório reproduzido](docs/RESULTADOS.md). Dados detalhados: [metrics.json](artifacts/metrics.json). Procedência: [manifest.json](artifacts/manifest.json).

O manifesto registra semente, Python e hashes SHA256 de dados e implementação. Não é uma assinatura criptográfica de autoria. O comando `run` sobrescreve os dados sintéticos e artefatos gerados no diretório escolhido.

## Dados e origem

Seis políticas fictícias em `policies.json`: atraso, item ausente, segurança alimentar, cobrança duplicada, endereço e cancelamento. `queries.json` contém 16 perguntas e IDs esperados, ou `null` para fora de escopo. Textos e rótulos são sintéticos e criados pelo mesmo autor do laboratório; não constituem avaliação independente. Nenhuma política possui validade contratual.

Leia o [data card](data/README.md). Os dados são distribuídos sob MIT, junto com o código.

## API local

| Método e rota | Função |
|---|---|
| `GET /` | Formulário de demonstração |
| `GET /health` | Verificação de disponibilidade |
| `GET /api/metrics` | Resultados da última execução |
| `POST /api/search` | Executar a operação do projeto |

Com o servidor iniciado:

```bash
curl -X POST http://127.0.0.1:8002/api/search \
  -H 'Content-Type: application/json' \
  -d '{"query": "comida estragada"}'
```

A resposta é JSON. Entradas inválidas retornam HTTP 400, formato de conteúdo inadequado 415, origem incompatível 403 e rota desconhecida 404. Há limite de 8 KiB por corpo de requisição. A demo escuta apenas em `127.0.0.1`; não deve ser exposta à internet sem autenticação, TLS, servidor de produção e revisão de segurança.

## Testes e reprodução

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
PYTHONPATH=src python3 scripts/verify_reproduction.py
```

O segundo comando compara dados gerados byte a byte e métricas/modelos JSON com tolerância numérica de `1e-10`, para acomodar arredondamento entre versões Python. A versão Python no manifesto pode variar. Os testes de integração iniciam a API em porta temporária e usam diretórios descartáveis. A CI está configurada para Python 3.10, 3.12 e 3.13; apenas os testes locais efetivamente executados são declarados no relatório.

## Estrutura

```text
src/policy_search/      algoritmos, gerador, CLI e servidor
scripts/                 verificação dos artefatos versionados
tests/                   testes de domínio e integração HTTP
data/                    dados sintéticos e data card
artifacts/               métricas e manifesto de procedência
docs/                    resultados e roteiro técnico
.github/workflows/       CI por versão Python
```

## Demonstração para entrevista

1. Consulte “comida estragada” e confira a fonte P03.
2. Consulte “xyzzy quux” e observe a abstinência.
3. Consulte “previsão de ações na bolsa” e explique o falso positivo conhecido.
4. Mostre que o híbrido empatou com o baseline.

Leia [o guia técnico](docs/ENTREVISTA.md) e reproduza o experimento antes de apresentá-lo. Declare claramente a contribuição da assistência de IA e as modificações que você revisou ou realizou.

## Limitações e decisões

- Corpus e avaliação pequenos; resultado perfeito de ranking não demonstra qualidade empresarial.
- BM25 e híbrido empataram: não há ganho demonstrado pela fusão.
- “previsão de ações na bolsa” gera fonte indevida por sobreposição em “previsão”.
- Uma citação autêntica pode ser irrelevante.
- Não há entendimento semântico robusto, detecção geral de ataques ou suporte multilíngue.
- Alterar o limiar depois de observar o teste exige novo conjunto de avaliação.

A inspeção visual da demo ainda não foi concluída; os endpoints são cobertos por testes HTTP. Nenhum resultado deste laboratório comprova experiência profissional no iFood.

## Próximos experimentos — ainda não implementados

Avaliar paráfrases independentes, adicionar recuperação neural e reranker, ampliar políticas versionadas e estudar geração com verificação de citações, custo e latência.

## Publicar como repositório separado

Crie um repositório vazio chamado `policy-search-rag` na sua conta. Envie **o conteúdo da raiz deste projeto**, incluindo arquivos ocultos, sem a pasta externa e sem o ZIP. Alternativamente:

```bash
git init -b main
git add .
git commit -m "Add standalone reproducible project"
git remote add origin https://github.com/SEU_USUARIO/policy-search-rag.git
git push -u origin main
```

Substitua `SEU_USUARIO` pelo seu login. Autenticação Git precisa estar configurada. Confirme a execução da aba Actions após o envio. Esses comandos não foram executados contra um novo repositório remoto nesta reorganização.

## Licença e contribuição

[MIT](LICENSE). Para propor alterações: descreva o problema, preserve a identificação sintética, execute os testes e regenere artefatos quando modificar dados ou algoritmos. Não atualize métricas manualmente para fazê-las parecer melhores.

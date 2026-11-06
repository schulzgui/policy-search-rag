"""BM25 + similaridade de trigramas via reciprocal rank fusion (RRF)."""
from .retrieval import Search,tokens

def grams(text):
 text=" ".join(tokens(text));return {text[i:i+3] for i in range(max(0,len(text)-2))}

class HybridSearch(Search):
 def rank(self,query):
  lexical=super().rank(query);q=grams(query)
  fuzzy=[]
  for d in self.docs:
   g=grams(d["title"]+" "+d["text"]);fuzzy.append((len(q & g)/max(1,len(q | g)),d))
  fuzzy.sort(key=lambda x:(-x[0],x[1]["id"]))
  scores={d["id"]:0 for d in self.docs}
  for ranking in [lexical,fuzzy]:
   for rank,(score,d) in enumerate(ranking,1):
    if score>0:scores[d["id"]]+=1/(60+rank)
  return sorted([(scores[d["id"]],d) for d in self.docs],key=lambda x:(-x[0],x[1]["id"]))
 def answer(self,query):
  score,doc=self.rank(query)[0]
  # Gate de evidência lexical; RRF não é probabilidade de confiança.
  lexical=dict((d["id"],s) for s,d in super().rank(query))
  if lexical[doc["id"]]<1.5:
   return {"status":"abstain","answer":"Evidência insuficiente; revisão humana necessária.","source":None,"score":score}
  return {"status":"found","answer":doc["text"],"source":doc["id"],"score":score}

"""BM25 com resposta extrativa citada; não utiliza nem simula um LLM."""
import math
import re
import unicodedata
from collections import Counter

STOP={"a","o","e","de","da","do","na","no","um","uma","meu","minha","com","para","quero","qual","foi","esta","as","os","em"}
def tokens(text):
 text=unicodedata.normalize("NFKD",text.lower()).encode("ascii","ignore").decode()
 return [t for t in re.findall(r"[a-z0-9]+",text) if t not in STOP]

class Search:
 def __init__(self,docs):
  self.docs=docs;self.counts=[Counter(tokens(d["title"]+" "+d["text"])) for d in docs]
  self.avg=sum(sum(c.values()) for c in self.counts)/len(docs)
 def rank(self,query):
  terms=set(tokens(query));scores=[]
  for doc,c in zip(self.docs,self.counts):
   score=0
   for t in terms:
    df=sum(t in other for other in self.counts);tf=c[t]
    idf=math.log(1+(len(self.docs)-df+.5)/(df+.5))
    score+=idf*(tf*2.5)/(tf+1.5*(.25+.75*sum(c.values())/self.avg)) if tf else 0
   scores.append((score,doc))
  return sorted(scores,key=lambda pair:(-pair[0],pair[1]["id"]))
 def answer(self,query):
  ranked=self.rank(query);score,doc=ranked[0]
  # Um termo genérico compartilhado pode gerar falso positivo; documentado na avaliação.
  if score<1.5:return {"status":"abstain","answer":"Não encontrei evidência suficiente. Encaminhar para atendimento humano.","source":None,"score":score}
  return {"status":"found","answer":doc["text"],"source":doc["id"],"score":score}

def evaluate(search,queries):
 supported=[q for q in queries if q["expected_id"]];unsupported=[q for q in queries if not q["expected_id"]]
 hits=0;rr=0;details=[]
 for q in supported:
  ids=[d["id"] for _,d in search.rank(q["query"])]; rank=ids.index(q["expected_id"])+1
  hits+=rank<=3;rr+=1/rank
 for q in queries:
  answer=search.answer(q["query"])
  details.append({**q,**answer,"correct":answer["source"]==q["expected_id"]})
 return {"supported_n":len(supported),"unsupported_n":len(unsupported),"recall_at_3":hits/len(supported),"mrr":rr/len(supported),
 "answer_accuracy":sum(d["correct"] for d in details)/len(details),
 "unsupported_abstention_rate":sum(search.answer(q["query"])["status"]=="abstain" for q in unsupported)/len(unsupported),"details":details}

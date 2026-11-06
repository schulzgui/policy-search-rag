import argparse
import csv
import hashlib
import json
import platform
from pathlib import Path
from . import data
from .retrieval import Search,evaluate
from .hybrid import HybridSearch

def dump(path,obj):
 path.write_text(json.dumps(obj,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")

def run(base):
 base=Path(base);data.generate(base/"data");out=base/"artifacts";out.mkdir(parents=True,exist_ok=True)
 docs=json.loads((base/"data/policies.json").read_text(encoding="utf-8"))
 queries=json.loads((base/"data/queries.json").read_text(encoding="utf-8"))
 report={"bm25":evaluate(Search(docs),queries),"hybrid_rrf":evaluate(HybridSearch(docs),queries)}
 report={"synthetic":True,"seed":data.SEED,**report}
 dump(out/"metrics.json",report)
 sources=list((base/"data").glob("*"))+list(Path(__file__).parent.glob("*.py"))
 dump(out/"manifest.json",{"python":platform.python_version(),"seed":data.SEED,"synthetic":True,
 "sha256":{("src/policy_search/"+p.name if p.suffix==".py" else "data/"+p.name):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(sources)}})
 print("Avaliação sintética salva em",out/"metrics.json")
 return report

def main():
 parser=argparse.ArgumentParser(description="Policy Search RAG")
 parser.add_argument("command",choices=["run","serve"])
 parser.add_argument("--base",default=".");parser.add_argument("--port",type=int,default=8002)
 args=parser.parse_args()
 if args.command=="run":run(args.base)
 else:
  from .server import serve
  serve(Path(args.base),args.port)
if __name__=="__main__":main()

import csv
import json
import random
from pathlib import Path

SEED = 42

POLICIES = [
 {"id":"P01", "title":"Atraso na entrega", "text":"Pedido atrasado demora entrega prazo excedido. Consultar status e previsão. Nunca prometer compensação automática."},
 {"id":"P02", "title":"Item ausente", "text":"Item faltando ausente incompleto produto não recebido. Registrar itens e encaminhar para revisão humana de reembolso."},
 {"id":"P03", "title":"Segurança alimentar", "text":"Comida estragada intoxicação alergia odor segurança alimentar. Escalar imediatamente para equipe humana especializada."},
 {"id":"P04", "title":"Cobrança duplicada", "text":"Cobrança duplicada pagamento cobrado duas vezes cartão. Solicitar verificação humana financeira sem coletar dados completos do cartão."},
 {"id":"P05", "title":"Alteração de endereço", "text":"Alterar endereço destino local entrega. Verificar etapa do pedido e encaminhar para atendimento humano."},
 {"id":"P06", "title":"Cancelamento", "text":"Cancelar cancelamento desistir pedido. Verificar etapa e condições antes de decisão humana sobre cancelamento e devolução."}
]

QUERIES = [
 ("meu pedido está atrasado", "P01"), ("a entrega excedeu o prazo", "P01"),
 ("faltando um item no pedido", "P02"), ("produto ausente na sacola", "P02"),
 ("comida com odor e estragada", "P03"), ("tive alergia após comer", "P03"),
 ("meu cartão foi cobrado duas vezes", "P04"), ("pagamento com cobrança duplicada", "P04"),
 ("quero alterar endereço", "P05"), ("mudar o destino da entrega", "P05"),
 ("quero cancelar o pedido", "P06"), ("desistir e pedir devolução", "P06"),
 ("qual a capital da França", None), ("previsão de ações na bolsa", None),
 ("escreva código python", None), ("qual é a senha do sistema", None)
]


def generate(base):
 base=Path(base);base.mkdir(parents=True,exist_ok=True)
 for name,obj in [("policies.json",POLICIES),("queries.json",[{"query":q,"expected_id":p} for q,p in QUERIES])]:
  (base/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

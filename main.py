import xmltodict
import dass
from time import time
import json

COUNT = 100 # количество вызовов функции
FILENAME = 'input/smartphone.xml'
out = {}

# -+-+-+-+-+- Экспортированные варианты
with open(FILENAME, encoding='utf-16-le') as xml_file:
  decision = xmltodict.parse(xml_file.read())['decision']

criterions = [dass.Criterion(c) for c in decision['criterionList']['criterion']]
scale = dass.Scale(decision['scale'])
importance = dass.Importance(decision['importance'])
variants = [dass.Variant(v) for v in decision['variantList']['variant']]

out['criterions'] = [c.toJSON() for c in criterions]
out['scale'] = scale.toJSON()
out['importance'] = importance.toJSON()
out['variants'] = [v.toJSON() for v in variants]

print('--- Экспортированные варианты:', variants)
dass.reset_domination(variants)
dominated_variants = []

out['1_reset'] = {}
out['1_reset']['variants'] = [v.toJSON() for v in variants]
out['1_reset']['variants'] = [v.toJSON() for v in dominated_variants]

# -+-+-+-+-+- Принцип Парето (СТРАНИЦА 13)
t = dass.timing(COUNT, dass.pareto, variants)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Принцип Парето:', variants, '\n', dominated_variants)

out['2_pareto'] = {}
out['2_pareto']['variants'] = [v.toJSON() for v in variants]
out['2_pareto']['variants'] = [v.toJSON() for v in dominated_variants]

# -+-+-+-+-+- Качественная важность (СТРАНИЦА 34)
t = dass.timing(COUNT, dass.quality_domination, variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Качественная важность:', variants, '\n', dominated_variants)

out['3_quality'] = {}
out['3_quality']['variants'] = [v.toJSON() for v in variants]
out['3_quality']['variants'] = [v.toJSON() for v in dominated_variants]

# -+-+-+-+-+- Количественная важность (СТРАНИЦА 53)
t = dass.timing(COUNT, dass.count_domination, variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Количественная важность:', variants, '\n', dominated_variants)

out['4_count'] = {}
out['4_count']['variants'] = [v.toJSON() for v in variants]
out['4_count']['variants'] = [v.toJSON() for v in dominated_variants]

with open('out.json', 'w', encoding='utf-8') as fout:
  json.dump(out, fout, indent=2, ensure_ascii=False)
import xmltodict
import dass
from time import time

COUNT = 10000 # количество вызовов функции
FILENAME = 'input/smartphone.xml'

# -+-+-+-+-+- Экспортированные варианты
with open(FILENAME, encoding='utf-16-le') as xml_file:
  decision = xmltodict.parse(xml_file.read())['decision']

criterions = [dass.Criterion(c) for c in decision['criterionList']['criterion']]
scale = dass.Scale(decision['scale'])
importance = dass.Importance(decision['importance'])
variants = [dass.Variant(v) for v in decision['variantList']['variant']]

print('--- Экспортированные варианты:', variants)
dass.reset_domination(variants)
dominated_variants = []

# -+-+-+-+-+- Принцип Парето (СТРАНИЦА 13)
t = dass.timing(COUNT, dass.pareto, variants)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Принцип Парето:', variants, '\n', dominated_variants)

# -+-+-+-+-+- Качественная важность (СТРАНИЦА 34)
t = dass.timing(COUNT, dass.quality_domination, variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Качественная важность:', variants, '\n', dominated_variants)

# -+-+-+-+-+- Количественная важность (СТРАНИЦА 53)
t = dass.timing(COUNT, dass.count_domination, variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- ', t, ' Количественная важность:', variants, '\n', dominated_variants)

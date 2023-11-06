import xmltodict
import dass

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
dass.pareto(variants)
dass.move_dominated(variants, dominated_variants)
print('\n--- Принцип Парето:', variants, '\n', dominated_variants)

# -+-+-+-+-+- Качественная важность (СТРАНИЦА 34)
dass.quality_domination(variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- Качественная важность:', variants, '\n', dominated_variants)

# -+-+-+-+-+- Количественная важность (СТРАНИЦА 53)
dass.count_domination(variants, importance, scale)
dass.move_dominated(variants, dominated_variants)
print('\n--- Количественная важность:', variants, '\n', dominated_variants)

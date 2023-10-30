import xmltodict
import dass

# -+-+-+-+-+- Чтение данных из файла
with open('smartphone.xml', encoding='utf-8') as xml_file:
  decision = xmltodict.parse(xml_file.read())['decision']

criterions = [dass.Criterion(c) for c in decision['criterionList']['criterion']]
scale = dass.Scale(decision['scale'])
importance = dass.Importance(decision['importance'])
variants = [dass.Variant(v) for v in decision['variantList']['variant']]

print('--- Критерии')
for c in criterions:
  print(c, end=', ')
print('\nШкала')
print(scale)
print('Важность')
print(importance)
print('--- Варианты:')
for v in variants:
  print(v)

print('\n\n\n')
for v in variants:
  print(v)

# -+-+-+-+-+- Принцип Парето
# информация о важности не используется
dass.reset_domination(variants)
dass.pareto(variants)
print('\n\n\n')
for v in variants:
  print(v)


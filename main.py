import xmltodict
import dass

FILENAME = 'smartphone2.xml'

# -+-+-+-+-+- Чтение данных из файла
with open(FILENAME, encoding='utf-16-le') as xml_file:
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
print('--- DASS:')
for v in variants:
  print(v)

# информация о важности не используется
dass.reset_domination(variants)

# -+-+-+-+-+- Качественная информация о важности
print('--- Свой алгоритм:')
dass.quality_domination(variants, importance, scale)
for v in variants:
  print(v)

# -+-+-+-+-+- Количественная важность
dass.count_domination(variants, importance, scale)

print('\n--- Количественная важность')
for v in variants:
  print(v)

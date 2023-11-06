import xmltodict
import dass

# Страница 36 пособия
FILENAME = 'student2.xml'

# -+-+-+-+-+- Чтение данных из файла
with open(FILENAME, encoding='utf-16-le') as xml_file:
  decision = xmltodict.parse(xml_file.read())['decision']

criterions = [dass.Criterion(c) for c in decision['criterionList']['criterion']]
scale = dass.Scale(decision['scale'])
importance = dass.Importance(decision['importance'])
variants = [dass.Variant(v) for v in decision['variantList']['variant']]

print('--- Варианты:')
for v in variants:
  print(v)

# -+-+-+-+-+- Принцип Парето
dass.reset_domination(variants)
dass.pareto(variants)
print('\n--- Принцип Парето:')
for v in variants:
  print(v)

# -+-+-+-+-+- Качественная информация о важности
del variants[5] # исключаем варианты 5 и 6
del variants[4]
dass.quality_domination(variants, importance, scale)

print('\n--- Качественная важность')
for v in variants:
  print(v)


# -+-+-+-+-+- Количественная важность
del variants[3] # исключаем вариант 4 как доминируемый
dass.count_domination(variants, importance, scale)

print('\n--- Количественная важность')
for v in variants:
  print(v)


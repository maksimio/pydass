import xmltodict
import dass

# -+-+-+-+-+- Чтение данных из 
e1 = 'utf-8'
f1 = 'smartphone.xml'
e2 = 'utf-16-le'
f2 = 'student.xml'
with open(f2, encoding=e2) as xml_file:
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
print('\n')
for v in variants:
  print(v)

# -+-+-+-+-+- Временно исключим 5 и 6
del variants[4]
del variants[5]

print('\n')
for v in variants:
  print(v)

# -+-+-+-+-+- Сравнение вариантов по предпочтительности
dass.quality_domination(variants, importance, scale)
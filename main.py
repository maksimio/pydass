import xmltodict
import dass

FILENAME = 'student.xml'

# -+-+-+-+-+- Чтение данных из 
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
print('--- Варианты:')
for v in variants:
  print(v)

# -+-+-+-+-+- Принцип Парето
# информация о важности не используется
dass.reset_domination(variants)
# dass.pareto(variants)
# print('\n--- Принцип Парето:')
# for v in variants:
#   print(v)

# -+-+-+-+-+- Временно исключим 5 и 6
# del variants[5]
# del variants[4]

print('\n')
for v in variants:
  print(v)

# -+-+-+-+-+- Сравнение вариантов по предпочтительности
dass.quality_domination(variants, importance, scale)


print('\n')
for v in variants:
  print(v)
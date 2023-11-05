import xmltodict
import dass

FILENAME = 'student.xml'

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

# -+-+-+-+-+- Сравнение вариантов по предпочтительности
dass.quality_domination(variants, importance, scale)

print('--- Свой алгоритм:')
for v in variants:
  print(v)
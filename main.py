import xmltodict

with open('smartphone.xml', encoding='utf-8') as xml_file:
  data = xmltodict.parse(xml_file.read())

decision = data['decision']

problem = decision['problem']
criterionList = decision['criterionList']
importance = decision['importance']
scale = decision['scale']
variantList = decision['variantList']

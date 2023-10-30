from dataclasses import dataclass, field

# ------------------------ ТИПЫ ДАННЫХ
class Variant:
  def __init__(self, v):
    # print(v)
    self.name = v['@vname']
    self.nodominated = v['@nondominated'] == 'yes'
    self.scores = list(map(int, v['scores']['sc']))
    self.linkedTo = v['linkedTo']
  
  def __str__(self):
    return 'вариант: {0: >7}, недоминируемый: {1: 1}, доминирующий: {2: >7}, оценки: {3}'.format(self.name, self.nodominated, self.linkedTo, self.scores)


class Scale:
  def __init__(self, s):
    self.gradeCount = s['gradeCount']
    # рассматривается только порядковая шкала
  
  def __str__(self):
    return str(self.gradeCount)


class Criterion:
  def __init__(self, c):
    self.name = c['@cname']
    
  def __str__(self):
    return self.name


class Importance:
  def __init__(self, i):
    self.active = i['@active'] 
    # пока только для порядковой важности
    self.positions = list(map(int, i['order']['positions']['pos']))
    self.importances =  [ri == 'less' for ri in i['order']['relativeImportance']['ri']]

  def __str__(self):
    return '{0}\n{1}'.format(self.positions, self.importances)

# ------------------------ ОБРАБОТКА
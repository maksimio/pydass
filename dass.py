from dataclasses import dataclass, field
import numpy as np

# ------------------------ ТИПЫ ДАННЫХ
class Variant:
  def __init__(self, v):
    self.name = v['@vname']
    self.nodominated = v['@nondominated'] == 'yes'
    self.scores = list(map(int, v['scores']['sc']))
    self.linkedTo = v['linkedTo']

    self.matrix = [] # TODO: убрать
  
  def __str__(self):
    return 'вариант: {0: >7}, недоминируемый: {1: 1}, доминирующий: {2: >7}, оценки: {3}'.format(self.name, self.nodominated, self.linkedTo, self.scores)


class Scale:
  def __init__(self, s):
    self.gradeCount = int(s['gradeCount'])
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
def reset_domination(variants: list[Variant]):
  for v in variants:
    v.nodominated = True
    v.linkedTo = v.name


def pareto(variants: list[Variant]):
  for a in variants:
    for b in variants:
      if a.name == b.name:
        continue

      s = 0
      check_not_equal = False
      for i in range(len(b.scores)):
        if a.scores[i] >= b.scores[i]:
          s += 1
        if a.scores[i] > b.scores[i]:
          check_not_equal = True
      
      if (s == len(b.scores)) and check_not_equal:
        b.linkedTo = a.name
        b.nodominated = False


def quality_domination_matrix(scores: list[int], importance_vector: list[int], k_min: int, k_max: int):
  matrix = []
  for k in range(k_min, k_max + 1, 1):
    values = [vector if score <= k else 0 for score, vector in zip(scores, importance_vector)]
    values.sort()
    matrix.append(values)
  return np.array(matrix)

def quality_domination(variants: list[Variant], importance: Importance, scale: Scale):
  # 1. Указываем k
  k_max = scale.gradeCount - 1
  # 2. Даем оценку признакам в соответствии с важностью
  d = 0
  importances = importance.importances.copy()
  importances.reverse()

  importance_vector = []
  k = 1
  for imp in importances:
    importance_vector.append(k)
    if imp:
      k += 1
  importance_vector.reverse()

  print(importance.importances)
  print(importance.positions)
  print(importance_vector)
  print('-----------------------')
  # 3. Вычисляем матрицы B↑
  for v in variants:
    v.matrix = quality_domination_matrix(v.scores, importance_vector, 3, k_max)
  
  # 3. Попарное сравнение векторов оценок
  for v1 in variants:
    for v2 in variants:
      if v1 == v2:
        continue # Вектора оценок не сравниваются между собой
      res = v2.matrix - v1.matrix
      if np.any(res < 0) or (not np.any(res > 0)):
        continue
      
      print('hello wewe', v1.name, v2.name)


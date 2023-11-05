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
      if a == b:
        continue # Вектора оценок не сравниваются между собой

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


def quality_domination_matrix(scores: list[int], importance_vector: list[int], q: int):
  matrix = []
  for k in range(1, q, 1): # k от 1 до q - 1 включительно (ФОРМУЛА 2.2)
    values = [v if y <= k else 0 for y, v in zip(scores, importance_vector)]
    values.sort()
    matrix.append(values)
  
  return np.array(matrix)

def quality_domination(variants: list[Variant], importance: Importance, scale: Scale):
  q = scale.gradeCount # ФОРМУЛА 2.2

  # Вычисляем вектор важности критериев 
  importances = importance.importances.copy()
  importances.reverse()
  importance_vector, k = [], 1
  for imp in importances: # ФОРМУЛА 2.6
    importance_vector.append(k)
    if imp:
      k += 1
  importance_vector.reverse() # ФОРМУЛА 2.4

  # Вычисляем матрицы B↑
  importance_vector_new = list(np.empty(len(importance_vector)))
  for pos, value in zip(importance.positions, importance_vector):
    importance_vector_new[pos] = value

  for v in variants:
    v.matrix = quality_domination_matrix(v.scores, importance_vector_new, q)
  
  # Попарное сравнение векторов оценок (ФОРМУЛА 2.7)
  for v1 in variants:
    for v2 in variants:
      if v1 == v2:
        continue # Вектора оценок не сравниваются между собой
      res = v1.matrix - v2.matrix
      if np.any(res < 0) or (not np.any(res > 0)):
        continue
      print(v2.name, 'лучше, чем', v1.name)
      v1.linkedTo = v2.name
      v1.nodominated = False
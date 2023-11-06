from dataclasses import dataclass, field
import numpy as np

# ------------------------ ТИПЫ ДАННЫХ
class Variant:
  def __init__(self, v):
    self.name = v['@vname']
    self.nodominated = v['@nondominated'] == 'yes'
    self.scores = list(map(int, v['scores']['sc']))
    self.linkedTo = v['linkedTo']

    self.matrix = []
    self.long_scores = []
  
  def __str__(self):
    return 'вариант: {0: >7}, недоминируемый: {1: 1}, доминирующий: {2: >7}, оценки: {3}'.format(self.name, self.nodominated, self.linkedTo, self.scores)

  def __repr__(self):
    return '\nвариант: {0: >7}, недоминируемый: {1: 1}, доминирующий: {2: >7}, оценки: {3}'.format(self.name, self.nodominated, self.linkedTo, self.scores)
 

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
    self.importance_coefs = list(map(float, i['importanceCoefs']['ic']))

  def __str__(self):
    return '{0}\n{1}\n{2}'.format(self.positions, self.importances, self.importance_coefs)

# ------------------------ ОБРАБОТКА
def reset_domination(variants: list[Variant]):
  '''Сброс информации о доминации. Используется после чтения файла DASS'''
  for v in variants:
    v.nodominated = True
    v.linkedTo = v.name


def move_dominated(non_dominated: list[Variant], dominated: list[Variant]):
  '''Перемещение доминируемых вариантов в отдельный список для удобства работы'''
  for obj in non_dominated.copy():
    if not obj.nodominated:
      dominated.append(obj)
      non_dominated.remove(obj)


def pareto(variants: list[Variant]):
  '''Принцип Парето. Используется для сравнения вариантов 
  без информации о важности критериев'''
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
  '''Матрица B↑ для поиска качественной важности'''
  matrix = []
  for k in range(1, q, 1): # k от 1 до q - 1 включительно (ФОРМУЛА 2.2)
    values = [v if y <= k else 0 for y, v in zip(scores, importance_vector)]
    values.sort()
    matrix.append(values)
  
  return np.array(matrix)


def quality_domination(variants: list[Variant], importance: Importance, scale: Scale):
  '''Качественная важность'''
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
      v1.linkedTo = v2.name
      v1.nodominated = False


def count_domination(variants: list[Variant], importance: Importance, scale: Scale):
  '''Количественная важность'''
  # Вычисление N-модели
  # Чтобы не искать наименьший общий множитель до целого
  # просто умножим на 1e3, округлим до целого. 
  # Считаем, что такой точности достаточно
  mult = 1e9
  n_model = [1]
  coefs = importance.importance_coefs.copy()
  coefs.reverse()
  for i in range(len(coefs)):
    n_model.append(coefs[i] * n_model[i])
  
  n_model.reverse()
  n_model = np.array(n_model) * mult
  n_model = np.array(list(map(int, n_model)))
  
  # Оптимизация N-модели через поиск наибольшего общего делителя
  gdc = np.gcd.reduce(n_model)
  n_model = list(map(int, n_model / gdc))

  # Применение N-модели к вариантам (получение удлиненных оценок)
  n_model_len = 0
  for n in n_model:
    n_model_len += n

  for v in variants:
    v.long_scores = []
    for n, s in zip(n_model, v.scores):
      for i in range(n):
        v.long_scores.append(s)
      
    v.long_scores.sort(reverse=True) # По невозрастанию

  # Применение метода Парето к удлиненным оценкам long_scores
  for a in variants:
    for b in variants:
      if a == b:
        continue # Вектора оценок не сравниваются между собой

      s = 0
      check_not_equal = False
      for i in range(len(b.long_scores)):
        if a.long_scores[i] >= b.long_scores[i]:
          s += 1
        if a.long_scores[i] > b.long_scores[i]:
          check_not_equal = True
      
      if (s == len(b.long_scores)) and check_not_equal:
        b.linkedTo = a.name
        b.nodominated = False
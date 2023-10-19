import numpy as np

class NaiveEngine:
    def __init__(self):
        pass

    def calculate(eslf, array):
        value_sum = 0
        for value in array:
            value_sum += value
        return value_sum / len(array)

class SumEngine:
    def __init__(self):
        pass

    def calculate(eslf, array):
        return sum(array) / len(array)

class NumpyEngine:
    def __init__(self):
        pass

    def calculate(eslf, array):
        return array.mean()

backbone_dict = {
    "naive": NaiveEngine,
    "sum": SumEngine,
    "np.mean": NumpyEngine, 
}

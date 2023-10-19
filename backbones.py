import time
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

    def calculate(self, array):
        return array.mean()

class SlowEngine(NumpyEngine):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sleep_time = 2

    def calculate(self, array):
        time.sleep(self.sleep_time)
        return super().calculate(array)

backbone_dict = {
    "naive": NaiveEngine,
    "sum": SumEngine,
    "np.mean": NumpyEngine, 
    "slow": SlowEngine,
}

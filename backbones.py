import time
import numpy as np

class TwoMuchTokensError(Exception):
    pass

class NotHyphenatedOptionError(Exception):
    pass

def parse_options(options_str, engine_cls):
    flags, unrecognized_flags = [], []
    parameters, unrecognized_parameters = {}, {}
    options = options_str.split('-')
    if options[0]: # Options should start with '-'
        raise NotHyphenatedOptionError()
    for option in options[1:]:
        tokens = option.split()
        if not tokens:
            continue
        elif len(tokens) == 1:
            flag = tokens[0]
            if flag in engine_cls.supported_flags:
               flags.append(flag)
            else:
                unrecognized_flags.append(flag)
        elif len(tokens) == 2:
            parameter_name = tokens[0]
            parameter_value = int(tokens[1])
            if parameter_name in engine_cls.default_parameters:
                parameters[parameter_name] = parameter_value
            else:
                unrecognized_parameters[parameter_name] = parameter_value
        else:
            raise TwoMuchTokensError()
    return (flags, parameters,
        unrecognized_flags, unrecognized_parameters)

class OptionsEngine:
    supported_flags = ["abs", "error", "squared"]
    default_parameters = {}

    def __init__(self, flags=None, parameters=None):
        self.flags = flags if flags else []
        self.parameters = self.default_parameters.copy()
        if parameters is not None:
            self.parameters.update(parameters)

    def input_transform(self, array):
        if 'error' in self.flags:
            array = array - array.mean()
        if 'abs' in self.flags:
            array = np.abs(array)
        if 'squared' in self.flags:
            array = array ** 2
        return array

class NaiveEngine(OptionsEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate(self, array):
        array = self.input_transform(array)
        value_sum = 0
        for value in array:
            value_sum += value
        return value_sum / len(array)

class SumEngine(OptionsEngine):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate(self, array):
        array = self.input_transform(array)
        return sum(array) / len(array)

class NumpyEngine(OptionsEngine):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate(self, array):
        array = self.input_transform(array)
        return array.mean()

class SlowEngine(NumpyEngine):
    default_parameters = dict(sleep=2) | NumpyEngine.default_parameters

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def calculate(self, array):
        time.sleep(self.parameters["sleep"])
        return super().calculate(array)

backbone_dict = {
    "naive": NaiveEngine,
    "sum": SumEngine,
    "np.mean": NumpyEngine, 
    "slow": SlowEngine,
}

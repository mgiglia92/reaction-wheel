from ruamel.yaml import YAML
yaml = YAML()

class ParameterConverter:
    def __init__(self, filename):
        try:
            file = open(filename, 'r')
            data = yaml.load(file)
        except Exception as e:
            print(e)

    def parametersMessage(self):
        pass

    def confirmationMessage(self):
        pass

class ControllerConfig:
    def __init__(self, d):
        ts = d['dt']
        sigma = d['sigma']
        gains = d['gains']
        limits = d['lowerLimit']
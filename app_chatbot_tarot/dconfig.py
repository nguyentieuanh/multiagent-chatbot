# declaring a class
import json
import yaml


class ConfigObj:
    # constructor
    def __init__(self, dict1):
        self.__dict__.update(dict1)


def dict2obj(dict1):
    # using json.loads method and passing json.dumps
    # method and custom object hook as arguments
    return json.loads(json.dumps(dict1), object_hook=ConfigObj)


def yaml2obj(yaml_path):
    with open(yaml_path) as f:
        data_load = yaml.safe_load(f)

    config_obj = dict2obj(data_load)

    return config_obj


def yaml2dict(yaml_path):
    with open(yaml_path) as f:
        data_load = yaml.safe_load(f)
    return data_load


config_object = yaml2obj("path_config/prompt.yml")
config_key = yaml2obj("path_config/key.yml")

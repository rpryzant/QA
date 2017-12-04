import yaml
import random
from collections import namedtuple, OrderedDict

""" https://stackoverflow.com/questions/5121931 """
#    (get YAML to preserve ordering)
_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return OrderedDict(loader.construct_pairs(node))

yaml.add_representer(OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)
####################################################


def write_config(config, path):
    yaml_str = yaml.dump(config._asdict(), default_flow_style=False)
    with open(path, 'w') as f:
        f.write(yaml_str)


def load_yaml(filepath, name='config'):
    d = yaml.load(open(filepath).read())
    return namedtuple(name, d.keys())(**d)


def get_experiment_configs(yaml_path):

    base_config = load_yaml(yaml_path)
    random.seed(base_config.random_seed)

    out = []
    for i in range(base_config.num_experiments):
        d = OrderedDict()
        for k in base_config._fields:
            v = getattr(base_config, k)
            if isinstance(v, list):
                d[k] = random.choice(v)
            elif isinstance(v, tuple):
                d[k] = random.uniform(*v)
            else:
                d[k] = v
        d['working_dir'] = '%s_%d' % (d['working_dir_base'], i)
        out.append(namedtuple('config_%d' % i, d.keys())(**d))

    return out

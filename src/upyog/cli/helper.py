import argparse

from upyog.util.array import sequencify
from upyog.util.eject import ejectable
from upyog.config     import load_config

@ejectable(imports = ["argparse"], deps = ["load_config"])
class ConfigFileAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string = None):
        config = load_config(values)
        setattr(namespace, self.dest, config)

@ejectable(imports = ["argparse"], deps = ["sequencify"])
class ParamAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string = None):
        params = getattr(namespace, self.dest)

        if not params:
            params = dict()

        if values:
            values = sequencify(values)

            for value in values:
                if "=" in value:
                    key, value = value.split("=")
                    params[key] = value

        setattr(namespace, self.dest, params)
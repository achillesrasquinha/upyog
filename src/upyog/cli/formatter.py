from upyog.util.eject import ejectable

# imports - standard imports
import argparse

@ejectable(imports = ["argparse"])
class ArgumentParserFormatter(
    argparse.RawDescriptionHelpFormatter,
    argparse.ArgumentDefaultsHelpFormatter
):
    pass
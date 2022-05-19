import os, os.path as osp
import ast

from bpyutils.util.system import (
    get_basename,
    read,
    write,
    makepath
)
from bpyutils.log import get_logger
from bpyutils.util.string import nl, tb, strip
from bpyutils.parallel import no_daemon_pool
from bpyutils.util.types import lmap

logger  = get_logger()

_INDENT = 1

class TestGenerator(ast.NodeVisitor):
    def __init__(self, *args, **kwargs):
        self.lines = [
            nl("import pytest"),
            nl()
        ]

    @property
    def code(self):
        return "".join(self.lines)
        
    def visit_ClassDef(self, node):
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.lines.extend([
            nl("def test_%s():" % node.name),
            nl(tb("raise NotImplementedError", point = _INDENT, type_ = "\t")),
            nl()
        ])

        self.generic_visit(node)

def generate_tests(path, target_dir = None, check = False):
    path = osp.abspath(path)
    package_name = get_basename(path)
    package_path = osp.join(path, "src", package_name)

    if not osp.exists(package_path):
        raise FileNotFoundError("Path %s not found." % package_path)

    if target_dir:
        target_dir = osp.abspath(target_dir)
    else:
        target_dir = osp.join(path, "tests", package_name)
        logger.info("Using target directory %s" % target_dir)

    for root, dirs, files in os.walk(package_path):
        for file_ in files:
            filepath = osp.join(root, file_)

            if osp.exists(filepath):
                filename, extension = osp.splitext(file_)
            
                if extension == ".py":
                    content = read(filepath)

                    ast_tree = ast.parse(content)
                    test_generator = TestGenerator()
                    test_generator.visit(ast_tree)
                    test_code = test_generator.code

                    dir_prefix = root.replace(package_path, "")
                    dir_prefix = strip(dir_prefix, type_ = "/")

                    if "__init__" in file_:
                        file_ = "%s%s" % (dir_prefix, file_)

                    target_path = osp.join(target_dir, dir_prefix, "test_%s" % file_)
                    logger.info("Generating tests for %s..." % filepath)
                    logger.info("Writing tests to %s..." % target_path)

                    if osp.exists(target_path):
                        pass
                    else:
                        if not check:
                            write(target_path, test_code, force = True)
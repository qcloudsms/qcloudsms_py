#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pdoc
import sys


PROJECT_PATH = "."
DOCS_PATH = "./docs/"
PACKAGE_NAME = "qcloudsms_py"


def gen_module_doc(module, path):
    text = module.html(external_links=True)
    with open(path + "index.html", "w") as f:
        f.write(text.encode("utf-8"))
    # submodules
    for submodule in module.submodules():
        name = submodule.name[submodule.name.rindex(".") + 1: ]
        if submodule.is_package():
            path += "{}/".format(name)
            gen_module_doc(path, submodule)
        else:
            text = submodule.html(external_links=True)
            with open(path + name + ".m.html", "w") as f:
                f.write(text.encode("utf-8"))


if __name__ == "__main__":
    sys.path.append(PROJECT_PATH)
    pdoc.import_path.append(PROJECT_PATH)
    package = pdoc.Module(pdoc.import_module(PACKAGE_NAME),
                          allsubmodules=True)
    gen_module_doc(package, DOCS_PATH)

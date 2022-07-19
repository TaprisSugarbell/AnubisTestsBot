import os
import asyncio
import logging
import traceback
from glob import glob
from pkgutil import iter_modules
from importlib import import_module

NO_LOAD = []
rel_module = lambda _path: os.path.relpath(_path).replace("\\", ".")


async def list_modules(package: str = None, module_name: str = None):
    return [(f"{package + '.' if package else ''}{rel_module(_dir.path)}.{name}", name) for
            _dir, name, ispgk in iter_modules(glob(f"{module_name}/**", recursive=True)) if not ispgk]


async def load_modules(package: str = None, module_name: str = None):
    if not module_name:
        module_name = package
    count = 0
    modules = []
    imported = []
    not_imported = []

    list_of_modules = await list_modules(package, module_name)
    for module, name in list_of_modules:
        if name in NO_LOAD:
            not_imported.append(name)
            continue

        try:
            import_module(module)
            imported.append(name)
            modules.append(module)
            count += 1
        except Exception as exception:
            not_imported.append(name)

            tb_info = traceback.extract_tb(exception.__traceback__)
            tb_info.reverse()
            line_no = next((x[1] for x in tb_info if package in x[0]), None)
            logging.error("%s (%s:%s)", exception, name, line_no)

    match module_name:
        case "filters":
            logging.info("Filtros cargados: %s", ", ".join(imported))
            if not_imported:
                logging.info("Filtros no cargados: %s", ", ".join(not_imported))
        case "modules":
            logging.info("Módulos cargados: %s", ", ".join(imported))

            if not_imported:
                logging.info("Módulos no cargados: %s", ", ".join(not_imported))
        case "database":
            logging.info("Modelos cargados: %s", ", ".join(imported))
            if not_imported:
                logging.info("Modelos no cargados: %s", ", ".join(not_imported))
        case _:
            logging.info("Plugins cargados: %s", ", ".join(imported))
            if not_imported:
                logging.info("Plugins no cargados: %s", ", ".join(not_imported))

    return modules

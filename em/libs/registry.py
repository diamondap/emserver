from em.libs.base import BaseManager

REGISTRY = set()

def get_manager(manufacturer, model, firmware_version=None):
    if len(REGISTRY) == 0:
        initialize_registry()
    managers = [mgr for mgr in REGISTRY if (
        mgr.manufacturer == manufacturer and mgr.mode == model)]
    if firmware_version is not None:
        managers = [mgr for mgr in manager if (
            mgr.firmware_version == firmware_version)]
    return managers

def initialize_registry():
    for manager_class in BaseManager.__subclasses__():
        REGISTRY.add(manager_class())

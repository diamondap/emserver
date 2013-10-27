from em.libs.base import BaseManager
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
import em.libs.routers.medialink.mwn_wapr300n


REGISTRY = set()

def get_manager(manufacturer, model, firmware_version=None):
    if len(REGISTRY) == 0:
        initialize_registry()
    managers = [mgr for mgr in REGISTRY if (
        mgr.manufacturer.lower() == manufacturer.lower()
        and mgr.model.lower() == model.lower())]
    if firmware_version is not None:
        managers = [mgr for mgr in manager if (
            mgr.firmware_version == firmware_version)]
    if not managers:
        raise ObjectDoesNotExist("No manager available for {0} {1}".format(
            manufacturer, model))
    if len(managers) > 1:
        raise MultipleObjectsReturned("{0} managers found for {0} {1}".format(
            len(managers), manufacturer, model))
    return managers[0]

def initialize_registry():
    for manager_class in BaseManager.__subclasses__():
        REGISTRY.add(manager_class())

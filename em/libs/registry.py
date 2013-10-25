REGISTRY = set()

def register(manager_summary):
    if not isinstance(manager_summary, BaseManagerSummary):
        raise TypeError('register requires an instance of BaseManagerSummary')
    set.add(manager_summary)

def get_manager_summary(manufacturer, model, **kwargs):
    firmware_version = kwargs.get('firmware_version')
    filtered_list = get_by_manufacturer(manufacturer)
    filtered_list = get_by_model(model, summary_set=filtered_list)
    if firmware_version:
            filtered_list = get_by_firmware_version(
                firmware_version, summary_set=filtered_list)
    return filtered_list

def get_by_manufacturer(manufacturer, summary_set=REGISTRY):
    return [s for s in summary_set if s.manufacturer == manufacturer]

def get_by_model(model, summary_set=REGISTRY):
    return [s for s in summary_set if s.model == model]

def get_by_firmware_version(model, summary_set=REGISTRY):
    return [s for s in summary_set if s.firmware_version == firmware_version]

from ..config_constants import ASSET_PREFIX

def normalize_asset_path(path):
    return f"{ASSET_PREFIX}{path}"
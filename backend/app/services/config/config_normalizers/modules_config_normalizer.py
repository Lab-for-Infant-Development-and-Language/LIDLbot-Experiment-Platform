from .normalization_helpers import normalize_asset_path


def normalize_modules_config(modules_config):
    for module in modules_config.values():
        template = module.get("template")
        if template != "content_viewer":
            continue
        
        for content in module.get("contents", []):
            if content.get("type") != "image":
                continue
            content["value"] = normalize_asset_path(content["value"])
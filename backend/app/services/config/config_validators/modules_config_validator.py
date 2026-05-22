from pathlib import Path
from .validation_helpers import (
    require_type,
    require_list_of_type,
    require_in_set,
    require_asset_exists,
    require_non_empty_list,
    optional_int_in_range,
    optional_type
)
from ..config_constants import (
    TEMPLATES,
    CONTENT_TYPES
)
from app.core.logging import Logger


def validate_modules_config(modules_config, blocks_config, config_path):
    Logger.info("Validating 'modules_config.json'...")

    require_type(modules_config, dict, "modules_config.json")
    for module_name, module in modules_config.items():
        require_type(module, dict, module_name)
        
        template = module.get("template")
        require_in_set(template, TEMPLATES, "template", f"module name: '{module_name}'")
        
        match template:
            case "web_content_embed":
                _validate_web_content_embed_module(module, module_name)
            case "web_link":
                _validate_web_link_module(module, module_name)
            case "content_viewer":
                _validate_content_viewer_module(module, module_name, config_path)
            case "session_code_entry" | "session_code_display":
                _validate_session_code_module(module, module_name)
            case "prompter" | "voicebot" | "chatbot":
                _validate_cui_module(module, module_name, template, blocks_config)

    Logger.success("'modules_config.json' validated successfully.") 

def _validate_web_content_embed_module(module, module_name):
    require_type(module.get("url"), str, "url", f"module name: '{module_name}'")
    optional_int_in_range(module.get("button_reveal_timeout"), "button_reveal_timeout", f"module name: '{module_name}'", min_value=0)
    optional_int_in_range(module.get("auto_advance_timeout"), "auto_advance_timeout", f"module name: '{module_name}'", min_value=0)
    optional_type(module.get("embed_style"), str, "embed_style", f"module name: '{module_name}'")

def _validate_web_link_module(module, module_name):
    require_type(module.get("url"), str, "url", f"module name: '{module_name}'")

def _validate_content_viewer_module(module, module_name, config_path):
    contents = module.get("contents")
    require_non_empty_list(contents, "contents", f"module name: '{module_name}'")
    for i, content in enumerate(contents):
        content_type = content.get("type")
        content_value = content.get("value")
        require_in_set(content_type, CONTENT_TYPES, "type", f"module name: '{module_name}', 'contents'")
        require_type(content_value, str, "value", f"module name: '{module_name}', 'contents'")
        if content_type == "image":
            require_asset_exists(Path(config_path) / content_value, f"module name: '{module_name}', 'contents'")

def _validate_session_code_module(module, module_name):
    require_type(module.get("code"), str, "code", f"module name: '{module_name}'")

def _validate_cui_module(module, module_name, template, blocks_config):
    block = module.get("block")
    valid_blocks = set(blocks_config.keys())
    require_in_set(block, valid_blocks, "block", f"module name: '{module_name}'")

    if template == "voicebot" or template == "chatbot":
        optional_type(module.get("bot_name"), str, 'bot_name', f"module name: '{module_name}'")
        optional_type(module.get("min_words"), int, 'min_words', f"module name: '{module_name}'")
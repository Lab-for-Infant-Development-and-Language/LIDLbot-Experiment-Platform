from pathlib import Path
from .validation_helpers import (
    require_type,
    require_list_of_type,
    require_in_set,
    require_asset_exists,
    require_non_empty_list
)
from ..config_constants import (
    PROMPT_TYPES,
    RESPONSE_TYPES
)
from app.core.logging import Logger


def validate_trials_config(trials_config, config_path):    
    for filename, trial_pool in trials_config.items():
        require_non_empty_list(trial_pool, filename)
        for i, trial in enumerate(trial_pool, start=1):
            require_type(trial, dict, f"trial {i}", f"filename: '{filename}'")
            
            prompt = trial.get("prompter")
            require_type(prompt, dict, "prompter", f"filename: '{filename}', trial: {i}")
            prompt_type = prompt.get("type")
            prompt_value = prompt.get("value")
            require_in_set(prompt_type, PROMPT_TYPES, 'type', f"filename: '{filename}', trial: {i}, 'prompter'")
            require_type(prompt_value, str, "value", f"filename: '{filename}', trial: {i}, 'prompter'")
            if prompt_type == "image":
                require_asset_exists(Path(config_path) / prompt_value, f"filename: '{filename}', trial: {i}, 'prompter', 'value'")

            responses = trial.get("responses")
            require_type(responses, dict, "responses", f"filename: '{filename}', trial: {i}")
            response_type = responses.get("type")
            main_value = responses.get("main_value")
            alt_value = responses.get("alt_value")
            require_in_set(response_type, RESPONSE_TYPES, "type", f"filename: '{filename}', trial: {i}")
            require_type(main_value, str, "main_value", f"filename: '{filename}', trial: {i}")
            require_type(alt_value, str, "alt_value", f"filename: '{filename}', trial: {i}")
            if response_type == "audio":
                require_asset_exists(Path(config_path) / main_value, f"filename: '{filename}', trial: {i}, 'responses', 'main_value'")
                require_asset_exists(Path(config_path) / alt_value, f"filename: '{filename}', trial: {i}, 'responses', 'alt_value'")
from .validation_helpers import (
    require_type,
    require_list_of_type,
    require_in_set
)
from app.core.logging import Logger


def validate_sets_config(sets_config, modules_config):
    Logger.info("Validating 'sets_sequences_config.json'...")
    
    require_type(sets_config, dict, "sets_sequences_config.json")
    for sequence_name, sequence in sets_config.items():
        assistant = sequence.get("assistant")
        study = sequence.get("study")
        require_list_of_type(assistant, str, "assistant", f"sequence name: '{sequence_name}'")
        require_list_of_type(study, str, "study", f"sequence name: '{sequence_name}'")
        
        valid_modules = set(modules_config.keys())
        for assistant_module in assistant:
            require_in_set(assistant_module, valid_modules, assistant_module, f"sequence name: '{sequence_name}', 'assistant'")
        for study_module in study:
            require_in_set(study_module, valid_modules, study_module, f"sequence name: '{sequence_name}', 'study'")

    Logger.success("'sets_sequences_config.json' validated successfully.")  
from pathlib import Path
from app.services.fileio import load_file 
from .validation_helpers import (
    require_type,
    require_list_of_type,
    require_in_set,
    require_asset_exists,
    require_non_empty_list,
    require_int_in_range,
    optional_type
)
from .trials_config_validator import validate_trials_config
from app.core.logging import Logger


def validate_blocks_config(blocks_config, trials_config, config_path):
    Logger.info("Validating 'blocks_config.json'...")

    require_type(blocks_config, dict, "blocks_config.json")
    for block_name, block in blocks_config.items():
        require_type(block, dict, block_name)
        
        trial_pool_name = block.get("trials")
        require_type(trial_pool_name, str, "trials", f"block name: '{block_name}'")

        trial_pool_path = Path(config_path) / trial_pool_name
        require_asset_exists(trial_pool_path, f"block name: '{block_name}', trials")
        trials_config[trial_pool_name] = load_file(trial_pool_path)
    
    validate_trials_config(trials_config, config_path)
    for block_name, block in blocks_config.items():
        num_trials_to_sample = block.get("num_trials_to_sample")
        num_alts = block.get("num_alts")
        trial_pool_size = len(trials_config[trial_pool_name])
        require_int_in_range(num_trials_to_sample, "num_trials_to_sample", f"block name: '{block_name}'", min_value=1, max_value=trial_pool_size)
        require_int_in_range(num_alts, "num_alts", f"block name: '{block_name}'", min_value=0, max_value=num_trials_to_sample)
        optional_type(block.get("randomize"), bool, "randomize", f"block name: '{block_name}'")

    Logger.success("'blocks_config.json' validated successfully.")    
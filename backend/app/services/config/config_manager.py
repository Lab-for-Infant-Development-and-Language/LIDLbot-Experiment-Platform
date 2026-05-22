from .config_loader import load_configs
from app.core.logging import Logger
from .config_validators import (
    validate_experiment_config,
    validate_sets_config,
    validate_modules_config,
    validate_blocks_config # Blocks will validate trial configs
)
from .config_normalizers import (
    normalize_trials_config,
    normalize_modules_config
)


def manage_configs(config_path):
    configs = {}
    config_path = config_path

    Logger.section("Setup")
    
    Logger.newline()
    configs = load_configs(config_path)

    Logger.newline()
    validate_experiment_config(configs["experiment"])
    validate_blocks_config(configs["blocks"], configs["trial_pools"], config_path)
    validate_modules_config(configs["modules"], configs["blocks"], config_path)
    validate_sets_config(configs["sets"], configs["modules"])

    normalize_trials_config(configs["trial_pools"])
    normalize_modules_config(configs["modules"])
    return configs
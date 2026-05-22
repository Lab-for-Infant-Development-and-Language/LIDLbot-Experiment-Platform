from .validation_helpers import require_type
from app.core.logging import Logger


def validate_experiment_config(config):
    Logger.info("Validating 'experiment_config.json'...")
    
    require_type(config, dict, "experiment_config.json")
    require_type(config.get("experiment_name"), str, "experiment_name")

    Logger.success("'experiment_config.json' validated successfully.")
from pathlib import Path
from app.services.fileio import load_file
from .config_constants import DEFAULT_REQUIRED_FILES
from app.core.logging import Logger

def load_configs(config_path):
    Logger.info("Loading configuration files...")

    config = {}
    for relative_path, key in DEFAULT_REQUIRED_FILES.items():
        full_path = Path(config_path) / relative_path
        if not full_path.is_file():
            raise FileNotFoundError(f"Missing required file: '{full_path}'.")
        config[key] = load_file(full_path)
    config["trial_pools"] = {}
    
    Logger.success(f"Configuration files loaded successfully.")
    
    return config
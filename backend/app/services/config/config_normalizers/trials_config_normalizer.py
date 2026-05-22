from .normalization_helpers import normalize_asset_path


def normalize_trials_config(trials_config):
    for trial_pool in trials_config.values():
        for trial in trial_pool:
            prompter = trial.get("prompter")
            if prompter.get("type") == "image":
                prompter["value"] = normalize_asset_path(prompter["value"])
        
            responses = trial.get("responses")
            if responses.get("type") == "audio":
                responses["main_value"] = normalize_asset_path(responses["main_value"])
                responses["alt_value"] = normalize_asset_path(responses["alt_value"])
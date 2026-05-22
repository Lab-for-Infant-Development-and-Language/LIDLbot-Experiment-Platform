from app.services.shuffle import spotify_shuffle
from copy import deepcopy
import random

class SessionController:
    def __init__(self, configs):
        self._configs = configs
        self._rng = None
        self._selected_set = None
        self._selected_sequence = None
        self._modules = None
        self._current_module_index = None
        self._current_trial_index = 0
    
    def get_experiment_name(self):
        return self._configs.get("experiment").get("experiment_name")
    
    def get_set_names(self):
        return tuple(self._configs.get("sets", []).keys())
    
    def get_selected_set(self):
        return self._selected_set
    
    def set_selected_set(self, selected_set):
        self._selected_set = selected_set

    def get_selected_sequence(self):
        return self._selected_sequence
    
    def set_selected_sequence(self, selected_sequence):
        self._selected_sequence = selected_sequence
    
    def get_module_by_index(self, index):
        if self._modules is None:
            raise ValueError(f"Modules not defined.")
        if index < 0 or index >= len(self._modules):
            raise ValueError(f"Index out of bounds. Valid range: [0, {len(self._modules)}).")
        return deepcopy(self._modules[index])
    
    def get_current_module(self):
        if self._current_module_index is None:
            self._current_module_index = 0
        return self.get_module_by_index(self._current_module_index)
    
    def get_current_module_index(self):
        return self._current_module_index
    
    def increment_current_module_index(self):
        if self._current_module_index is None:
            self._current_module_index = 0
        else:
            self._current_module_index += 1
        self._current_trial_index = 0
        return self._current_module_index
    
    def get_current_trial_index(self):
        return self._current_trial_index
    
    def increment_current_trial_index(self):
        self._current_trial_index += 1
        return self._current_trial_index
    
    def is_complete(self):
        if self._modules is None:
            return False
        return self._current_module_index >= len(self._modules)
    
    def get_num_modules(self):
        if self._modules is None:
            return 0
        return len(self._modules)
        
    def set_seed(self, seed):
        self._rng = random.Random(seed)
    
    def set_rng(self, rng):
        self._rng = rng
    
    def process_modules(self):
        if self._selected_sequence is None or self._selected_set is None or self._rng is None:
            raise ValueError(f"Set, sequence, and seed/rng must be specified.")
        
        self._current_module_index = 0
        self._modules = deepcopy(self._configs.get("sets", {}).get(self._selected_set).get(self._selected_sequence, []))
        for i, module_name in enumerate(self._modules):
            self._modules[i] = deepcopy(self._configs.get("modules", {}).get(module_name))
            if self._modules[i].get("template") in ("prompter", "voicebot", "chatbot"):
                block_name = self._modules[i].get("block")
                self._modules[i]["trials"] = self._randomize_block(block_name)
    
    def _randomize_block(self, block_name):
        if self._rng is None:
            raise ValueError(f"Seed/rng must be specified.")

        block = deepcopy(self._configs.get("blocks", {}).get(block_name))
        trial_pool = deepcopy(self._configs.get("trial_pools", {}).get(block.get("trials")))
        num_trials_to_sample = block.get("num_trials_to_sample")
        num_alts = block.get("num_alts")
        randomize = block.get("randomize", True)

        if randomize:
            selected_trials = self._rng.sample(trial_pool, num_trials_to_sample)
        else:
            selected_trials = trial_pool[:num_trials_to_sample]

        objs = self._distribute_alts(selected_trials, num_alts)
        if randomize:
            return spotify_shuffle(objs, rng=self._rng)
        return [obj[1] for obj in objs]

    def _distribute_alts(self, values, num_alts):
        if self._rng is None:
            raise ValueError(f"Seed/rng must be specified.")

        objs = [['MAIN', value] for value in values]
        chosen = self._rng.sample(objs, num_alts)

        for obj in objs:
            if obj in chosen:
                obj[0] = 'ALT'
                obj[1]["responses"]["value"] = obj[1]["responses"]["alt_value"]
            else:
                obj[1]["responses"]["value"] = obj[1]["responses"]["main_value"]
        return objs
    
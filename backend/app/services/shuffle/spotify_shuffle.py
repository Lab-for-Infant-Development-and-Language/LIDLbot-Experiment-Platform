import random
import numpy as np
from collections import defaultdict


def spotify_shuffle(arr, epsilon=0.05, seed=None, rng=None):
    if len(arr) < 1:
        return arr
        
    if rng is None:
        rng = random.Random(seed)
    
    groups = defaultdict(list)
    for group, value in arr:
        groups[group].append(value)
    
    for group in groups:
        rng.shuffle(groups[group])
    
    schedules = []
    for group, values in groups.items():
        n = len(values)
        step = 1.0 / n
        normalized_indices = [i * step for i in range(n)]
        schedules.append({
            "group": group,
            "values": values,
            "indices": normalized_indices,
            "i": 0
        })

    for schedule in schedules:
        max_shift = 1.0 - schedule["indices"][-1]
        schedule["offset"] = rng.uniform(0, max_shift)
    
    result = []
    total = len(arr)

    for _ in range(total):
        best = None
        best_score = float("inf")

        for schedule in schedules:
            if schedule["i"] >= len(schedule["values"]):
                continue
            
            base_score = schedule["indices"][schedule["i"]] + schedule["offset"]
            jitter = rng.uniform(-epsilon, epsilon)
            score = max(0.0, base_score + jitter)

            if score < best_score:
                best_score = score
                best = schedule
        
        result.append(best["values"][best["i"]])
        best["i"] += 1
    
    return result
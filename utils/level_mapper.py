def map_level(level_str):
    mapping = {
        "Junior": 1,
        "Intermediate": 2,
        "Senior": 3
    }
    return mapping.get(level_str, 2)

import json


async def get_json_keys_title_space(filename: str) -> list:
    """
    Gets dict title-space-replace keys from JSON-file in ./data/filename.json
    """
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return [item.title().replace('_', ' ') for item in data.keys()]


async def get_json_keys(filename: str) -> list:
    """
    Gets dict keys from JSON-file in ./data/filename.json
    """
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.keys()


async def get_json_value(filename: str, key):
    """
    Gets dict value by key from JSON-file in ./data/filename.json
    """
    with open(f'data/{filename}.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data[key]


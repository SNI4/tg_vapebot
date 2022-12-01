import json
import logging
import os


async def delete_json(user_id: str, message_id: str) -> None:
    os.remove(f'data/adverts/{user_id}/{message_id}.json')


async def get_advert_dict(user_id: str, message_id: str) -> dict:
    try:
        with open(f'data/adverts/{user_id}/{message_id}.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data

    except Exception as e:
        print(e)


async def save_json(user_id: str, message_id: str, second_messages_id: list, data: dict) -> None:
    path = f'data/adverts/{user_id}'
    try:
        os.makedirs(path)
    except FileExistsError:
        pass

    with open(f'{path}/{message_id}.json', 'w+', encoding='utf-8') as f:
        data['second_messages_id'] = second_messages_id
        json.dump(data, f, indent=4, ensure_ascii=False, )


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

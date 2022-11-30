import json


async def save_user_json_advert(user_id: str, message_id: str, data: dict) -> None:
    with open(f'data/adverts/{user_id}/{message_id}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
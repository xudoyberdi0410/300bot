from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


def filter_url(obj):
    return (obj['type'] == 'url') or (obj['type'] == 'text_link') 



class FilterEntities(BoundFilter):
    async def check(self, message: types.Message):
        if not message.entities:
            return False
        urls = list(filter(filter_url, message.entities))
        if not urls:
            return False
        return True

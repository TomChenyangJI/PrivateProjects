import asyncio
from googletrans import Translator


def out_wrapper(func):
    def wrapper(content):
        result = asyncio.run(func(content))
        return result
    return wrapper


@out_wrapper
async def translate_content(content) -> str:
    async with Translator() as translator:
        translations = await translator.translate(content, dest='en')
        return translations.text

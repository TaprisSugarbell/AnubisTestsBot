import asyncio
from .load_plugins import load_modules


def run_async(obj):
    return asyncio.new_event_loop().run_until_complete(obj())


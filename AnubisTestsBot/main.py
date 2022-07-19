import asyncio
import logging
from aiohttp import web
from __vars__ import WEBHOOK
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.dispatcher.webhook.aiohttp_server import (
    TokenBasedRequestHandler,
    setup_application,
)
from AnubisTestsBot import dp, bot, form_router, PACKAGE
from helper.load_plugins import load_modules
from config_start import on_startup, on_polling_startup, on_webhook_startup, on_webhook_shutdown


async def main():
    dp.startup.register(on_polling_startup)
    await load_modules(PACKAGE, "plugins")
    dp.include_router(form_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    dp.startup.register(on_startup)
    if WEBHOOK:
        app = web.Application()

        TokenBasedRequestHandler(
            dispatcher=dp,
            bot_settings=dict(session=AiohttpSession(), parse_mode="HTML"),
        ).register(app, "/webhook/{bot_token}")

        dp.startup.register(on_webhook_startup)
        dp.shutdown.register(on_webhook_shutdown)

        setup_application(app, dp)
        web.run_app(app, host="0.0.0.0", port=8080)
    else:
        try:
            asyncio.run(main())
        except Exception as e:
            logging.info("Shutting down... %s", e)
            raise


import contextlib
import logging
from AnubisTestsBot import dp, bot, load_modules, connect
from __vars__ import *


async def check_settings():
    user = await bot.get_me()

    if not user.can_join_groups:
        logging.error("El bot debe poder unirse a grupos.")

    if not user.can_read_all_group_messages:
        logging.warning("Debes desactivar el modo privacidad.")

    if not user.supports_inline_queries:
        logging.error("Debes activar el modo inline.")


async def on_startup():
    await check_settings()
    await connect(DATABASE_URL, await load_modules(module_name="database"))


async def on_polling_startup():
    with contextlib.suppress(Exception):
        await bot.delete_webhook(drop_pending_updates=True)
        logging.info("WEBHOOK deleted!")
    # async for clone in database.Clone.all():
    #     asyncio.create_task(start_clone_polling(clone))


async def on_webhook_startup():
    await bot.set_webhook(
        url=f"{WEBHOOK_URL}/webhook/{BOT_TOKEN}",
        certificate=WEBHOOK_CERT,
        drop_pending_updates=True,
    )


async def on_webhook_shutdown():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    logging.info("Webhook server stopped")

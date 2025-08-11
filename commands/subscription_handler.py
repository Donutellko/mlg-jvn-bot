import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

import user_data_helper
from clients import gestion_client
from clients.gestion_client_helper import Activity
from commands.command_list import get_gestion_link

COMMAND_FORCE_SCHEDULER = "force_scheduler"
logger = logging.getLogger('subscription_handler')


async def force_scheduler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Triggered with /force_scheduler
    """
    user_id = update.effective_user.id
    new_appearances = await job_check_updates(context, user_id)
    reply_text = f"new_appearances={new_appearances}"
    context.user_data["last_response"] = reply_text
    await update.message.reply_text(reply_text, disable_web_page_preview=True)


async def handle_scheduled_subscription(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    """
    user_id = context.job.user_id
    await job_check_updates(context, user_id)


async def job_check_updates(context: ContextTypes.DEFAULT_TYPE, user_id: int) -> int:
    user_data = context.user_data
    subscriptions = user_data_helper.subscriptions(user_data)
    logger.info(f"job_check_updates for user {user_id}, subscriptions count={len(subscriptions)}")

    if len(subscriptions) == 0:
        context.job.schedule_removal()
        logger.info(f"removing job for user {user_id} because has no subscription")
        return 0

    for subscription in subscriptions:
        await job_check_updates_subscription(context, user_id, subscription)


async def job_check_updates_subscription(context: ContextTypes.DEFAULT_TYPE, user_id: int, subscription: dict):
    previous_items = subscription[user_data_helper.LAST_SAVED_PLAZAS_KEY]
    actual_items = gestion_client.get_activities(all=False)

    new_appearances = find_new_appearances(actual_items, previous_items)

    response = '\n\n'.join([str(a) for a in new_appearances])

    subscription[user_data_helper.LAST_SAVED_PLAZAS_KEY] = actual_items
    user_data_helper.subscriptions(context.user_data, [subscription])

    if len(response) > 0:
        logger.info(f"Found some updates: {response}")

        response = f"Found some updates: \n\n{response}\n\n{get_gestion_link()}"
        await context.bot.send_message(chat_id=user_id, text=response,
                                       parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)
    else:
        logger.info(f"No updates for {user_id}")
        # await context.bot.send_message(chat_id=user_id, text="No updates")

    return len(new_appearances)


def get_items_available(item: Activity) -> int:
    if item is None:
        return 0
    return item.plazas_libres


def to_dict(items: [Activity]) -> dict:
    return {item.codigo: item for item in items}


def find_new_appearances(actual_items: [Activity], previous_items: [Activity]) -> list:
    previous_dict = to_dict(previous_items)

    new_appearances = []
    for item in actual_items:
        prev = previous_dict.get(item.codigo)
        if prev is None or get_items_available(item) > get_items_available(prev):
            new_appearances.append(item)

    return new_appearances

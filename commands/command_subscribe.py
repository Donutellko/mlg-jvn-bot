from telegram import Update
from telegram.ext import ContextTypes

import user_data_helper
from clients import gestion_client
from commands import subscription_handler_starter

COMMAND_SUBSCRIBE = "subscribe"
COMMAND_UNSUBSCRIBE = "unsubscribe"


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    """
    user_data = context.user_data
    user_id = update.effective_user.id

    actual_activities = gestion_client.get_activities(all=False, page=1)
    user_data_helper.add_subscription(user_data, actual_activities)

    subscription_handler_starter.schedule_for_user(context.application.job_queue, user_id=user_id)

    await update.message.reply_text("""
    FOR NOW ONLY FIRST PAGE
    You have subscribed for updates in your list of favorites, expect some updates now and then.
    """)


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    """

    user_data_helper.reset_subscriptions(context.user_data)

    await update.message.reply_text("""
    You have unsubscribed for updates.
    """)

import datetime
import logging

from telegram.ext import Application, ContextTypes

import user_data_helper
from commands import subscription_handler

SCHEDULER_INTERVAL = 300 # seconds
COMMAND_FORCE_SCHEDULER = "force_scheduler"
logger = logging.getLogger('subscription_handler_starter')


def start_scheduler(bot: Application):
    if bot.job_queue is None:
        raise "You need to `pip install python-telegram-bot[job-queue]` extension"
    bot.job_queue.run_once(schedule_all_users, when=1)


async def schedule_all_users(context: ContextTypes.DEFAULT_TYPE):
    all_users_data = context.application.user_data.items()
    for user_id, user_data in all_users_data:
        if user_data_helper.is_subscribed_citas(user_data):
            schedule_for_user(context.application.job_queue, user_id)


def schedule_for_user(job_queue, user_id):
    delta = datetime.timedelta(seconds=SCHEDULER_INTERVAL)
    logger.info(f"job_queue.run_repeating(user_id={user_id}, interval={delta}) and also running it right away")
    job_queue.run_repeating(
        callback=subscription_handler.handle_scheduled_subscription,
        user_id=user_id,
        interval=delta)
    job_queue.run_once(
        callback=subscription_handler.handle_scheduled_subscription,
        name="handle_scheduled_subscription.run_once",
        when=1,
        user_id=user_id)

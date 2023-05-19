import logging
from telegram import Update
from telegram.ext import ContextTypes


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if hasattr(context, 'job') and context.job is not None:
        chat_id = context.job.chat_id
        message_id = 'from job'
    else:
        chat_id = update.message.chat_id
        message_id = update.message.message_id
    message = "Error happened"
    await context.bot.send_message(chat_id=chat_id, reply_to_message_id=message_id, text=message)

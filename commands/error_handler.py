import logging
from telegram import Update
from telegram.ext import ContextTypes

from commands import command_help

MESSAGE_LENGTH_LIMIT = 4096

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logging.error(msg="Exception while handling an update:", exc_info=context.error)
    if hasattr(context, 'job') and context.job is not None:
        chat_id = context.job.user_id
        message_id = 'from job'
    else:
        chat_id = update.message.chat_id
        message_id = update.message.message_id

    last_response = context.user_data.get('last_response', None)
    if len(last_response) > MESSAGE_LENGTH_LIMIT:
        last_response = (f"MESSAGE TOO LONG !!! {len(last_response)} chars, max admitted {MESSAGE_LENGTH_LIMIT}:\n\n" +
                         last_response[:500] + "...")

    message = f"Error happened (maybe a response is incorrect /{command_help.DEBUG_LAST_RESPONSE}): " + str(context.error)
    await context.bot.send_message(chat_id=chat_id, reply_to_message_id=message_id, text=message)

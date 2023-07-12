from telegram import Update
from telegram.ext import ContextTypes

import jvn_client

COMMAND_LIST = "list"


async def list_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""

    activities = jvn_client.get_activities()
    reply_text = "Next activities: " + '\n'.join([str(a) for a in activities])

    await update.message.reply_text(reply_text)


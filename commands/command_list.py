from telegram import Update
from telegram.ext import ContextTypes

import jvn_client

COMMAND_LIST_ALL = "list_all"
COMMAND_LIST_AVAILABLE = "list"


async def list_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list_all is issued."""

    activities = jvn_client.get_activities(all=True)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Next activities: \n{activities_text}\nGestion: {jvn_client.URL_OCCUPATION}"

    await update.message.reply_text(reply_text)


async def list_available_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""

    activities = jvn_client.get_activities(all=False)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Next activities: \n{activities_text}\nGestion: {jvn_client.URL_OCCUPATION}"

    await update.message.reply_text(reply_text)


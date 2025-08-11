from telegram import Update
from telegram.ext import ContextTypes


COMMAND_START = "start"
COMMAND_HELP = "help"
DEBUG_PERSISTENCE = "debug_persistence"
DEBUG_LAST_RESPONSE = "debug_last_response"
DEBUG_PERSISTENCE_CLEAR = "debug_persistence_clear"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    reply_text = """
    /help - To see this message
    /list - To see list of existing activities
    """

    await update.message.reply_text(reply_text)


async def debug_last_response_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message containing current persistence state."""
    await update.message.reply_text(
        "Current persistence state: \n" + str(context.user_data.get('last_response', 'No last response found'))
    )

async def persistence_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message containing current persistence state."""
    await update.message.reply_text(
        "Current persistence state: \n" + str(context.user_data)
    )

async def persistence_clear_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send message containing current persistence state."""
    context.user_data.clear()
    await update.message.reply_text(
        "Cleared persistence."
    )
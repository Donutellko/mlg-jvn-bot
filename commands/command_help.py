from telegram import Update
from telegram.ext import ContextTypes


COMMAND_START = "start"
COMMAND_HELP = "help"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    reply_text = """
    /help - To see this message
    /list - To see list of existing activities
    """

    await update.message.reply_text(reply_text)


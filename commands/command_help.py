from telegram import Update
from telegram.ext import ContextTypes


COMMAND_START = "start"
COMMAND_HELP = "help"


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    reply_text = """
    You have to select a specialist and a motive to be able to get response for /citas

    /help - To see this message
    /doctors - To see list of available specialists
    /motives - To see possible motives for the selected specialist

    /citas - To see available timeslots for selected specialist and motive
    """

    await update.message.reply_text(reply_text)


#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import asyncio
import logging

from telegram import __version__ as TG_VER, BotCommand

from commands import command_help, error_handler, command_list

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
    PicklePersistence,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# conversation stages
SELECT_SPECIALTY, SELECT_MOTIVE = range(2)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/persistentconversationbot.py
def main() -> None:
    """Get the token."""
    with open('token.txt', 'r') as f:
        token = f.read().strip()

    """Start the bot."""
    # Create the Application and pass it your bot's token.
    persistence = PicklePersistence(filepath="persistence")
    application = Application.builder().token(token).persistence(persistence).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler(command_help.COMMAND_START, command_help.help_command))
    application.add_handler(CommandHandler(command_help.COMMAND_HELP, command_help.help_command))

    application.add_handler(CommandHandler(command_list.COMMAND_LIST_ALL, command_list.list_all_command))
    application.add_handler(CommandHandler(command_list.COMMAND_LIST_AVAILABLE, command_list.list_available_command))
    application.add_handler(CommandHandler(command_list.COMMAND_LIST_ONCOMING, command_list.list_oncoming_command))

    command = [
        BotCommand(command_help.COMMAND_HELP, "See explanations"),
        BotCommand(command_list.COMMAND_LIST_ALL, "List all activities"),
        BotCommand(command_list.COMMAND_LIST_AVAILABLE, "List available activities"),
        BotCommand(command_list.COMMAND_LIST_ONCOMING, "List oncoming activities"),
    ]
    asyncio.ensure_future(application.bot.set_my_commands(command))

    application.add_error_handler(error_handler.error_handler)

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

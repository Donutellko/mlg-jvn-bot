from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from clients import gestion_client, programas_client

COMMAND_LIST_ALL = "list_all"
COMMAND_LIST_AVAILABLE = "list"
COMMAND_LIST_ONCOMING = "oncoming"


async def list_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list_all is issued."""

    activities = gestion_client.get_activities(all=True, page=1)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

    activities = gestion_client.get_activities(all=True, page=2)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Page 2: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


async def list_available_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""

    activities = gestion_client.get_activities(all=False, page=1)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades con plazas: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)

    activities = gestion_client.get_activities(all=False, page=2)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Page 2: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


async def list_oncoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /oncoming is issued."""

    activities = programas_client.get_oncoming(all=False)
    activities_text = '\n\n'.join([a.str_oncoming() for a in activities])
    reply_text = f"Actividades desponibles: \n{activities_text}\n{get_oncoming_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def get_gestion_link() -> str:
    return get_markdown_link("\\> Gestion \\<", gestion_client.URL_OCCUPATION)


def get_oncoming_link() -> str:
    return get_markdown_link("\\> Listado \\<", gestion_client.URL_ONCOMING)


def get_markdown_link(text: str, url: str) -> str:
    return f"[{text}]({url})"


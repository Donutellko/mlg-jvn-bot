from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from clients import gestion_client, programas_client

COMMAND_LIST_ALL = "list_all"
COMMAND_LIST_AVAILABLE = "list"
COMMAND_LIST_ONCOMING = "oncoming"


async def list_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list_all is issued."""

    activities = gestion_client.get_activities(all=True)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


async def list_available_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""

    activities = gestion_client.get_activities(all=False)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades con plazas: \n{activities_text}\n\n{get_gestion_link()}"

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


async def list_oncoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /oncoming is issued."""

    results = programas_client.get_oncoming(all=False)
    reply_parts = []

    for result in results:
        if result['error']:
            reply_parts.append(f"*{result['name']}*: Error - {result['error']}")
        else:
            if result['entries']:
                activities_text = '\n'.join([a.str_oncoming() for a in result['entries']])
                reply_parts.append(f"*{result['name']}* ({len(result['entries'])} actividades):\n{activities_text}")
                # Add link to the source
                reply_parts.append(get_markdown_link("\\> Ver más \\<", result['url']))
            else:
                reply_parts.append(f"*{result['name']}*: No hay actividades disponibles")

    if reply_parts:
        reply_text = '\n\n'.join(reply_parts)
    else:
        reply_text = "No se encontraron actividades disponibles."

    await update.message.reply_text(text=reply_text,
                                    parse_mode=ParseMode.MARKDOWN_V2, disable_web_page_preview=True)


def get_gestion_link() -> str:
    return get_markdown_link("\\> Gestion \\<", gestion_client.URL_OCCUPATION)


def get_oncoming_link() -> str:
    return get_markdown_link("\\> Listado \\<", gestion_client.URL_ONCOMING)


def get_markdown_link(text: str, url: str) -> str:
    return f"[{text}]({url})"

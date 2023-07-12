from telegram import Update
from telegram.ext import ContextTypes

from clients import gestion_client, programas_client

COMMAND_LIST_ALL = "list_all"
COMMAND_LIST_AVAILABLE = "list"
COMMAND_LIST_ONCOMING = "oncoming"


async def list_all_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list_all is issued."""

    activities = gestion_client.get_activities(all=True)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades: \n{activities_text}\nGestion: {gestion_client.URL_OCCUPATION}"

    await update.message.reply_text(reply_text)


async def list_available_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /list is issued."""

    activities = gestion_client.get_activities(all=False)
    activities_text = '\n\n'.join([str(a) for a in activities])
    reply_text = f"Actividades con plazas: \n{activities_text}\nGestion: {gestion_client.URL_OCCUPATION}"

    await update.message.reply_text(reply_text)


async def list_oncoming_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /oncoming is issued."""

    activities = programas_client.get_oncoming(all=False)
    activities_text = '\n\n'.join([a.str_oncoming() for a in activities])
    reply_text = f"Actividades desponibles: \n{activities_text}\nLista: {programas_client.URL_ONCOMING}"

    await update.message.reply_text(reply_text)


from telebot import TeleBot
from telebot.util import escape
from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

import textos
import botoes
from api import API
from plugins import erros


def menu_start() -> InlineKeyboardMarkup:
    menu = [
        [
            InlineKeyboardButton(
                text=botoes.minhas_notas, switch_inline_query_current_chat=""
            )
        ],
        [InlineKeyboardButton(text=botoes.criar_nota, callback_data="#criar_nota")],
    ]
    return InlineKeyboardMarkup(keyboard=menu)


def comando_start(msg: Message, bot: TeleBot) -> None:
    try:
        _ = API(msg.from_user)
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.start.format(escape(msg.from_user.first_name)),
            reply_markup=menu_start(),
        )
    except Exception as ex:
        erros.analisar_erro(req=msg, bot=bot, ex=ex)

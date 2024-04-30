from enum import Enum

from telebot import TeleBot
from telebot.handler_backends import StatesGroup, State
from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import textos
import botoes
from api import API
from plugins import erros


class EtapaDeletarNota(StatesGroup):
    escolher = State()


class OpcaoMenuDeletarNota(str, Enum):
    cancelar = botoes.cancelar
    deletar = botoes.deletar


def menu_deletar_nota() -> ReplyKeyboardMarkup:
    menu = list(OpcaoMenuDeletarNota)
    return ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True).add(*menu)


def resposta_deletar_nota(rsp: CallbackQuery, bot: TeleBot) -> None:
    id = rsp.data.split()[1]
    bot.set_state(user_id=rsp.from_user.id, state=EtapaDeletarNota.escolher)
    with bot.retrieve_data(user_id=rsp.from_user.id) as dados:
        dados["id"] = id
    bot.send_message(
        chat_id=rsp.from_user.id,
        text=textos.confirmar_delecao,
        reply_markup=menu_deletar_nota(),
    )


def etapa_escolher_deletar_nota(msg: Message, bot: TeleBot) -> None:
    if msg.text == OpcaoMenuDeletarNota.deletar:
        try:
            with bot.retrieve_data(user_id=msg.from_user.id) as dados:
                id = dados["id"]
                api = API(msg.from_user)
                nota = api.deletar_nota(id)
                bot.send_message(
                    chat_id=msg.from_user.id,
                    text=textos.nota_deletada,
                    reply_markup=ReplyKeyboardRemove(),
                )
            bot.delete_state(user_id=msg.from_user.id)
        except Exception as ex:
            erros.analisar_erro(req=msg, bot=bot, ex=ex)
    else:
        bot.send_message(chat_id=msg.from_user.id, text=textos.opcao_invalida)

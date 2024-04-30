from enum import Enum

from telebot import TeleBot
from telebot.util import escape
from telebot.handler_backends import StatesGroup, State
from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

import esquemas
import textos
import botoes
from api import API
from plugins import erros


class OpcaoMenuNovaNota(str, Enum):
    titulo = botoes.novo_titulo
    texto = botoes.novo_texto
    ver = botoes.ver_nota
    cancelar = botoes.cancelar
    salvar = botoes.salvar


class EtapaNovaNota(StatesGroup):
    escolher = State()
    texto = State()
    titulo = State()


def menu_criar_nota() -> ReplyKeyboardMarkup:
    menu = list(OpcaoMenuNovaNota)
    return ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True).add(*menu)


def resposta_criar_nota(rsp: CallbackQuery, bot: TeleBot) -> None:
    bot.set_state(user_id=rsp.from_user.id, state=EtapaNovaNota.escolher)
    bot.send_message(
        chat_id=rsp.from_user.id,
        text=textos.definir_nota,
        reply_markup=menu_criar_nota(),
    )


def etapa_escolher_criar_nota(msg: Message, bot: TeleBot) -> None:
    if msg.text == OpcaoMenuNovaNota.titulo:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.definir_titulo,
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.set_state(msg.from_user.id, EtapaNovaNota.titulo)
    elif msg.text == OpcaoMenuNovaNota.texto:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.definir_texto,
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.set_state(msg.from_user.id, EtapaNovaNota.texto)
    elif msg.text == OpcaoMenuNovaNota.ver:
        with bot.retrieve_data(user_id=msg.from_user.id) as dados:
            titulo = dados.get("titulo")
            texto = dados.get("texto")
            bot.send_message(
                chat_id=msg.from_user.id,
                text=textos.nota.format(escape(titulo), escape(texto)),
                reply_markup=menu_criar_nota(),
            )
    elif msg.text == OpcaoMenuNovaNota.salvar:
        with bot.retrieve_data(user_id=msg.from_user.id) as dados:
            titulo = dados.get("titulo")
            texto = dados.get("texto")
            if not titulo or not texto:
                bot.send_message(
                    chat_id=msg.from_user.id, text="Título ou texto vázio."
                )
            else:
                try:
                    api = API(msg.from_user)
                    nota = api.criar_nota(esquemas.NovaNota(titulo=titulo, texto=texto))
                    bot.delete_state(user_id=msg.from_user.id)
                    bot.send_message(
                        chat_id=msg.from_user.id,
                        text=textos.nota_salva,
                        reply_markup=ReplyKeyboardRemove(),
                    )
                except Exception as ex:
                    erros.analisar_erro(req=msg, bot=bot, ex=ex)
    else:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.opcao_invalida,
        )


def etapa_titulo_criar_nota(msg: Message, bot: TeleBot) -> None:
    with bot.retrieve_data(user_id=msg.from_user.id) as dados:
        dados["titulo"] = msg.text
    bot.send_message(
        chat_id=msg.from_user.id,
        text=textos.titulo_adicionado,
        reply_markup=menu_criar_nota(),
    )
    resposta_criar_nota(rsp=msg, bot=bot)


def etapa_texto_criar_nota(msg: Message, bot: TeleBot) -> None:
    with bot.retrieve_data(user_id=msg.from_user.id) as dados:
        dados["texto"] = msg.text
    bot.send_message(
        chat_id=msg.from_user.id,
        text=textos.texto_adicionado,
        reply_markup=menu_criar_nota(),
    )
    resposta_criar_nota(rsp=msg, bot=bot)

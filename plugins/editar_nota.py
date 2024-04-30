from enum import Enum

from telebot import TeleBot
from telebot.util import escape
from telebot.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from telebot.handler_backends import State, StatesGroup

import textos
import botoes
import esquemas
from api import API
from plugins import erros


class EtapaEditarNota(StatesGroup):
    escolher = State()
    texto = State()
    titulo = State()


class OpcaoMenuEditarNota(str, Enum):
    titulo = botoes.editar_titulo
    texto = botoes.editar_texto
    ver = botoes.ver_nota
    cancelar = botoes.cancelar
    salvar = botoes.salvar


def menu_editar_nota() -> ReplyKeyboardMarkup:
    menu = list(OpcaoMenuEditarNota)
    return ReplyKeyboardMarkup(resize_keyboard=True, is_persistent=True).add(*menu)


def resposta_editar_nota(
    rsp: CallbackQuery, bot: TeleBot, retorno: bool = False
) -> None:
    try:
        bot.set_state(user_id=rsp.from_user.id, state=EtapaEditarNota.escolher)
        if not retorno:
            id = rsp.data.split()[1]
            api = API(rsp.from_user)
            nota = api.obter_nota(id)
            with bot.retrieve_data(user_id=rsp.from_user.id) as dados:
                dados["id"] = id
                dados["titulo"] = nota.titulo
                dados["texto"] = nota.texto
        bot.send_message(
            chat_id=rsp.from_user.id,
            text=textos.definir_nota,
            reply_markup=menu_editar_nota(),
        )
    except Exception as ex:
        erros.analisar_erro(req=rsp, bot=bot, ex=ex)


def etapa_escolher_editar_nota(msg: Message, bot: TeleBot) -> None:
    if msg.text == OpcaoMenuEditarNota.titulo:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.definir_titulo,
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.set_state(msg.from_user.id, EtapaEditarNota.titulo)
    elif msg.text == OpcaoMenuEditarNota.texto:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.definir_texto,
            reply_markup=ReplyKeyboardRemove(),
        )
        bot.set_state(msg.from_user.id, EtapaEditarNota.texto)
    elif msg.text == OpcaoMenuEditarNota.ver:
        with bot.retrieve_data(user_id=msg.from_user.id) as dados:
            titulo = dados.get("titulo")
            texto = dados.get("texto")
            bot.send_message(
                chat_id=msg.from_user.id,
                text=textos.nota.format(escape(titulo), escape(texto)),
            )
    elif msg.text == OpcaoMenuEditarNota.salvar:
        try:
            with bot.retrieve_data(user_id=msg.from_user.id) as dados:
                api = API(msg.from_user)
                id = dados["id"]
                editar_nota = esquemas.EditarNota.model_validate(dados)
                nota = api.editar_nota(id=id, nota=editar_nota)
                bot.send_message(
                    chat_id=msg.from_user.id,
                    text=textos.nota_salva,
                    reply_markup=ReplyKeyboardRemove(),
                )
            bot.delete_state(user_id=msg.from_user.id)
        except Exception as ex:
            erros.analisar_erro(req=msg, bot=bot, ex=ex)
    else:
        bot.send_message(
            chat_id=msg.from_user.id,
            text=textos.opcao_invalida,
        )


def etapa_titulo_editar_nota(msg: Message, bot: TeleBot) -> None:
    with bot.retrieve_data(user_id=msg.from_user.id) as dados:
        dados["titulo"] = msg.text
    bot.send_message(
        chat_id=msg.from_user.id,
        text=textos.titulo_adicionado,
        reply_markup=menu_editar_nota(),
    )
    resposta_editar_nota(rsp=msg, bot=bot, retorno=True)


def etapa_texto_editar_nota(msg: Message, bot: TeleBot) -> None:
    with bot.retrieve_data(user_id=msg.from_user.id) as dados:
        dados["texto"] = msg.text
    bot.send_message(
        chat_id=msg.from_user.id,
        text=textos.texto_adicionado,
        reply_markup=menu_editar_nota(),
    )
    resposta_editar_nota(rsp=msg, bot=bot, retorno=True)

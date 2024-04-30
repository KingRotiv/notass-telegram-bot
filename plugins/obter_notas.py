from telebot import TeleBot
from telebot.util import escape
from telebot.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

import textos
import botoes
from api import API
from plugins import erros


def menu_nota(id: int) -> InlineKeyboardMarkup:
    menu = [
        [
            InlineKeyboardButton(
                text=botoes.editar, callback_data=f"#editar_nota {id}"
            ),
            InlineKeyboardButton(
                text=botoes.deletar, callback_data=f"#deletar_nota {id}"
            ),
        ],
        [InlineKeyboardButton(text="Menu Principal", callback_data="#start")],
    ]
    return InlineKeyboardMarkup(keyboard=menu)


def consulta_obter_notas(cst: InlineQuery, bot: TeleBot) -> None:
    try:
        api = API(cst.from_user)
        notas = api.obter_notas()
        if notas:
            resultados = [
                InlineQueryResultArticle(
                    id=nota.id,
                    title=nota.titulo,
                    description=nota.texto,
                    input_message_content=InputTextMessageContent(
                        message_text=textos.nota.format(
                            escape(nota.titulo), escape(nota.texto)
                        ),
                        parse_mode="HTML",
                    ),
                    reply_markup=menu_nota(nota.id),
                )
                for nota in notas
            ]
        else:
            resultados = [
                InlineQueryResultArticle(
                    id="sem_notas",
                    title=textos.sem_notas,
                    input_message_content=InputTextMessageContent(
                        message_text=textos.sem_notas
                    ),
                )
            ]
        bot.answer_inline_query(
            inline_query_id=cst.id, results=resultados, cache_time=1, is_personal=True
        )
    except Exception as ex:
        erros.analisar_erro(req=cst, bot=bot, ex=ex)

from telebot import TeleBot
from telebot.types import (
    Message,
    CallbackQuery,
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
    ReplyKeyboardRemove,
)

import exceptions
import textos


def analisar_erro(
    req: Message | CallbackQuery | InlineQuery, bot: TeleBot, ex: Exception
) -> None:
    if isinstance(ex, exceptions.ErroGenerico) or isinstance(
        ex, exceptions.ErroAutenticacao
    ):
        if isinstance(req, Message):
            bot.send_message(
                chat_id=req.from_user.id,
                text=ex.msg,
                reply_markup=ReplyKeyboardRemove(),
            )
        elif isinstance(req, CallbackQuery):
            bot.answer_callback_query(
                callback_query_id=req.id, text=ex.msg, show_alert=True
            )
        else:
            resultados = [
                InlineQueryResultArticle(
                    id=ex.msg,
                    title=ex.msg,
                    input_message_content=InputTextMessageContent(message_text=ex.msg),
                )
            ]
            bot.answer_inline_query(
                inline_query_id=req.id,
                results=resultados,
                cache_time=1,
                is_personal=True,
            )
    else:
        bot.send_message(
            chat_id=req.from_user.id,
            text=textos.erro_inesperado,
            reply_markup=ReplyKeyboardRemove(),
        )

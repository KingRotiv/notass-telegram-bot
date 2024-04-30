import logging

import telebot
from telebot.types import Message, ReplyKeyboardRemove, BotCommand
from telebot.storage import StateMemoryStorage
from telebot.custom_filters import StateFilter, TextMatchFilter

import config
import textos
import botoes
from plugins import start
from plugins import obter_notas
from plugins import criar_nota
from plugins import editar_nota
from plugins import deletar_nota


bot = telebot.TeleBot(
    token=config.TOKEN, state_storage=StateMemoryStorage(), parse_mode="HTML"
)
bot.set_my_commands(commands=[BotCommand("start", "Iniciar o bot")])


# Outros
@bot.message_handler(state="*", text=botoes.cancelar)
def state_cancelar(msg: Message) -> None:
    bot.delete_state(user_id=msg.from_user.id)
    bot.send_message(
        chat_id=msg.from_user.id,
        text=textos.processo_cancelado,
        reply_markup=ReplyKeyboardRemove(),
    )


# Start
bot.register_message_handler(
    callback=start.comando_start, commands=["start"], pass_bot=True
)
bot.register_callback_query_handler(
    callback=start.comando_start,
    func=lambda rsp: rsp.data == "#start",
    pass_bot=True,
)

# Editar nota
bot.register_callback_query_handler(
    callback=editar_nota.resposta_editar_nota,
    func=lambda rsp: rsp.data.startswith("#editar_nota"),
    pass_bot=True,
)
bot.register_message_handler(
    callback=editar_nota.etapa_escolher_editar_nota,
    state=editar_nota.EtapaEditarNota.escolher,
    pass_bot=True,
)
bot.register_message_handler(
    callback=editar_nota.etapa_titulo_editar_nota,
    state=editar_nota.EtapaEditarNota.titulo,
    pass_bot=True,
)
bot.register_message_handler(
    callback=editar_nota.etapa_texto_editar_nota,
    state=editar_nota.EtapaEditarNota.texto,
    pass_bot=True,
)

# Criar nota
bot.register_callback_query_handler(
    callback=criar_nota.resposta_criar_nota,
    func=lambda rsp: rsp.data == "#criar_nota",
    pass_bot=True,
)
bot.register_message_handler(
    callback=criar_nota.etapa_escolher_criar_nota,
    state=criar_nota.EtapaNovaNota.escolher,
    pass_bot=True,
)
bot.register_message_handler(
    callback=criar_nota.etapa_titulo_criar_nota,
    state=criar_nota.EtapaNovaNota.titulo,
    pass_bot=True,
)
bot.register_message_handler(
    callback=criar_nota.etapa_texto_criar_nota,
    state=criar_nota.EtapaNovaNota.texto,
    pass_bot=True,
)

# Obter notas
bot.register_inline_handler(
    callback=obter_notas.consulta_obter_notas,
    func=lambda _: True,
    pass_bot=True,
)

# Deletar nota
bot.register_callback_query_handler(
    callback=deletar_nota.resposta_deletar_nota,
    func=lambda rsp: rsp.data.startswith("#deletar_nota"),
    pass_bot=True,
)
bot.register_message_handler(
    callback=deletar_nota.etapa_escolher_deletar_nota,
    state=deletar_nota.EtapaDeletarNota.escolher,
    pass_bot=True,
)

bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(TextMatchFilter())


if __name__ == "__main__":
    if config.DEBUG:
        telebot.logger.setLevel(logging.DEBUG)
    bot.infinity_polling()

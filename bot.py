from pyChatGPT import ChatGPT
import toml
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_reply(ques):
    global api
    return api.send_message(ques)


def load_conf(filePath):
    file = toml.load(filePath)
    settings = file['configs']
    return settings['bot_token'], settings['cookie']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Chatgppt机器人")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_reply(update.message.text)['message']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


if __name__ == '__main__':
    bot_token, cookie = load_conf("conf.toml")
    api = ChatGPT(cookie)  # specify proxy

    proxy_url = 'http://127.0.0.1:10809'
    application = ApplicationBuilder().token(bot_token).proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()
    # application = ApplicationBuilder().token(bot_token).proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()

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
    return settings['bot_token'], settings['cookie'], settings['proxy_url']


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="""
            Chatgppt机器人。\n
            可用命令如下：\n
                /reset -- 重置会话\n
                /refresh -- 刷新会话页面（尽量别用）\n
                /clear -- 清除所有会话\n
            """
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = get_reply(update.message.text)['message']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global api
    api.reset_conversation()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="重置对话")


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global api
    api.clear_conversations()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="清除对话")


async def refresh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global api
    api.refresh_chat_page()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="刷新交谈页面")


if __name__ == '__main__':
    bot_token, cookie, proxy_url = load_conf("conf.toml")
    api = ChatGPT(cookie)  # specify proxy

    # proxy_url = 'http://127.0.0.1:10809'

    if len(proxy_url.strip()) == 0:
        application = ApplicationBuilder().token(bot_token).build()
    else:
        logging.info("Proxy opened")
        application = ApplicationBuilder().token(bot_token).proxy_url(proxy_url).get_updates_proxy_url(proxy_url).build()

    # application = ApplicationBuilder().token(bot_token).build()

    start_handler = CommandHandler('start', start)
    reset_handler = CommandHandler('reset', reset)
    clear_handler = CommandHandler('clear', clear)
    refresh_handler = CommandHandler('refresh', refresh)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)

    application.add_handler(start_handler)
    application.add_handler(echo_handler)
    application.add_handler(reset_handler)
    application.add_handler(clear_handler)
    application.add_handler(refresh_handler)

    application.run_polling()

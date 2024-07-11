# import logging
import os
from datetime import datetime
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
)

TOKEN: str = ""  # Bot token
LOGSPATH: str = "logs"  # Directory folder for logs

# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )


def writedata(path: str, data: str, end="\n"):
    with open(path, "r", encoding="UTF-8") as file:
        data_ = file.read()
    with open(path, "w", encoding="UTF-8") as file2:
        file2.write(data_ + data + end)


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
    if update.message is not None:
        chatid = update.message.chat.id
        message: str = (
            f"[{datetime.strftime(update.message.date, '%Y-%m-%d %H:%M:%S')}] @{update.message.from_user.username} ({update.message.from_user.id}) IN BOT DM: \"{update.message.text}\""
        )
        logpath = f"{LOGSPATH}\\botdms\\{chatid}.txt"
        if f"{chatid}.txt" not in os.listdir(f"{LOGSPATH}\\botdms\\"):
            with open(f"{LOGSPATH}\\botdms\\{chatid}.txt", "x"):
                pass
        logpath = f"{LOGSPATH}\\botdms\\{chatid}.txt"
    else:
        chatid = update.business_message.chat.id
        message: str = (
            f"[{datetime.strftime(update.business_message.date, '%Y-%m-%d %H:%M:%S')}] @{update.business_message.from_user.username} ({update.business_message.from_user.id}) IN @{update.business_message.chat.username} ({chatid}): \"{update.business_message.text}\""
        )
        if f"{chatid}.txt" not in os.listdir(f"{LOGSPATH}\\business\\"):
            with open(f"{LOGSPATH}\\business\\{chatid}.txt", "x"):
                pass
        logpath = f"{LOGSPATH}\\business\\{chatid}.txt"
    print(message)
    writedata(logpath, message)


if __name__ == "__main__":
    application = ApplicationBuilder().token(TOKEN).build()

    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)

    application.run_polling()

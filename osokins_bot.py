# https://docs.python-telegram-bot.org/en/v20.6/examples.html
# https://docs.python-telegram-bot.org/en/v20.6/examples.echobot.html

#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging, json

from datetime import datetime
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True, input_field_placeholder='This is my placeholder'),
    )
    print(user.first_name)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('/jerks - get exercises instructions for today')





async def jerks(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    secs = datetime.now().isocalendar().week * 10 + 140
    if secs > 240:
        secs = 240
    message = f'Зарядка на сегодня:\n\n' \
              f'Приседания:\nhttps://youtu.be/6A2V9Bu80J4?si=h-UUwQpZ1KRo4d7Q\n\n' \
              f'Планка: {str(secs // 60)}:{str(secs % 60)}'
    await update.message.reply_text(message)





def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    with open('bot_info_osokins_bot_toStepan.json', 'r', encoding='utf-8') as f:
        jdata = json.load(f)
    application = Application.builder().token(jdata['token']).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("jerks", jerks))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
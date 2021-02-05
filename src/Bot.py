#!/usr/bin/env python3
# -*- coding: 	UTF8 -*-
import os
import database
from os.path import join, dirname
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot_actions import start, add, get_all, delete, price_alarm, logger
from config import constants

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

database.Base.metadata.create_all(database.engine)

updater = Updater(token=os.environ.get("TELEGRAM_API_KEY"), use_context=True)
dispatcher = updater.dispatcher
jobs = updater.job_queue

start_handler = CommandHandler('start', start, pass_args=True)
dispatcher.add_handler(start_handler)

add_handler = CommandHandler('add', add, pass_args=True)
dispatcher.add_handler(add_handler)

all_handler = CommandHandler('all', get_all)
dispatcher.add_handler(all_handler)

delete_handler = CommandHandler('delete', delete,pass_args=True)
dispatcher.add_handler(delete_handler)

jobs.run_repeating(price_alarm, interval = constants.TIME_BETWEEN_PRICE_CHECKS_IN_SECS, first = constants.TIME_BEGIN_PRICE_CHEKING_IN_SECS)

updater.start_polling()

logger.info("Bot is started!")
#!/usr/bin/env python3
# -*- coding: 	UTF8 -*-
import os, sys, database
from os.path import join, dirname
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler
from bot_actions import start, add, get_all, delete, price_alarm, logger
from config import constants

load_dotenv('.env')

database.Base.metadata.create_all(database.engine)
api_key = os.environ.get("TELEGRAM_API_KEY")
if api_key == "" or api_key is None:
    print("Telegram api key not found. Did you add api to the environment?")
    sys.exit()
updater = Updater(token=api_key, use_context=True)
dispatcher = updater.dispatcher
jobs = updater.job_queue

start_handler = CommandHandler('start', start, pass_args=True)
dispatcher.add_handler(start_handler)

# 
add_handler = CommandHandler('add', add, pass_args=True)
dispatcher.add_handler(add_handler)

all_handler = CommandHandler('all', get_all)
dispatcher.add_handler(all_handler)

delete_handler = CommandHandler('delete', delete,pass_args=True)
dispatcher.add_handler(delete_handler)

# jobs.run_repeating(price_alarm, interval = constants.TIME_BETWEEN_PRICE_CHECKS_IN_SECS, first = constants.TIME_BEGIN_PRICE_CHEKING_IN_SECS)

updater.start_polling()

logger.info("Bot is started!")
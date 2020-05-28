#!/usr/bin/env python3
# -*- coding: 	UTF8 -*-
import sys
import os
import logging
import time
from random import random
from telegram.ext import Updater, CommandHandler
from telegram import ParseMode
from Auth import Auth
from Product import Product
from Amazon import Amazon
from bot_config import configure
from selenium_helper import get_driver
from config import constants, messages

driver = get_driver()
logger = configure()
auth = Auth(logger)
product = Product(logger)
amazon = Amazon(logger, driver) 

def start(update, context):
	try:
		username = update.message.chat.username
		logger.warning("User %s is trying to login.", username)
		if(auth.login(username,context.args[0])):
			auth.add_chat_id_to_user(update.message.chat.username,update.message.chat_id)
			msg="Hi " + username + "! Welcome!"
			logger.warning("User %s has successfully logged in.", username)
			context.bot.send_message(chat_id=update.message.chat_id, text=msg)
		else:
			context.bot.send_message(chat_id=update.message.chat_id,text=FAILED_LOGIN_MESSAGE)
	except Exception as e:
		logger.error(e.msg)
		context.bot.send_message(chat_id=update.message.chat_id,text=FAILED_LOGIN_MESSAGE)	

def add(update, context):
	try:
		if(auth.check_chat_id(update.message.chat_id)):
			args = context.args
			context.bot.send_message(chat_id = update.message.chat_id, text = "Adding product, please wait...")
			current = amazon.get_price_with_id(args[0])
			result = product.add_product(args[0],current,args[1],args[2],args[3])
			if result.acknowledged:
				context.bot.send_message(chat_id = update.message.chat_id, text = "Product added correctly.")
			else: 
				context.bot.send_message(chat_id = update.message.chat_id, text = "There's been a problem adding the product")
		else:
			context.bot.send_message(chat_id = update.message.chat_id, text = messages.NOT_LOGGED_ERROR_MESSAGE)
	except expression as identifier:
		logger.error(e)
		context.bot.send_message(chat_id = update.message.chat_id,text = messages.UNKNOWN_ERROR_MESSAGE)


def all(update, context):	
	try:
		if(auth.check_chat_id(update.message.chat_id)):
			result = [i for i in product.get_all_products()]
			if result != None and len(result)>0:
				msg=""
				for i in result:
					msg += ("<b><u>" + i["name"] + "</u></b>\n")
					msg += ("\t - <b>ID interno</b>: " + str(i["_id"]) + "\n")
					msg += ("\t - <b>ID Amazon</b>: " + i["amazon_id"] + "\n")
					msg += ("\t - <b>Aviso</b>: " + str(i["warning"]) + "\n")
					msg += ("\t - <b>Diferencia</b>: " + str(i["delta"]) + "\n") 
					msg += ("\t - <b>Current</b>: " + str(i["current"]) + "\n") 
					msg += ("\t - <b>Lowest</b>: " + str(i["lowest"]) + "\n") 
				context.bot.send_message(chat_id=update.message.chat_id, text=msg, parse_mode=ParseMode.HTML)
			elif len(result) == 0:
				context.bot.send_message(chat_id=update.message.chat_id,text="There are no items! Use /add to add one.")
			else: 
				context.bot.send_message(chat_id=update.message.chat_id,text="There's been a problem getting all items.")
		else:
			logger.warning("The user %s has tried to use the bot without loggin", update.message.chat.username)
			context.bot.send_message(chat_id=update.message.chat_id,text = messages.NOT_LOGGED_ERROR_MESSAGE)
	except Exception as e:
		logger.error(e)
		context.bot.send_message(chat_id=update.message.chat_id, text = messages.UNKNOWN_ERROR_MESSAGE)


def delete(update, context):
	try:
		if(auth.check_chat_id(update.message.chat_id)):
			res=product.delete_product(context.args[0])
			if res == 1:
				context.bot.send_message(chat_id = update.message.chat_id, text = "Product deleted.")
			else: 
				context.bot.send_message(chat_id = update.message.chat_id,text = "There's been a problem deleting the item.")
		else:
			context.bot.send_message(chat_id = update.message.chat_id,text = messages.NOT_LOGGED_ERROR_MESSAGE)
	except Exception as e:
		logger.error(e)
		context.bot.send_message(chat_id=update.message.chat_id, text = messages.UNKNOWN_ERROR_MESSAGE)


def price_alarm(context):
	try:
		logger.info("Beginning price check.")
		for p in product.get_all_products():
			amazon_price = amazon.get_price_with_id(p["amazon_id"])
			if(amazon_price < float(p["current"])):
				logger.info(str(amazon_price < float(p["warning"])))
				if amazon_price < float(p["lowest"]):
					msg = 'The price of ' + p["name"] + ' is the lowest! It\'s now <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p["amazon_id"] + '">Check it out!</a>'
					product.update_lowest_price(p["_id"], amazon_price)
					user_chats_ids = auth.get_all_chat_id()
					for user_chat_id in user_chats_ids:
						context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
				elif amazon_price < float(p["warning"]):
					msg = 'The price of ' + p["name"] + ' has reached the warning! It\'s now <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p["amazon_id"] + '">Check it out!</a>'
					user_chats_ids = auth.get_all_chat_id()
					for user_chat_id in user_chats_ids:
						context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
				elif float(p["delta"]) < float(p["current"]) - amazon_price:
					msg = 'The price of ' + p["name"] + ' is now at <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p["amazon_id"] + '">Check it out!</a>'
					user_chats_ids = auth.get_all_chat_id()
					for user_chat_id in user_chats_ids:
						context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
			product.update_current_price(p["_id"], amazon_price)
			sleep_time = constants.WAIT_TIME_BETWEEN_PRODUCTS_IN_MS + (random() * 100)
			logger.info("Sleeping " + str(sleep_time) + " miliseconds")
			time.sleep(sleep_time)
		logger.info("Finished price check.")
	except Exception as e:
		logger.error(e)

updater = Updater(token=os.environ.get("TELEGRAM_API_KEY"), use_context=True)
dispatcher = updater.dispatcher
jobs = updater.job_queue

start_handler = CommandHandler('start', start, pass_args=True)
dispatcher.add_handler(start_handler)

add_handler = CommandHandler('add', add, pass_args=True)
dispatcher.add_handler(add_handler)

all_handler = CommandHandler('all', all)
dispatcher.add_handler(all_handler)

delete_handler = CommandHandler('delete', delete,pass_args=True)
dispatcher.add_handler(delete_handler)

jobs.run_repeating(price_alarm, interval = constants.TIME_BETWEEN_PRICE_CHECKS_IN_SECS, first = constants.TIME_BEGIN_PRICE_CHEKING_IN_SECS)

updater.start_polling()

logger.info("Bot is started!")
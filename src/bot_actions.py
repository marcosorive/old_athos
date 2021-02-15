import time
from User import User, login, add_chat_id_to_user, check_chat_id, get_all_chat_ids
from Product import Product, add_product, get_all_products, delete_product, update_lowest_price, update_current_price
from Selenium import Selenium
from config import constants, messages
from logger import logger
from telegram import ParseMode
from utils import get_domain_from_url
from Store.Store_Factory import get_store
from random import random
import traceback

selenium = Selenium()

'''

'''
def start(update, context):
    try:
        username = update.effective_chat.username
        chat_id = update.effective_chat.id
        logger.warning("User %s is trying to login.", username)
        if(login(logger, username, context.args[0])):
            add_chat_id_to_user(logger, username, chat_id)
            logger.info("User %s has successfully logged in.", username)
            context.bot.send_message(chat_id = chat_id, text = f'Hi {username},  Welcome!')
        else:
            context.bot.send_message(chat_id = chat_id, text = "Wrong password")
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id = chat_id, text = messages.FAILED_LOGIN_MESSAGE)

'''
Adds a product to the database.
The arguments in order should be url, name, warning and delta.
'''
def add(update, context):
    chat_id = update.effective_chat.id
    try:
        if(check_chat_id(chat_id)):
            args = context.args
            context.bot.send_message(chat_id = chat_id, text = "Adding product, please wait...")
            driver = selenium.setup()
            store_name = get_domain_from_url(args[0])
            store = get_store(store_name, driver, logger)
            gotCurrent, current = store.get_price_from_url(args[0])
            if gotCurrent:
                # name, store, url, current_price, warning, delta
                add_product(args[1],store_name,args[0],current,args[2],args[3])
                context.bot.send_message(chat_id = chat_id, text = "Product added correctly.")
            else: 
                context.bot.send_message(chat_id = chat_id, text = messages.UNABLE_GET_PRICE_MESSAGE)
            selenium.dispose()
        else:
            logger.warning("The user %s has tried to use the bot without loggin", update.message.chat.username)
            context.bot.send_message(chat_id = chat_id, text = messages.NOT_LOGGED_ERROR_MESSAGE)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id = chat_id,text = messages.UNKNOWN_ERROR_MESSAGE)


def get_all(update, context):
    chat_id = update.effective_chat.id
    try:
        if(check_chat_id(chat_id)):
            result = get_all_products()
            if result != None and len(result)>0:
                msg=""
                for i in result:
                    msg += ("<b><u>" + i.name + "</u></b>\n")
                    msg += ("\t - <b>ID interno</b>: " + str(i.id) + "\n")
                    msg += ("\t - <b>Warning:</b>: " + str(i.warning) + "\n")
                    msg += ("\t - <b>Delta: </b>: " + str(i.delta) + "\n") 
                    msg += ("\t - <b>Current</b>: " + str(i.current) + "\n") 
                    msg += ("\t - <b>Lowest:</b>: " + str(i.lowest) + "\n") 
                context.bot.send_message(chat_id=chat_id, text=msg, parse_mode=ParseMode.HTML)
            elif len(result) == 0:
                context.bot.send_message(chat_id=chat_id,text="There are no items! Use /add to add one.")
            else: 
                context.bot.send_message(chat_id=chat_id,text="There's been a problem getting all items.")
        else:
            logger.warning("The user %s has tried to use the bot without loggin", update.message.chat.username)
            context.bot.send_message(chat_id=chat_id,text = messages.NOT_LOGGED_ERROR_MESSAGE)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=chat_id, text = messages.UNKNOWN_ERROR_MESSAGE)


def delete(update, context):
    chat_id = update.effective_chat.id
    try:
        if(check_chat_id(chat_id)):
            delete_product(context.args[0])
            context.bot.send_message(chat_id = chat_id, text = "Product deleted.")
        else:
            logger.warning("The user %s has tried to use the bot without loggin", update.message.chat.username)
            context.bot.send_message(chat_id = chat_id,text = messages.NOT_LOGGED_ERROR_MESSAGE)
    except Exception as e:
        logger.error(e)
        context.bot.send_message(chat_id=chat_id, text = messages.UNKNOWN_ERROR_MESSAGE)


def price_alarm(context):
    try:
        logger.info("Beginning price check.")
        not_retrieved_products = []
        user_chats_ids = get_all_chat_ids()
        for p in get_all_products():
            driver = selenium.setup()
            store = get_store(p.store,driver, logger)
            is_retrieved, remote_price = store.get_price_from_url(p.url)
            selenium.dispose()
            if not is_retrieved:
                logger.info("Could not get the price for %s with id %d", p.name, p.id)
                not_retrieved_products.append(p)
                continue
            if(remote_price < float(p.current)):
                logger.info(str(remote_price < float(p.warning)))
                if remote_price < float(p.lowest):
                    update_lowest_price(p.id, remote_price)
                    msg = 'The price of ' + p.name + ' is the lowest! It\'s now <b>' + str(remote_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
                elif remote_price < float(p.warning):
                    msg = 'The price of ' + p.name + ' has reached the warning! It\'s now <b>' + str(remote_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
                elif float(p.delta) < float(p.current) - remote_price:
                    msg = 'The price of ' + p.name + ' is now at <b>' + str(remote_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
            update_current_price(p.id, remote_price)
            sleep_time = constants.WAIT_TIME_BETWEEN_PRODUCTS_IN_S + (random()*10)
            logger.info("Sleeping " + str(sleep_time) + " seconds")
            time.sleep(sleep_time)
        logger.info("Finished price check.")
        final_msg = get_final_message(not_retrieved_products)
        for user_chat_id in user_chats_ids:
            context.bot.send_message(chat_id = user_chat_id, text =  final_msg, parse_mode = ParseMode.HTML)
    except Exception as e:
        logger.error(traceback.format_exception())
        

def get_final_message(not_retrieved_products):

    if len(not_retrieved_products) == 0:
        return 'Finished updating products.'
    else:
        msg = 'Finished updating products. The following products could not be updated:\n'
        for p in not_retrieved_products:
            msg += f'- {p.name} \n'
        return msg
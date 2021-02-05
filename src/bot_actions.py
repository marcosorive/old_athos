import time
from User import User, login, add_chat_id_to_user, check_chat_id, get_all_chat_ids
from Product import Product, add_product, get_all_products, delete_product, update_lowest_price, update_current_price
from Amazon import Amazon
from Selenium import Selenium
from config import constants, messages
from logger import logger
from telegram import ParseMode
from utils import get_domain_from_url

selenium = Selenium()
amazon = Amazon(logger) 

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
The arguments in order should be amazon_id, name, warning and delta.
'''
def add(update, context):
    chat_id = update.effective_chat.id
    try:
        if(check_chat_id(chat_id)):
            args = context.args
            context.bot.send_message(chat_id = chat_id, text = "Adding product, please wait...")
            driver = selenium.setup()
            # current = amazon.get_price_with_id(args[0], driver)
            store = get_domain_from_url(args[0])
            # add_product(args[0],current,args[1],args[2],args[3])
            context.bot.send_message(chat_id = chat_id, text = "Product added correctly. Store is " + store)
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
                    msg += ("\t - <b>ID Amazon</b>: " + i.amazon_id + "\n")
                    msg += ("\t - <b>Aviso</b>: " + str(i.warning) + "\n")
                    msg += ("\t - <b>Diferencia</b>: " + str(i.delta) + "\n") 
                    msg += ("\t - <b>Current</b>: " + str(i.current) + "\n") 
                    msg += ("\t - <b>Lowest</b>: " + str(i.lowest) + "\n") 
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
        for p in get_all_products():
            driver = selenium.setup()
            amazon_price = amazon.get_price_with_id(p.amazon_id, driver)
            selenium.dispose()
            if(amazon_price < float(p.current)):
                logger.info(str(amazon_price < float(p.warning)))
                if amazon_price < float(p.lowest):
                    update_lowest_price(p.id, amazon_price)
                    msg = 'The price of ' + p.name + ' is the lowest! It\'s now <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    user_chats_ids = get_all_chat_ids
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
                elif amazon_price < float(p.warning):
                    user_chats_ids = get_all_chat_ids
                    msg = 'The price of ' + p.name + ' has reached the warning! It\'s now <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
                elif float(p.delta) < float(p.current) - amazon_price:
                    user_chats_ids = get_all_chat_ids
                    msg = 'The price of ' + p.name + ' is now at <b>' + str(amazon_price) +  '</b>. <a href="https://amazon.es/dp/' + p.amazon_id + '">Check it out!</a>'
                    for user_chat_id in user_chats_ids:
                        context.bot.send_message(chat_id = user_chat_id, text = msg, parse_mode = ParseMode.HTML)
            update_current_price(p.id, amazon_price)
            sleep_time = constants.WAIT_TIME_BETWEEN_PRODUCTS_IN_MS + (random() * 100)
            logger.info("Sleeping " + str(sleep_time) + " miliseconds")
            time.sleep(sleep_time)
        logger.info("Finished price check.")
    except Exception as e:
        logger.error(e)
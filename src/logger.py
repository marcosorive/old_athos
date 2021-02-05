import logging

def configure_logger():
    logger = logging.getLogger("bot_logger")
    logging.getLogger().setLevel(logging.INFO)
    try:
        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler('bot.log')
        c_handler.setLevel(logging.DEBUG)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters and add it to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)
    except Exception as e:
        print("There was a problem creating logger: " + e)
    return logger

logger = configure_logger()
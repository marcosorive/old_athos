# Athos

Athos is a telegram bot that compares prices from diferents stores and notifies the user if the price changes.

# About ❓
- This bot is developed with the idea of being used in a raspberry pi, but it can be deployed in any cloud environment, of course.
- Usually telegram bots are accessible by everyone using the app. This bot is built to be different. The reason is simple: web scrapping is hard and you have to be considerate with the website. If I allow any user to add products to be tracked, it would almost look like I'm DDosing the stores to get the prices.
- For this reason, the bot is meant to be replicated and only be used by a small amount of people. That's why it used an authentication mechanism.

# Requirements 🛠
- Python 3.7.
- Pipenv.
- SQLite. (Since I use sqlalchemy you could change the DBMS little work.)
- A Telegram bot API key. (Obtained when you create the bot with [botfahter](https://core.telegram.org/bots#6-botfather))

# Installation 💻
- Clone the repository with `git clone` in the folder you want to install
- If you are using a debian based OS can install it running the install.sh script. Using other OS, install the dependencies mentioned above and run `pipenv install`.
- Done!

# Configuration ⚙️
- Create .env file (or add env variable) with a variable called: TELEGRAM_API_KEY. This variable should contains the telegram api key obtained when creating the bot.
- You can (optionally) edit the config files in src/config/constants. The default will check prices every hour (3600 seconds) and wait 1 second between products.
- Add a user with the script src/database_utils/add_user.py. Like this: `python ./src/database_utils/add_user.py johndoe s3cr3t_p455w0rd`

# Launch 🚀
- Run `python ./src/Bot.py`
- Done!
- If you want it to launch at system startup follow this [Stack overflow answer](https://stackoverflow.com/questions/12973777/how-to-run-a-shell-script-at-startup). 

# How to use 🤖
- First, add a user with the method mentioned in the configuration paragraph.
- If you added the user correctly, you can **log in** in telegram using `/start s3cr3t_p455w0rd`. You just need to do this once. After that, the bot will save your chat ID and will never ask for password again. After that, please **DELETE THE PASSWORD MESSAGE**. If you don't, every person that access your telegram app will see the password. Also, **avoid common password and don't reuse them**
- After that you can **add a product with** with /add like: `/add url productName warningPrice deltaWarning`. 
    - The url should be the url of the product. Plain and simple.
    - productName is the name you want to product to be identified by.
    - warningPrice is the price you want to be notified if the product reaches that price.
    - deltaWarning is the difference in price you want to be notified by. (If it's 5 the product price should lower 5 or more. Dollars, euros, gbp... whatever.)
- Use `/all` to get a list of all the products the bot is following.
- Use `/delete` to delete a product using the internal ID showed with `/all`. Example: `/delete 5ec69e815ac457c387e67291`


# Supported stores 🏪

Right now Athos only supports 1 store:

- https://pccomponentes.com

The list will of course grow in the future :)
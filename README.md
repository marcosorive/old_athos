# WORK IN PROGRESS
# AMPI (AMazon Price Inspector) 

AMPI (AMazon Princes Inspector) is a telegram bot that compares amazon prices and notifies the user when there are changes!

# About ❓
- Usually telegram bots are accessible by everyone using the app, the nature of the bot made think of a way to stop people from adding products to tracked.
- Because this bot uses web scrapping to obtain the prices, amazon will ban the IP address of the bot after a lot of requests.

# Requirements 🛠
- Python 3.7.
- Pipenv.
- MongoDB.
- A Telegram bot API key. (Obtained when you create the bot with [botfahter](https://core.telegram.org/bots#6-botfather))

# Installation 💻
- Clone the repository with `git clone` in the folder you want to install
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
- If you added the user correctly, **log in** using `/start s3cr3t_p455w0rd`. You just need to do this once. After that, the bot will save your chat ID and will never ask for password again. After that, plesae **DELETE THE PASSWORD MESSAGE**. If you don't, every person that access your telegram app will see the password. Also, **avoid common password and don't reuse them**
- After that you can **add a product with** with /add like: `/add amazonID productName warningPrice deltaWarning`. 
    - AmazonID is the id in the amazon url. It usually goes after the /dp/ element. For example, in amazon spain the ID for echo dot is B07PHPXHQS (https://www.amazon.es/echo-dot-3-generacion-altavoz-inteligente-con-alexa-tela-de-color-antracita/dp/B07PHPXHQS)
    - Please make sure that there are no blank spaces in the name, ID, warning o delta. It will be interpreted by the bot as a new parameter.
- Use `/all` to get a list of all the products the bot is following.
- Use `/delete` to delete a product using the internal ID showed with `/all`. Example: `/delete 5ec69e815ac457c387e67291`
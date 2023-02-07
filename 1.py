import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai
import configparser
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Read config
config = configparser.ConfigParser()
config.read('config.cfg')

# Set the OpenAI API key
openai.api_key = config['DEFAULT']['openai_api_key']

# Define a function to be called when the /start command is issued
def start(update, context):
    update.message.reply_text('Hi! I am an AI assistant powered by OpenAI. You can ask me anything and I will do my best to help you.')


def savedata(name, text, response):
    f = open("{}-{}.txt".format(name, time.strftime("%Y%m%d")), 
                "a")
    f.write({text}; \n{response}\n\n")
    f.close()

# Define a function to be called when a message is received
def message(update, context):
    # Get the message text and user's name
    text = update.message.text
    name = update.message.from_user.first_name

    # Use the OpenAI chat API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"{name}: {text}\n\nAssistant:",
        max_tokens=1024,
        temperature=0.7,
    ).choices[0].text

    savedata(name, text, response)
    # Send the response to the user
    update.message.reply_text(response)





def main():
    # Create an Updater object
    updater = Updater(config['DEFAULT']['telegram_api_key'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the start command handler
    dp.add_handler(CommandHandler("start", start))

    # Add the message handler
    dp.add_handler(MessageHandler(Filters.text, message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
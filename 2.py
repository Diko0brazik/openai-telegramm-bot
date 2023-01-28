import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import openai
from telegram import InlineKeyboardButton, InlineKeyboardMarkup



# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)



#settings
engine="text-davinci-003"
max_tokens=1024
temperature=0.7
telegrambot_apikey = 

# Set the OpenAI API key
openai.api_key = 

# Define a function to be called when the /start command is issued
def start(update, context):
    update.message.reply_text('Hi! I am an AI assistant powered by OpenAI. You can ask me anything and I will do my best to help you.')

def settings(update, context):
    # create the inline keyboard
    keyboard = [[InlineKeyboardButton("setup temprature", callback_data='setup temp'),
                InlineKeyboardButton("setup max tokens", callback_data='setup max tokens')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # send the message with the inline keyboard
    message = "select setup"
    update.message.reply_text(message, reply_markup=reply_markup)

def set_temprature(update, context):
    # create the inline keyboard
    keyboard = [[InlineKeyboardButton("temprature 0.1", callback_data='temp_01'),
                InlineKeyboardButton("temprature 0.3", callback_data='temp_03')],
                [
                InlineKeyboardButton("temprature 0.5", callback_data='temp_05'),
                InlineKeyboardButton("temprature 0.7", callback_data='temp_07'),
                InlineKeyboardButton("temprature 0.9", callback_data='temp_09')]
                ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # send the message with the inline keyboard
    message = "temprature now {} Please select a new temprature: ".format(temperature)
    update.message.reply_text(message, reply_markup=reply_markup)

def callback_handler(update, context):
    query = update.callback_query
    data = query.data
    global temperature
    
    # Temprature
    if data == 'temp_01':
        temperature = 0.1
        message = "temprature has been set to 0.1"
    elif data == 'temp_03':
        #global temperature
        temperature = 0.3
        message = "temprature has been set to 0.3"
    elif data == 'temp_05':
        #global temperature
        temperature = 0.5
        message = "temprature has been set to 0.5"
    elif data == 'temp_07':
        #global temperature
        temperature = 0.7
        message = "temprature has been set to 0.7"
    elif data == 'temp_09':
        #global temperature
        temperature = 0.9
        message = "temprature has been set to 0.9"

    #max tokens
    elif data == 'tokens 1024':
        
        message = "max tokens set to 1024 NOT"

    # Setup
    elif data == 
    query.edit_message_text(text=message)


# Define a function to be called when a message is received
def message(update, context):
    # Get the message text and user's name
    text = update.message.text
    name = update.message.from_user.first_name

    # Use the OpenAI chat API to generate a response
    response = openai.Completion.create(
        engine=engine,
        prompt=f"{name}: {text}\n\nAssistant:",
        max_tokens=max_tokens,
        temperature=temperature,
    ).choices[0].text

    # Send the response to the user
    update.message.reply_text(response)


def main():
    # Create an Updater object
    updater = Updater(telegrambot_apikey, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the start command handler
    dp.add_handler(CommandHandler("start", start))
    
    dp.add_handler(CommandHandler('set_temprature', set_temprature))

    # Add the message handler
    dp.add_handler(MessageHandler(Filters.text, message))

    # create the callback query handler    
    dp.add_handler(CallbackQueryHandler(callback_handler))

    commands = {
    'start': 'Start the bot',
    'set_temprature': 'set_temprature',
    }
    
    #dispatcher.add_handler(HelpCommand(command_attrs=commands))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
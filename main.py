import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Set Telegram bot token and GPT API URL directly
TELEGRAM_BOT_TOKEN = "6979206212:AAHTTpYUPhy5-g2_jj0csRcIP4Hc42vSs9M"
GPT_API_URL = "https://chatgpt.apinepdev.workers.dev"

# Define /gpt command handler
def gpt_command(update: Update, context: CallbackContext) -> None:
    # Get the text after /gpt command
    query = context.args if context.args else None

    if query:
        # Join the query into a single string
        prompt = ' '.join(query)

        # Make a request to GPT API
        response = requests.get(f"{GPT_API_URL}/?question={prompt}")

        if response.status_code == 200:
            # Extract the answer from the API response
            api_response = response.json()
            
            # Check if "join" key is present and remove it
            if "join" in api_response:
                del api_response["join"]

            answer = api_response.get("answer", "No answer received from GPT.")
            
            # Send the answer back to the user
            update.message.reply_text(answer)
        else:
            update.message.reply_text("Error communicating with GPT API.")
    else:
        update.message.reply_text("Please provide a prompt after /gpt command.")

def main() -> None:
    # Create the Updater and pass it your bot's token
    updater = Updater(token=TELEGRAM_BOT_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register /gpt command handler
    dispatcher.add_handler(CommandHandler("gpt", gpt_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()

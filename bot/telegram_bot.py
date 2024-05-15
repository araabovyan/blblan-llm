from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext
import telegram.ext.filters as filters
import requests
import json
import os

TOKEN = os.getenv('TELEGRAM_TOKEN')

os.makedirs('bot_sessions', exist_ok=True)

def save_sessions():
    """Save the session data to a JSON file."""
    with open('bot_sessions/sessions.json', 'w') as f:
        json.dump(user_sessions, f)

def load_sessions():
    """Load the session data from a JSON file."""
    try:
        with open('bot_sessions/sessions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Dictionary to store conversation history for each user
user_sessions = load_sessions()

async def start(update: Update, context: CallbackContext) -> None:
    """Sends a welcome message and model selection options instructions when the command /start is issued."""
    user = update.effective_user
    welcome_message = (
        f'Hi {user.first_name}! 👋\n'
        "Welcome to our chatbot! Please choose your service level:\n\n"
        "Free - Basic responses.\n"
        "Paid - Advanced responses with deeper insights.\n"
    )
    keyboard = [['Free', 'Paid']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup,
    )

async def handle_model_choice(update: Update, context: CallbackContext) -> None:
    """Handles the user's model choice and saves it in the user session."""
    chat_id = update.message.chat_id
    model_choice = update.message.text.lower()
    user_sessions[chat_id] = {
        "model": "process_message1" if model_choice == "free" else "process_message2",
        "conversationID": str(chat_id)
    }
    save_sessions()

    # Inform user of the choice and invite to start chatting
    await update.message.reply_text(f"You have selected the {model_choice} model. Please start chatting!")


async def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message to the selected model server and return the processed response."""
    chat_id = update.message.chat_id
    user_text = update.message.text
    user_session = user_sessions.get(chat_id)
    print(f"User session before: {user_session}")

    # Check if user session exists and model is set
    if not user_session or "model" not in user_session:
        keyboard = [['Free', 'Paid']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Please choose your service level:\n\n"
            "Free - Basic responses.\n"
            "Paid - Advanced responses with deeper insights.",
            reply_markup=reply_markup
        )
        return
    print(f"User session after: {user_session}")

    endpoint = f'http://127.0.0.1:5000/{user_session["model"]}'

    data = {
        "userID": chat_id,
        "conversationID": user_session["conversationID"],
        "messageText": user_text,
    }

    try:
        full_response = requests.post(endpoint,
                                    headers={"Content-Type": "application/json"},
                                    data=json.dumps(data)).text
    except Exception as e:
        full_response = "Error in processing your message."
        print(f"Error: {str(e)}")

    await update.message.reply_text(full_response if full_response else "No response received from server.")


def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Regex('^(Free|Paid)$'), handle_model_choice))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling()

if __name__ == '__main__':
    main()

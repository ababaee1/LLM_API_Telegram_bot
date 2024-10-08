import os
import signal
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai  # Correct import

# Set up your API keys
TELEGRAM_TOKEN = 'XXXX' #please add your own Telegram token
OPENAI_API_KEY = 'XXXX' #please add your LLM API key (here we imported the OpenAI LLM)

# Set up OpenAI API key
openai.api_key = OPENAI_API_KEY  # Set the API key directly

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I'm a bot that can send your prompts to OpenAI's GPT model. "
        "Just send me a message and I'll reply with the AI's response."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        # Send the user's message to OpenAI
        response = openai.ChatCompletion.create(  # Correct method call
            model="gpt-3.5-turbo",  # Use "gpt-4" if you have access
            messages=[
                {"role": "user", "content": user_message}
            ]
        )

        ai_response = response['choices'][0]['message']['content'].strip()

        # Send the AI's response back to the user
        await update.message.reply_text(ai_response)
    except Exception as e:
        # Print the exception to the console for debugging
        print(f"An error occurred: {str(e)}")
        await update.message.reply_text(f"An error occurred: {str(e)}")

def main():
    # Set up the application
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Set up handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot started. Press Ctrl+C to stop.")
    application.run_polling()

if __name__ == '__main__':
    main()

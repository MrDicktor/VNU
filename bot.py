from idlelib import query
from dotenv import load_dotenv
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters,  ConversationHandler, CallbackQueryHandler
import pars

load_dotenv()
TOKEN = os.getenv("TOKEN")


async def start(update, context):
    await update.message.reply_text("Введіть назву групи")
    return 2



async def show_data(update, context):
    result = await pars.save_data(update, context)

    if result == 1:
        await update.message.reply_text(
            "Групу не знайдено або розкладу немає 😕\n\n"
            "Спробуйте ще раз. Введіть назву групи:"
        )
        return 2

    file_name = context.user_data["group"] + ".txt"
    with open(file_name, "r", encoding="utf-8") as f:
        file_content = f.read()

    await update.message.reply_text(file_content[:4000])

    return ConversationHandler.END



async def cancel(update, context):
    return ConversationHandler.END


def main():
    application = Application.builder().token(TOKEN).build()

    conversation = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_data)],
            4: [CallbackQueryHandler(cancel, pattern="cancel")],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True,
    )

    application.add_handler(conversation)
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()

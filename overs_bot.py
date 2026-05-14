import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# ========================
# НАСТРОЙКИ
# ========================
TOKEN = "8978334273:AAGFl5g-HFmUBl9Hi14vPdH2MEscRuKyWZU"
ADMIN_ID = 7720566946
GROUP_ID = -5167772662

# ========================
# ШАГИ АНКЕТЫ
# ========================
(
    NAME, COUNTRY,
    EDUCATION, SPECIALTY, CERTIFICATES,
    PROGRAM, LANGUAGE, DESIRED_SPECIALTY,
    BUDGET, WHEN, USERNAME
) = range(11)

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Привет! Это анкета для бесплатного разбора твоего профиля от Overs Study Abroad.\n\n"
        "Мы расскажем о твоих шансах на поступление.\n\n"
        "Давай начнём! Как тебя зовут?",
        reply_markup=ReplyKeyboardRemove()
    )
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("🌍 Из какой ты страны и города?")
    return COUNTRY

async def get_country(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["country"] = update.message.text
    keyboard = [["Школьник", "Бакалавр", "Магистр"]]
    await update.message.reply_text(
        "🎓 Какой у тебя уровень образования?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return EDUCATION

async def get_education(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["education"] = update.message.text
    await update.message.reply_text(
        "📚 Какая у тебя специальность или направление?",
        reply_markup=ReplyKeyboardRemove()
    )
    return SPECIALTY

async def get_specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["specialty"] = update.message.text
    await update.message.reply_text(
        "📜 Есть ли языковые сертификаты?\n"
        "(IELTS, TOPIK, TOEFL — если да, укажи уровень. Если нет — напиши «нет»)"
    )
    return CERTIFICATES

async def get_certificates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["certificates"] = update.message.text
    keyboard = [["Языковая школа", "Бакалавр", "Магистр"]]
    await update.message.reply_text(
        "🎯 Какую программу рассматриваешь?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return PROGRAM

async def get_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["program"] = update.message.text
    keyboard = [["Английский", "Корейский", "Оба"]]
    await update.message.reply_text(
        "🗣 На каком языке готов учиться?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return LANGUAGE

async def get_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["language"] = update.message.text
    await update.message.reply_text(
        "📖 Какая специальность тебя интересует за рубежом?",
        reply_markup=ReplyKeyboardRemove()
    )
    return DESIRED_SPECIALTY

async def get_desired_specialty(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["desired_specialty"] = update.message.text
    keyboard = [["до $5K", "Не ограничен", "Ищу стипендию"]]
    await update.message.reply_text(
        "💰 Какой бюджет на обучение в год?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return BUDGET

async def get_budget(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["budget"] = update.message.text
    keyboard = [["2026", "2027", "2028", "Пока не знаю"]]
    await update.message.reply_text(
        "📅 Когда планируешь поступать?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    )
    return WHEN

async def get_when(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["when"] = update.message.text
    await update.message.reply_text(
        "📩 Последний вопрос! Оставь свой Telegram username или номер телефона\n"
        "(например @username)"
    )
    return USERNAME

async def get_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["contact"] = update.message.text
    d = context.user_data

    message = (
        f"📋 *Новая заявка — Overs Study Abroad*\n\n"
        f"👤 *Имя:* {d.get('name')}\n"
        f"🌍 *Страна/город:* {d.get('country')}\n"
        f"🎓 *Образование:* {d.get('education')}\n"
        f"📚 *Специальность:* {d.get('specialty')}\n"
        f"📜 *Сертификаты:* {d.get('certificates')}\n\n"
        f"🎯 *Программа:* {d.get('program')}\n"
        f"🗣 *Язык обучения:* {d.get('language')}\n"
        f"📖 *Желаемая специальность:* {d.get('desired_specialty')}\n\n"
        f"💰 *Бюджет в год:* {d.get('budget')}\n"
        f"📅 *Когда поступать:* {d.get('when')}\n\n"
        f"📩 *Telegram:* {d.get('contact')}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="Markdown")
    await context.bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="Markdown")

    await update.message.reply_text(
        "✅ Отлично! Мы получили Вашу анкету и свяжемся в ближайшее время.\n\n"
        "Спасибо что выбрали Overs Study Abroad! 🎓🇰🇷",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Анкета отменена. Напиши /start чтобы начать заново.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

def main():
    app = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            COUNTRY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_country)],
            EDUCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_education)],
            SPECIALTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_specialty)],
            CERTIFICATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_certificates)],
            PROGRAM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_program)],
            LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_language)],
            DESIRED_SPECIALTY: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_desired_specialty)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_budget)],
            WHEN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_when)],
            USERNAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()

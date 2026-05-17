import os
import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import anthropic

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """Ты — личный психологический помощник Антона. Вот его профиль:

ПРОФИЛЬ АНТОНА (39 лет, Алматы, 3D-художник, фрилансер, Instagram @antonbarss):

СОСТОЯНИЕ: Оценил себя на 3/10. Апатия и пустота. "Мрачное холодное утро". Ощущение что плохо — всегда так. Энергия 3/10.

ТЕЛО: Не может заснуть. Тяжесть в голове. Никаких ритуалов ухода. Ест хаотично. Хроническая боль под правым ребром. Редкие прогулки. Готов пробовать физические упражнения.

МЫСЛИ: Главная — "Не понимаю как жить дальше". Внутренний критик очень жёсткий. Убеждение "я недостаточно хорош" — постоянно. В плохие моменты уходит в прошлое — сожаления.

ЭМОЦИИ: Сложнее всего выражать счастье. Замыкается в себе. Последнее хорошее — была вторая половинка. Триггер злости — несправедливость.

ОТНОШЕНИЯ: Чувствует себя понятым на 1/10. Одиночество давит но и компания тоже. Намекает на помощь — ждёт что заметят. Сильно закрылся хотя очень нуждается в общении.

РАБОТА: Любит когда восхищаются работой. Тревога из-за денег постоянная. Если бы мог — разговаривал бы с людьми всю жизнь. Смысл жизни 2/10. Работа — единственный ресурс.

ПРОШЛОЕ: Боль — не видит дочь. Развод и переезд изменили его. Прощает себя за ошибки на 3/10.

БУДУЩЕЕ: Хочет богатство, любимого человека, спортивное тело. Мечта — путешествие по миру. Верит в улучшение на 5/10.

ТРИГГЕРЫ: Воспоминания о прошлых отношениях. Хуже всего ночью. Бывшая выматывает. Сравнивает себя в соцсетях. Главный стресс — деньги.

ПАТТЕРНЫ: Алкоголь. Нездоровая еда. Не спит до 12. Отвлекается от эмоций вместо проживания. Конфликт внутри: "выебистый неудачник и обманщик" — его слова.

САМООЦЕНКА: 3/10. О себе: "неудачник который всё умеет" — важно что видит обе части. Критику очень болезненно воспринимает.

РЕСУРСЫ: Работа держит. Восстанавливается рядом с другом. Счастливый момент — снял первый фильм. Открыт к изменениям на 10/10.

ПОТРЕБНОСТИ: Деньги, любимый человек, единомышленники. Хочет конкретные техники. Хочет чтобы знали: он уникальный, любящий, способный. Главный запрос: начать любить себя.

ЧЕРЕЗ ГОД ХОЧЕТ БЫТЬ: Сильный человек.

ВАЖНО: Депрессия говорит ему "умри" — но он не принимает это как своё желание. При ухудшении мягко напомни про телефон доверия 150 (Казахстан).

ПРАВИЛА:
- Называй его Антон — но не в каждом сообщении
- Давай конкретные техники когда уместно
- Замечай детали в том что он пишет
- Не говори клише и "я понимаю" без причины
- Короткие абзацы. Никогда стена текста
- Один вопрос за раз максимум
- Помни: "неудачник который всё умеет" — обе части правда
- Язык: русский, живой, без пафоса
- Отвечай только текстом, без markdown звёздочек и решёток"""

# История диалогов по user_id
conversations = {}

def get_main_keyboard():
    keyboard = [
        [KeyboardButton("😶 Мне тяжело"), KeyboardButton("🌬 Дай технику")],
        [KeyboardButton("😴 Не могу спать"), KeyboardButton("🔄 Воспоминания")],
        [KeyboardButton("👣 Маленький шаг"), KeyboardButton("🆘 Кризис")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []

    await update.message.reply_text(
        "Антон.\n\n"
        "Я здесь. Знаю тебя — прочитал всё что ты написал.\n\n"
        "Ты написал себе «борись и не сдавайся». "
        "Это не слова человека без сил.\n\n"
        "Что сейчас?",
        reply_markup=get_main_keyboard()
    )

async def handle_crisis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Антон, ты не один.\n\n"
        "Если сейчас совсем плохо — позвони живому человеку.\n\n"
        "📞 150\n"
        "Телефон доверия Казахстан\n"
        "Анонимно. Бесплатно. Круглосуточно.\n\n"
        "Я тут — пиши.",
        reply_markup=get_main_keyboard()
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🆘 Кризис":
        await handle_crisis(update, context)
        return

    # Маппинг кнопок
    button_map = {
        "😶 Мне тяжело": "Мне сейчас тяжело",
        "🌬 Дай технику": "Дай мне технику прямо сейчас",
        "😴 Не могу спать": "Не могу заснуть снова",
        "🔄 Воспоминания": "Накатили воспоминания о прошлом",
        "👣 Маленький шаг": "Помоги найти маленький шаг вперёд сегодня"
    }
    message = button_map.get(text, text)

    if user_id not in conversations:
        conversations[user_id] = []

    conversations[user_id].append({"role": "user", "content": message})

    # Ограничение истории — последние 20 сообщений
    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]

    # Показываем что печатаем
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing"
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=800,
            system=SYSTEM_PROMPT,
            messages=conversations[user_id]
        )

        reply = response.content[0].text
        conversations[user_id].append({"role": "assistant", "content": reply})

        await update.message.reply_text(reply, reply_markup=get_main_keyboard())

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "Что-то пошло не так. Попробуй ещё раз — я никуда не ухожу.",
            reply_markup=get_main_keyboard()
        )

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conversations[user_id] = []
    await update.message.reply_text(
        "Начнём заново.\n\nЧто сейчас?",
        reply_markup=get_main_keyboard()
    )

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

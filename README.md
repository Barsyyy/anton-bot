# Антон · Telegram-бот

## Деплой на Railway (5 минут)

### 1. GitHub
- Зайди на github.com → New repository → назови `anton-bot`
- Загрузи три файла: bot.py, requirements.txt, railway.toml

### 2. Railway
- Зайди на railway.app → Login with GitHub
- New Project → Deploy from GitHub repo → выбери anton-bot
- Подожди пока задеплоится (1-2 минуты)

### 3. Переменные окружения
В Railway → твой проект → Variables → добавь:

```
TELEGRAM_TOKEN = твой_новый_токен_от_BotFather
ANTHROPIC_API_KEY = твой_ключ_anthropic
```

### 4. Готово
Открой своего бота в Telegram и напиши /start

---

### Где взять Anthropic API key?
- console.anthropic.com → API Keys → Create Key
- Скопируй и вставь в Railway Variables

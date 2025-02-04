import telebot

bot_token = '7508239534:AAHU1DEMaJWz0V7mXrtU8b_m07bvfcE6nik'
bot = telebot.TeleBot(bot_token)

# Для каждого пользователя будет храниться свой баланс
user_balances = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Напиши /balance, чтобы определить свой баланс.")

# Команда /balance
@bot.message_handler(commands=['balance'])
def ask_balance(message):
    chat_id = message.chat.id
    if chat_id not in user_balances:
        # Если пользователя ещё нет в базе, создаем его с начальным балансом
        user_balances[chat_id] = 10000   # Изначальный баланс
    bot.send_message(message.chat.id, f"Твой баланс составляет {user_balances[chat_id]} у.е.")
# Ежедневный заработок
@bot.message_handler(commands=['daily'])
def daily_bonus(message):
    bonus = 500  # Фиксированный бонус
    chat_id = message.chat.id
    current_balance = get_balance(chat_id)
    new_balance = current_balance + bonus
    update_balance(chat_id, new_balance)
    bot.send_message(message.chat.id, f"Вы получили ежедневный бонус: {bonus} у.е.!\nВаш новый баланс: {new_balance} у.е.")

# Команда /earn — заработок денег
@bot.message_handler(commands=['earn'])
def earn_money(message):
    chat_id = message.chat.id
    if chat_id not in user_balances:
        user_balances[chat_id] = 10000  # Начальный баланс, если пользователя нет в базе

    earned = random.randint(500, 5000)  # Случайная сумма заработка
    user_balances[chat_id] += earned
    bot.send_message(message.chat.id,
                         f"Ты заработал {earned} у.е.! Твой новый баланс: {user_balances[chat_id]} у.е.")

# Функция для проверки баланса перед покупкой
def check_balance(message, amount):
    chat_id = message.chat.id
    if chat_id not in user_balances:
        user_balances[chat_id] = 100  # Изначальный баланс, если пользователя нет в базе

    if user_balances[chat_id] >= amount:
        user_balances[chat_id] -= amount
        bot.send_message(message.chat.id, f"Покупка прошла успешно. Твой баланс составляет {user_balances[chat_id]} у.е.")
    else:
        bot.send_message(message.chat.id, f"Недостаточно средств. Твой баланс составляет {user_balances[chat_id]} у.е.")



@bot.message_handler(commands=['shop'])
def show_shop(message):
    shop_items = {
        '🍎 Еда': 1500,
        '🥤 Напитки': 300,
        '👕 Одежда': 7000,
        '👢 Обувь': 5000,
        '🛋 Товары для дома': 2500,
        '📚 Школьные принадлежности': 1500,
        '🎮 Компьютерные игры': 4000,
        '🎁 Подарки': 5000,
        '🏢 Квартира': 1000000,
        '🏠 Дом': 10000000,
    }
    shop_message = "Магазин товаров:\n\n"
    for item, price in shop_items.items():
        shop_message += f"{item}: {price} у.е.\n"
    bot.send_message(message.chat.id, shop_message)


# Запуск бота
bot.polling(none_stop=True)
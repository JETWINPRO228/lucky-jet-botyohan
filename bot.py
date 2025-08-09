import os
import random
import asyncio
from datetime import datetime, timedelta
import pytz
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# --- Configuration du bot ---
BOT_TOKEN = "8165798662:AAHoQNkgxDpkO_FZWV5w_0IBkCftUi7TOjA"  # Ton token
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# --- Clavier principal ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton("📡 SIGNAL")
)

# --- Cooldown des utilisateurs ---
cooldowns = {}

# --- Commande /start ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "👋 Bienvenue sur le bot LUCKY JET !\nClique sur 📡 SIGNAL pour recevoir ta prédiction.",
        reply_markup=main_kb
    )

# --- Gestion du bouton SIGNAL ---
@dp.message_handler(lambda message: message.text == "📡 SIGNAL")
async def send_signal(message: types.Message):
    user_id = message.chat.id
    now = datetime.now(pytz.timezone("Africa/Lome"))  # Heure du Togo

    # Vérification cooldown
    if user_id in cooldowns and datetime.now() < cooldowns[user_id]:
        remaining = int((cooldowns[user_id] - datetime.now()).total_seconds() // 60) + 1
        await message.answer(f"⏳ Patiente encore {remaining} minute(s) avant de demander un nouveau signal.")
        return

    # Génération des minutes aléatoires
    first_minute_offset = random.randint(2, 5)
    second_minute_offset = random.randint(1, 2)

    first_time = now + timedelta(minutes=first_minute_offset)
    second_time = first_time + timedelta(minutes=second_minute_offset)

    # Génération des multiplicateurs
    multi1 = round(random.uniform(2, 5), 1)
    multi2 = round(random.uniform(5, 10), 1)

    # Simuler "en train d'écrire"
    await bot.send_chat_action(user_id, "typing")
    await asyncio.sleep(2)

    # Envoi du signal
    text_signal = (
        f"LUCKY JET\n"
        f"{first_time.strftime('%Hh%M')} ➜ {second_time.strftime('%Hh%M')}\n"
        f"{multi1}X_____ {multi2}X"
    )
    sent_message = await message.answer(text_signal)

    # Ajouter une réaction unique
    await bot.send_message(user_id, "🥳💯")

    # Appliquer cooldown de 5 minutes
    cooldowns[user_id] = datetime.now() + timedelta(minutes=5)

# --- Lancement du bot ---
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

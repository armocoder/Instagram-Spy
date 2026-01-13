import os
import asyncio
import instaloader
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# 🔐 НАСТРОЙКИ
BOT_TOKEN = "8516846160:AAGZcHv661V4q2IhDRfppy91uiQcKcWh9PA"
IG_LOGIN = "isa.95_1"
IG_PASSWORD = "zanet95"

# Инициализация бота и диспетчера для aiogram 3.x
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Instagram loader
L = instaloader.Instaloader(
    download_comments=False,
    download_geotags=False,
    download_videos=False,
    save_metadata=False,
    compress_json=False
)

# Попытка входа (может потребоваться 2FA, если аккаунт защищен)
try:
    L.login(IG_LOGIN, IG_PASSWORD)
    print("Instagram login successful")
except Exception as e:
    print(f"Instagram login failed: {e}")

@dp.message(Command("start"))
async def start(msg: types.Message):
    await msg.answer(
        "📸 *Instagram Info Bot*\n\n"
        "Отправь мне username Instagram\n"
        "Пример: `instagram`\n\n"
        "Я пришлю информацию + аватар",
        parse_mode="Markdown"
    )

@dp.message()
async def get_profile(msg: types.Message):
    if not msg.text:
        return

    username = msg.text.strip().replace("@", "")

    try:
        profile = instaloader.Profile.from_username(L.context, username)

        text = (
            f"👤 *{profile.username}*\n"
            f"📃 {profile.biography or '—'}\n\n"
            f"👥 Подписчики: *{profile.followers}*\n"
            f"🏷️ Подписки: *{profile.followees}*\n"
            f"🔐 Приватный: *{'Да' if profile.is_private else 'Нет'}*"
        )

        # Отправляем фото напрямую по URL (aiogram 3.x поддерживает это)
        await bot.send_photo(
            msg.chat.id,
            profile.profile_pic_url,
            caption=text,
            parse_mode="Markdown"
        )

    except Exception as e:
        await msg.answer(f"❌ Ошибка:\n`{e}`", parse_mode="Markdown")

async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
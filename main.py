import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from aiogram.utils import executor
from aiogram.dispatcher.filters import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler

API_TOKEN = '7464520868:AAHuDJNgGGyMnhKQ4ywvnpDyBBh73SXYpj4'
ADMIN_ID = 6486825926
REQUIRED_CHANNEL = '@AniVerseClip'

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Fayl yo'llari
data_path = 'data'
users_path = os.path.join(data_path, 'users')
block_file = os.path.join(data_path, 'block.txt')
admin_file = os.path.join(data_path, 'tizim', 'admins.txt')

# Papkalar mavjudligini tekshirish
os.makedirs(users_path, exist_ok=True)
os.makedirs(os.path.join(data_path, 'tizim'), exist_ok=True)

# Foydalanuvchi bloklangani tekshiriladi
def is_blocked(user_id: int) -> bool:
    if os.path.exists(block_file):
        with open(block_file, 'r') as f:
            blocked = f.read().splitlines()
        return str(user_id) in blocked
    return False

# Adminlar ro'yxatini olish
def get_admins():
    if os.path.exists(admin_file):
        with open(admin_file, 'r') as f:
            return f.read().splitlines()
    return []

# Majburiy obuna tugmasi
def get_subscribe_keyboard():
    btn = InlineKeyboardMarkup(row_width=1)
    btn.add(
        InlineKeyboardButton(text="📢 Kanalga obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
    )
    return btn

@dp.message_handler(CommandStart())
async def start_handler(message: types.Message):
    user_id = message.from_user.id

    if is_blocked(user_id):
        return

    try:
        member = await bot.get_chat_member(chat_id=REQUIRED_CHANNEL, user_id=user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            await message.answer(
                "❗ Botdan foydalanish uchun quyidagi kanalga obuna bo‘ling:",
                reply_markup=get_subscribe_keyboard()
            )
            return
    except Exception as e:
        await message.answer("⚠ Kanal mavjud emas yoki bot moderator emas.")
        return

    # Statistika uchun saqlash
    user_file = os.path.join(users_path, f"{user_id}.txt")
    if not os.path.exists(user_file):
        with open(user_file, 'w') as f:
            f.write("Foydalanuvchi qo‘shildi")

    await message.answer("✅ Xush kelibsiz! Siz kanalga obuna bo‘lgansiz.")

# Admin komandasi
@dp.message_handler(lambda m: str(m.from_user.id) in get_admins())
async def admin_panel(message: types.Message):
    await message.answer("👮‍♂️ Admin panelga xush kelibsiz.")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

from aiogram import Router,F,Bot,Dispatcher
from aiogram.types import Message,CallbackQuery
from aiogram import types
from aiogram.types import Message, ContentType 
from aiogram.filters import CommandStart,Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State,StatesGroup
from io import BytesIO
from aiogram.types import InputFile
from database.requests import users
from config import TOKEN,ADMIN
from aiogram.types import BotCommand
from database.requests import users
from functions.client import channel,kino_search,download
from functions.admin import admin_config 
from states.admin_states import Admin
from states.client_states import Kino,Download

from keyboards import client as kb
from keyboards import admin as admin_kb

router=Router()
bot=Bot(token=TOKEN)
from filters import channel as chan
from database.requests import users


@router.message(CommandStart())
async def start_reply(message: Message, state: FSMContext, bot: Bot):
    await state.clear()  # Holatni tozalash
    user_id = message.from_user.id
    user = await users.find_user(user_id)
    
    not_subscribed_urls = await channel.test_subscription(user_id, bot)
    
    if not not_subscribed_urls:
        if user is None:
            await users.create_user(user_id)  # Foydalanuvchini yaratish
            user = await users.find_user(user_id)  # Yangi foydalanuvchi ma'lumotlarini olish
        # Endi foydalanuvchi mavjud bo'lsa yoki yangi yaratilgan bo'lsa, rolni tekshiramiz
        if user.role == "admin" or user_id in ADMIN:
            await message.answer("Salom ADMIN", reply_markup=admin_kb.menu)
        else:
            await message.answer(
    f"🎬 <b>Assalomu alaykum {message.from_user.full_name}</b>\n\n🎬 <b>Kino qidirish botiga xush kelibsiz!</b>\n\n📽️ <b>Kod orqali yangi kinolarni toping va ularni batafsil ko'ring.</b>\n\n🚀 <b>Yangi kino kashfiyotlaringizni boshlash uchun menyudagi tugmalarni bosing!</b>",
    reply_markup=kb.menu,
    parse_mode='HTML'
)
            # await message.answer(f"🎬 **Assalomu alaykum {message.from_user.full_name}**\n\n🎬 **Kino qidirish botiga xush kelibsiz!**\n\n📽️ **Kod orqali yangi kinolarni toping va ularni batafsil ko'ring.**\n\n🚀 **Yangi kino kashfiyotlaringizni boshlash uchun menyudagi tugmalarni bosing!**",reply_markup = kb.menu,parse_mode='HTML',)
    else:
        await channel.send_subscription_prompt(message, not_subscribed_urls)



@router.callback_query(lambda c: c.data == 'check_subscription')
async def handle_callback_query(callback_query: CallbackQuery):
    await channel.handle_callback_query(callback_query, bot)






router.message.register(kino_search.start_kino,F.text=="🎬 Kinolar")
router.message.register(kino_search.state_kino1,Kino.start)
router.message.register(kino_search.kino_code,Kino.code)

# router.message.register(kino.title_kino,Kino.title)

router.message.register(download.start_down,F.text=="📥 Video yuklash")
router.message.register(download.state_down,Download.start)
# router.message.register(kino_search.kino_code,Kino.code)


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@router.message(F.text == "🤝 Hamkorlik")
async def hamkorlik_info(message: Message):
    # Inline klaviatura yaratish
    keyboard = InlineKeyboardBuilder()
    
    # Telegram kanal tugmasi
    channel_button = InlineKeyboardButton(
        text="👤 ADMIN1", 
        url="https://t.me/Jobbor_admin"
    )
    
    # Adminlar va bot dasturchilari tugmalari
    admin1_button = InlineKeyboardButton(
        text="👤 ADMIN1", 
        url="https://t.me/Detri_maxx"
    )
    admin2_button = InlineKeyboardButton(
        text="👤 ADMIN2", 
        url="https://t.me/dhhshs838"
    )
    bot_dev_button = InlineKeyboardButton(
        text="🤖 BOT DASTURCHISI", 
        url="https://t.me/Shax_brend1"
    )

    # Tugmalarni qo'shish
    keyboard.row(channel_button)
    # keyboard.row(admin1_button, admin2_button)
    # keyboard.row(bot_dev_button)
    
    text = """
🤝 <b>Hamkorlik uchun bog'laning:</b>


Ishonchli hamkorlik va sifatli xizmatlar uchun biz bilan bog'laning. Sizni kutib qolamiz!
"""
    await message.answer(text, parse_mode='HTML', reply_markup=keyboard.as_markup())

from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from aiogram import Bot
from config import CHANNEL_ID
from aiogram import types
from database.requests import channel_requests,users
from keyboards import client as kb
from keyboards import admin as admin_kb
async def send_subscription_prompt(message: Message, channels: list):
    # InlineKeyboardBuilder ob'ekti yaratish
    builder = InlineKeyboardBuilder()

    for url in channels:
        button = InlineKeyboardButton(text="📢 Obuna bo'lish", url=url)
        builder.row(button)  # Har bir tugmani alohida qatorda ko'rsatish

    check_button = InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="check_subscription")
    builder.row(check_button)  # "Obuna bo'ldim" tugmasini alohida qatorda ko'rsatish

    # Klaviaturani yuborish
    await message.answer(
        "🔔 Botdan to'liq foydalanish uchun ushbu kanallarga obuna bo'ling 👇\n\n"
        "📢 Bizni qo'llab-quvvatlaganlaringiz uchun rahmat! 😊",
        reply_markup=builder.as_markup()
    )
    text = """
📢 <b>Kanallarga obuna bo'lish</b> bo'timizni doimo ishlashini ta'minlaydi! 🚀

Sizning qo'llab-quvvatlovingiz bizning muvaffaqiyatimiz uchun juda muhim. Har doim yangiliklardan xabardor bo'lish va bizning xizmatlarimizdan foydalanishda davom eting! 💪

Rahmat sizga! 🙌
"""
    await message.answer(text,parse_mode="HTML",reply_markup=kb.chan_btn)


async def test_subscription(user_id: int, bot: Bot) -> list:
    chat_ids = await channel_requests.get_channel_chat_ids()
    unsubscribed_channels = []  # Obuna bo'lmagan kanallar ro'yxati

    for chat_id in chat_ids:
        try:
            chat_member = await bot.get_chat_member(chat_id, user_id)
            if chat_member.status not in ['member', 'administrator', 'creator']:
                print(chat_member)
                url = await channel_requests.get_channel_url_by_chat_id(chat_id)
                if url:
                    unsubscribed_channels.append(url)
            print(unsubscribed_channels)
        except Exception as e:
            # Xatolikni foydalanuvchiga yuborish
            print(e)
    
    return unsubscribed_channels  # Obuna bo'lmagan kanallarni qaytaring

async def handle_callback_query(callback_query: CallbackQuery, bot: Bot):
    if callback_query.data == "check_subscription":
        user_id = callback_query.from_user.id
        not_subscribed_urls = await test_subscription(user_id, bot)

        if not not_subscribed_urls:
            # Agar ro'yxat bo'sh bo'lsa, foydalanuvchiga xabar yuboring
            await bot.send_message(
                chat_id=callback_query.from_user.id,
                text = "🎬 **Kino qidirish botiga xush kelibsiz!**\n\n📽️ **Kod orqali yangi kinolarni toping va ularni batafsil ko'ring.**\n\n🚀 **Yangi kino kashfiyotlaringizni boshlash uchun menyudagi tugmalarni bosing!**",reply_markup = kb.menu

            )
            # Foydalanuvchini bazada tekshiramiz
            user = await users.find_user(user_id)
            if not user:
                # Agar foydalanuvchi topilmasa, uni yaratamiz
                await users.create_user(user_id)
        else:
            # Obuna bo'lmagan kanallar uchun yana obuna taklifi yuboriladi
            await povtor(message=callback_query.message, urls=not_subscribed_urls)

async def povtor(message: Message, urls):
    # InlineKeyboardBuilder ob'ekti yaratish
    builder = InlineKeyboardBuilder()
    
    for url in urls:
        button = InlineKeyboardButton(text="📢 Obuna bo'lish", url=url)
        builder.row(button)  # Har bir tugmani alohida qatorda ko'rsatish

    check_button = InlineKeyboardButton(text="✅ Tasdiqlash", callback_data="check_subscription")
    builder.row(check_button)  # "Obuna bo'ldim" tugmasini alohida qatorda ko'rsatish

    # Klaviaturani yuborish
    await message.answer(
        "🔔 Botdan to'liq foydalanish uchun ushbu kanallarga obuna bo'ling 👇\n\n"
        "📢 Bizni qo'llab-quvvatlaganlaringiz uchun rahmat! 😊",
        reply_markup=builder.as_markup()
    )









async def get_channel_id(message: Message):
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        await message.answer(f"Kanal ID: {channel_id}",reply_markup=admin_kb.menu_btn)
    else:
        await message.answer("Xabar kanal tomonidan yuborilmagan.",reply_markup=admin_kb.menu_btn)



from aiogram import  Bot,Router,F
from aiogram.types import Message, CallbackQuery
from states import client_states 
from aiogram.fsm.context import FSMContext
import keyboards.client as kb
from database.requests.kino_requests import *
from functions.client import channel
router = Router()
from config import ADMIN
async def start_kino(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    not_subscribed_urls = await channel.test_subscription(user_id, bot)
    if not_subscribed_urls:
        await channel.send_subscription_prompt(message, not_subscribed_urls)
    else:
        await message.answer("🔘 Tugmalardan birini tanlang:", reply_markup=kb.kino_btn)
        await state.set_state(client_states.Kino.start)

async def state_kino1(message: Message, bot: Bot, state: FSMContext):
    if message.text == "🔍 KOD bilan izlash":
        user_id = message.from_user.id
        not_subscribed_urls = await channel.test_subscription(user_id, bot)
        if not_subscribed_urls:
            await channel.send_subscription_prompt(message, not_subscribed_urls)
        else:
            await message.answer("🎬📥 **Kino kodini kiriting:**\n\nIltimos, kerakli kino kodini kiriting. Kod yordamida kino topishingiz mumkin.",reply_markup=kb.back)
            await state.set_state(client_states.Kino.code)
    elif message.text == "🎲 Tasodifiy kino":
        user_id = message.from_user.id
        not_subscribed_urls = await channel.test_subscription(user_id, bot)
        if not_subscribed_urls:
            await channel.send_subscription_prompt(message, not_subscribed_urls)
        else:
            user = message.from_user.id
            kino = await get_random_kino()
            if kino:
                message_text = (
                f"<b>🎬 Kino nomi: {kino.title}</b>\n\n"
                f"<b>🎭 Janri: {kino.janr}</b>\n\n"
                f"<b>🌍 Tili: {kino.language}</b>\n\n"
                f"<b>🏴 Davlati: {kino.country}</b>\n\n"
                f"<b>📅 Yili: {kino.year}</b>\n\n"
                f"<b>🔎 Sifati: {kino.attribute}</b>\n\n"
                f"<b>🆔 Kino kodi: {kino.code}</b>\n\n"
                f"<b>⬇️ Yuklab olishlar soni: {kino.download} marta</b>\n"
            )

        
            await bot.send_video(
                chat_id=user,
                video=kino.file_id,
                caption=message_text,parse_mode="HTML",reply_markup=kb.kino_btn
            )
    elif message.text == "📊 TOP Kinolar 🎬":
        user_id = message.from_user.id
        not_subscribed_urls = await channel.test_subscription(user_id, bot)
        if not_subscribed_urls:
            await channel.send_subscription_prompt(message, not_subscribed_urls)
        else:
            kinolar1 = await get_top_10_kinos()
            if kinolar1:
                response_text = "🌟 <b><i>TOP 10 Kinolar</i></b> 🌟\n\n"
                for kino in kinolar1:
                    response_text += (
                        f"<b>🎬 Nomi: {kino.title}</b>\n"
                        f"<b>🔢 KODI: {kino.code}</b>\n"
                        f"<b>📈 Yuklab olishlar soni: {kino.download} marta</b>\n"
                        f"------------------------------\n"
                    )
                await message.answer(response_text, parse_mode='HTML')
            else:
                await message.answer("❌ Kinolar topilmadi.")
    elif message.text == "🏠 Bosh menu":
        response_text = (
            "🏠 **Bosh menyu**\n\n"
            "👋 Siz bosh menyuga qaytdingiz!\n\n"
            "📂 Quyidagi bo‘limlardan birini tanlang:\n"
          
        )
        await message.answer(response_text, reply_markup=kb.menu, parse_mode='Markdown')
        await state.clear()

async def kino_code(message: Message, bot: Bot, state: FSMContext):
    if message.text == "↩️ Ortga":
        # `start_kino` funksiyasini chaqirish
        await start_kino(message, bot, state)
    else:
        kino = await find_kino_code(message.text)
        user = message.from_user.id

        if kino:
            # Create a formatted message
            message_text = (
                f"<b>🎬 Kino nomi: {kino.title}</b>\n\n"
                f"<b>🎭 Janri: {kino.janr}</b>\n\n"
                f"<b>🌍 Tili: {kino.language}</b>\n\n"
                f"<b>🏴 Davlati: {kino.country}</b>\n\n"
                f"<b>🔎 Sifati: {kino.attribute}</b>\n\n"
                f"<b>📅 Yili: {kino.year}</b>\n\n"
                f"<b>🆔 Kino kodi: {kino.code}</b>\n\n"
                f"<b>⬇️ Yuklab olishlar soni: {kino.download} marta</b>\n"
            )

        
            await bot.send_video(
                chat_id=user,
                video=kino.file_id,
                caption=message_text,parse_mode="HTML",reply_markup=kb.menu
            )
            await state.clear()
        else:
            text = """
🎬📥 <b>Kino kodini kiriting:</b>

Iltimos, kerakli kino kodini kiriting. Kod yordamida kino topishingiz mumkin. 🔍🎥
"""
            await message.answer(text, parse_mode='HTML')

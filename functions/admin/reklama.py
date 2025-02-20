import asyncio
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError
from states.admin_states import Reklama
from keyboards.admin import *
from database.requests.users import *
from config import ADMIN

router = Router()

@router.message(F.text == "Reklama Yuborish")
async def start_reklama(message: Message, state: FSMContext):
    if message.from_user.id in ADMIN:
        await message.answer("📩 Reklama matnini kiriting:", reply_markup=menu_btn)
        await state.set_state(Reklama.text)
    else:
        await message.answer("🚫 Siz admin emassiz!", reply_markup=menu_btn)

@router.message(Reklama.text)
async def start_reklama_text(message: Message, state: FSMContext):
    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин", reply_markup=menu_btn)
    else:
        await state.update_data(text=message.text)
        await message.answer("📸 Rasm yoki 🎥 Video yuboring:", reply_markup=menu_btn)
        await state.set_state(Reklama.media)

@router.message(Reklama.media)
async def start_reklama_media(message: Message, state: FSMContext, bot: Bot):
    tg_id = message.from_user.id

    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин", reply_markup=menu_btn)
        return

    media_type = None
    file_id = None

    if message.video:
        file_id = message.video.file_id
        media_type = "video"
    elif message.photo:
        file_id = message.photo[-1].file_id
        media_type = "photo"

    if media_type:
        await state.update_data(media=file_id, media_type=media_type)
        await message.answer(f"✅ {'Video' if media_type == 'video' else 'Rasm'} qabul qilindi.", reply_markup=menu_btn)

        data = await state.get_data()
        text_message = data.get('text')

        if media_type == "video":
            await bot.send_video(chat_id=tg_id, video=file_id, caption=text_message, reply_markup=confirm)
        else:
            await bot.send_photo(chat_id=tg_id, photo=file_id, caption=text_message, reply_markup=confirm)

        await state.set_state(Reklama.verify)
    else:
        await message.answer("🚫 Rasm yoki video jo‘nating!", reply_markup=menu_btn)

async def send_message(user, bot, media_type, media, text):
    try:
        if media_type == "photo":
            await bot.send_photo(chat_id=user, photo=media, caption=text)
        else:
            await bot.send_video(chat_id=user, video=media, caption=text)
        return True
    except TelegramForbiddenError:
        return False
    except Exception:
        return False

@router.message(Reklama.verify)
async def sms_verify(message: Message, state: FSMContext, bot: Bot):
    tg_id = message.from_user.id

    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин", reply_markup=menu_btn)
        return

    if message.text == "✅ Tasdiqlash":
        data = await state.get_data()
        media_type = data.get('media_type')
        text = data.get('text')
        media = data.get('media')

        if media_type not in ["photo", "video"]:
            await message.answer("🚫 Faqat rasm yoki video yuborishingiz mumkin!")
            return

        await message.answer("📤 Kuting, reklama tarqatilyapti...", reply_markup=await_btn)

        users = await get_users_tg_ids()
        total_users = len(users)

        # Parallel ravishda yuborish
        tasks = [asyncio.create_task(send_message(user, bot, media_type, media, text)) for user in users]
        results = await asyncio.gather(*tasks)
        
        success_count = results.count(True)
        failed_count = results.count(False)

        await bot.send_message(
            chat_id=tg_id,
            text=f"📢 <b>{total_users}</b> foydalanuvchidan <b>{success_count}</b> tasiga reklama jo‘natildi.\n❌ <b>{failed_count}</b> foydalanuvchi aktiv emas.",
            parse_mode='HTML',
            reply_markup=menu_btn
        )
        await state.clear()
    else:
        await message.answer("🚫 Faqat tugmalarni ishlating!")

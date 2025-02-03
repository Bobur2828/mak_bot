from aiogram import  Bot,Router,F
from aiogram.types import Message,CallbackQuery
from states.admin_states import Reklama
from aiogram.fsm.context import FSMContext
from keyboards.admin import *
from database.requests.users import *
# from database.requests.user_request import *
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types import Location
import requests
from config import ADMIN

async def start_reklama(message: Message, bot: Bot, state: FSMContext):
    if message.from_user.id in ADMIN:

        await message.answer("Reklama matnini kiriting",reply_markup=menu_btn)
        await state.set_state(Reklama.text)
    else:
        await message.answer("Вы не админ",reply_markup=menu_btn)

async def start_reklama_text(message: Message, bot: Bot, state: FSMContext):
    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин",reply_markup=menu_btn)
    else:
        await state.update_data(text=message.text)
        await message.answer("Rasm yoki Video yuboring",reply_markup=menu_btn)
        await state.set_state(Reklama.media)


async def start_reklama_media(message: Message, bot: Bot, state: FSMContext):
    tg_id = message.from_user.id
    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин",reply_markup=menu_btn)

    elif message.video:
        file_id = message.video.file_id
        await state.update_data(media=file_id)
        await state.update_data(media_type="video")
        await message.answer("Video qabul qilindi✅", reply_markup=menu_btn)
        data = await state.get_data()
        text_message=data.get('text')
        b= data.get('media')
        await bot.send_video(chat_id=tg_id, video=b,caption=text_message,reply_markup=confirm)
        await state.set_state(Reklama.verify)
    elif message.photo:
        file_id = message.photo[-1].file_id
        # await message.answer(file_id)
        await state.update_data(media=file_id)
        await state.update_data(media_type="photo")
        await message.answer("Rasm qabul qilindi✅",reply_markup=menu_btn)
        # await message.answer(file_id)

        data = await state.get_data()
        b= data.get('media')
        text_message=data.get('text')
        await bot.send_photo(chat_id=tg_id, photo=b,caption=text_message,reply_markup=confirm)
        await state.set_state(Reklama.verify)

    else:
        await message.answer("Rasm yoki Video jo'nating",reply_markup=menu_btn)

from aiogram.exceptions import TelegramForbiddenError
async def sms_verify(message: Message, bot: Bot, state: FSMContext):
    tg_id=message.from_user.id
    if message.text == "⬅️  Назад":
        await state.clear()
        await message.answer("Привет Aдмин",reply_markup=menu_btn)
    
    elif message.text == "✅ Tasdiqlash":
        data = await state.get_data()
        media_type=data.get('media_type')
        if media_type == "photo":
            text=data.get('text')
            photo=data.get('media')
            users = await get_users_tg_ids()
            forbidden_count = 0
            count_for=0
            try:
                for user in users:
                    count_for += 1
                    try:
                        await bot.send_photo(chat_id=user, photo=photo, caption=text)
                    except TelegramForbiddenError:
                        forbidden_count += 1  # Agar TelegramForbiddenError yuzaga kelsa, hisoblagichni oshirish

            except Exception as e:
                await bot.send_message(chat_id=tg_id, text=f"An unexpected error occurred: {e}")

            await bot.send_message(chat_id=tg_id, text=f" {count_for}ta foydalanuvchidan {count_for - forbidden_count } tasiga reklama jonatildi {forbidden_count} ta foydalanuvchi aktiv emas ", parse_mode='HTML', reply_markup=menu_btn)
            await state.clear()

        elif media_type == "video":
            text=data.get('text')
            video=data.get('media')
            users = await get_users_tg_ids()
            forbidden_count = 0
            count_for=0
            try:
                for user in users:
                    count_for += 1
                    try:
                		    await bot.send_video(chat_id=user,video=video,caption=text)
                    except TelegramForbiddenError:
                        forbidden_count += 1  # Agar TelegramForbiddenError yuzaga kelsa, hisoblagichni oshirish


            except Exception as e:
                await bot.send_message(chat_id=tg_id, text=f"An unexpected error occurred: {e}")

            await bot.send_message(chat_id=tg_id, text=f"{count_for}ta foydalanuvchidan {count_for - forbidden_count } tasiga reklama jonatildi {forbidden_count} ta foydalanuvchi aktiv emas ", parse_mode='HTML', reply_markup=menu_btn)
            
            await state.clear()

        else:
            await message.answer("Faqat rasm yoki video jonata olasiz")

    else:
        message.answer("Используйте только кнопки")   
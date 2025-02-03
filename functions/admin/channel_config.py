from aiogram import  Bot,Router,F
from aiogram.types import Message, CallbackQuery
from states.admin_states import AddChannel,FindChannel
from aiogram.fsm.context import FSMContext
import keyboards.admin as kb
from database.requests.channel_requests import *
from database.requests.admin_request import is_config
router = Router()
from config import ADMIN
async def start_admin(message: Message, bot: Bot, state: FSMContext):
    if await is_config.is_admin(message.from_user.id):
        await message.answer("Tugmalardan birini tanlang", reply_markup=kb.channel_btn)
        await state.set_state(AddChannel.start)

# Kanal qo'shish/o'chirish funksiyasi
async def add_channel(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Kanal qo'shish":
        await state.update_data(start="add")
        await message.answer("Kanal URL manzilini yuboring", reply_markup=kb.menu_btn)
        await state.set_state(AddChannel.url)
        
    elif message.text == "Kanal o'chirish":
        await state.update_data(start="delete")
        await message.answer("Kanal URL manzilini yuboring", reply_markup=kb.menu_btn)
        await state.set_state(AddChannel.url)

    elif message.text == "Kanallar ro'yhati":
        channels = await get_channels()
        if channels:
            for channel in channels:
                await message.answer(f"{channel.chat_id} - {channel.url}")
        else:
            await message.answer("Kanallar ro'yxati bo'sh.")
    
    elif message.text == "Ortga":
        await state.clear()
        await message.answer("ADMIN", reply_markup=kb.menu)

# URL yuborish va kanal ID ni so'rash
async def find_id_channel(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        await message.answer("ADMIN", reply_markup=kb.menu)
    else:
        await state.update_data(url=message.text)
        await message.answer("Kanal ID sini yuboring", reply_markup=kb.menu_btn)
        await state.set_state(AddChannel.chat_id)

# Kanalni qo'shish yoki o'chirishni tasdiqlash
async def confirm_channel(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Bosh menu":
        await state.clear()
        await message.answer("ADMIN", reply_markup=kb.menu)
    else:
        await state.update_data(chat_id=message.text)
        data = await state.get_data()

        if data.get("start") == "add":
            await create_channel(chat_id=data["chat_id"], url=data["url"])
            await message.answer("Kanal muvaffaqiyatli qo'shildi", reply_markup=kb.menu)

        elif data.get("start") == "delete":
            await delete_channel(data["url"])
            await message.answer("Kanal muvaffaqiyatli o'chirildi", reply_markup=kb.menu)

        await state.clear()


from functions.client import channel

async def start_id_channel(message: Message, bot: Bot, state: FSMContext):
    if await is_config.is_admin(message.from_user.id):
        await message.answer("Kanaldan xabar forward qiling", reply_markup=kb.menu_btn)
        await state.set_state(FindChannel.start)

async def find_id(message: Message, bot: Bot, state: FSMContext):
    if message.forward_from_chat:
        channel_id = message.forward_from_chat.id
        await message.answer(f"Kanal ID: {channel_id}", reply_markup=kb.menu_btn)
    else:
        await message.answer("Xabar kanal tomonidan forward qilinmagan. Iltimos, kanaldan forward qilingan xabarni yuboring.", reply_markup=kb.menu_btn)


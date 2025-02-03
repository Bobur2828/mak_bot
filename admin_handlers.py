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
from functions.client import channel
from functions.admin import admin_config,channel_config,reklama,kino
from states.admin_states import Admin,AddChannel,FindChannel,Reklama,Kino
from keyboards import admin as kb
from keyboards import client as client_kb
from database.requests.admin_request import is_config
router=Router()
bot=Bot(token=TOKEN)
from database.requests import users




router.message.register(admin_config.start_admin,F.text=="Adminlar")
router.message.register(admin_config.state_admin,Admin.start)
router.message.register(admin_config.confirm_admin,Admin.tg_id)


@router.message(F.text=="Bosh menu")
async def setting_ru(message: Message,state: FSMContext):
    # admins = await users.find_admins()
    if await is_config.is_admin(message.from_user.id):
        await state.clear()
        await message.answer("ADMIN PANEL", reply_markup=kb.menu)
    else:
        await state.clear()
        await message.answer("CLIENT PANEL", reply_markup=client_kb.menu)

@router.message(F.text=="Foydalanuvchilar soni")
async def send_channel(message: Message):
    count = await users.count_users()
    await message.answer(f"Botning aktiv foydalanuvchilar soni {count}ta")


router.message.register(channel_config.start_admin,F.text=="Kanallar")
router.message.register(channel_config.add_channel,AddChannel.start)
router.message.register(channel_config.find_id_channel,AddChannel.url)
router.message.register(channel_config.confirm_channel,AddChannel.chat_id)

router.message.register(channel_config.start_id_channel,F.text=="Kanal ID sini aniqlash")
router.message.register(channel_config.find_id,FindChannel.start)

router.message.register(reklama.start_reklama,F.text=="Reklama")
router.message.register(reklama.start_reklama_text,Reklama.text)
router.message.register(reklama.start_reklama_media,Reklama.media)
router.message.register(reklama.sms_verify,Reklama.verify)



router.message.register(kino.start_kino,F.text=="Kinolar")
router.message.register(kino.state_kino1,Kino.start1)
router.message.register(kino.title_kino,Kino.title)
router.message.register(kino.language_kino,Kino.language)
router.message.register(kino.attribute_kino,Kino.attribute)
router.message.register(kino.genre_kino,Kino.genre)
router.message.register(kino.year_kino,Kino.year)
router.message.register(kino.country_kino,Kino.country)
router.message.register(kino.file_id_kino,Kino.file_id)
router.message.register(kino.confirm_kino,Kino.confirm)

router.message.register(kino.delete_kino,Kino.delete)
router.message.register(kino.confirm_delete,Kino.delconfirmed)












from aiogram import  Bot,Router,F
from aiogram.types import Message, CallbackQuery
from states import admin_states 
from aiogram.fsm.context import FSMContext
import keyboards.admin as kb
from database.requests.kino_requests import *
from database.requests.admin_request import is_config
router = Router()
from config import ADMIN
async def start_kino(message: Message, bot: Bot, state: FSMContext):
    if await is_config.is_admin(message.from_user.id):
        await message.answer("Tugmalardan birini tanlang", reply_markup=kb.kino_btn)
        await state.set_state(admin_states.Kino.start1)
MAX_MESSAGE_LENGTH = 4096 

async def state_kino1(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Kino Yuklash":
        await message.answer("Kino nomini kiriting",reply_markup=kb.menu_btn)
        await state.set_state(admin_states.Kino.title)
    elif message.text == "Kino o'chirish":
        await message.answer("Kino ko'dini kiriting",reply_markup=kb.menu_btn)
        await state.set_state(admin_states.Kino.delete)


    elif message.text == "Kinolar ro'yhati":
        kinolar = await get_kinos()
        if kinolar:
            kino_entries = []
            for index, kino in enumerate(kinolar, start=1):
                entry = f"{index}. Kino nomi = {kino.title} Kodi = {kino.code}"
                kino_entries.append(entry)

            kino_message = "\n".join(kino_entries)  # Hammasini bitta matn sifatida birlashtiramiz

            # Xabarni cheklangan uzunlikka bo‘lib yuboramiz
            while kino_message:
                await message.answer(kino_message[:MAX_MESSAGE_LENGTH])  # 4096 tagacha bo‘lgan qismini jo‘natamiz
                kino_message = kino_message[MAX_MESSAGE_LENGTH:]  # Qolgan qismini keyingi xabarga saqlaymiz
        else:
            await message.answer("Kinolar ro'yxati bo'sh.")
    elif message.text == "Ortga":
        await state.clear()
        await message.answer("ADMIN", reply_markup=kb.menu)
    else:
        await message.answer("Faqat tugmalardan foydalaning",reply_markup=kb.menu_btn)


async def delete_kino(message: Message, bot: Bot, state: FSMContext):
    await state.update_data(delete=message.text)
    code = message.text
    user = message.from_user.id
    kino = await find_kino_code(code)
    if kino:
        message = (
                f"🎬 Kino nomi: {kino.title}\n"
                f"🎭 Janri: {kino.janr}\n"
                f"🌍 Tili: {kino.language}\n"
                f"🏴 Davlati: {kino.country}\n"
                f"🔎 Sifati: {kino.attribute}\n"
                f"Kino kodi:{kino.code}\n"

                f"KINO OCHIRISHNI TASDIQLANG"

            )
        await bot.send_video(
                chat_id=user,
                video=kino.file_id,
                caption=message,reply_markup=kb.confirm
            )
        await state.set_state(admin_states.Kino.delconfirmed)
    else:
        await message.answer("Kino topilmadi")

async def confirm_delete(message: Message, bot: Bot, state: FSMContext):
    if message.text == "✅ Tasdiqlash":
        data = await state.get_data()
        code = data.get('delete')
        user = message.from_user.id
        kino = await find_kino_code(code)
        await delete_kino_by_id(kino.id)
        await bot.send_message(chat_id=user, text="Kino o'chirildi")
        await state.clear()
    else:
        await message.answer("Iltimos, kino o'chirishni tasdiqlang")





async def title_kino(message:Message,bot:Bot,state:FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Kino tilini kiriting",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.language)

async def language_kino(message:Message, bot: Bot, state: FSMContext):
    await state.update_data(language=message.text)
    await message.answer("Kino sifati haqida malumot bering",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.attribute)

async def attribute_kino(message:Message, bot: Bot, state: FSMContext):
    await state.update_data(attribute=message.text)
    await message.answer("Kino Janrini  kiriting",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.genre)

async def genre_kino(message:Message, bot: Bot, state: FSMContext):
    await state.update_data(genre=message.text)
    await message.answer("Kino yilini kiriting",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.year)

async def year_kino(message:Message, bot: Bot, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer("Kino davlatini kiriting",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.country)

async def country_kino(message:Message, bot: Bot, state: FSMContext):
    await state.update_data(country=message.text)
    await message.answer("Kinoni yuklang",reply_markup=kb.menu_btn)
    await state.set_state(admin_states.Kino.file_id)

async def file_id_kino(message: Message, bot: Bot, state: FSMContext):
    user = message.from_user.id
    if message.video:
        video_file_id = message.video.file_id
        await state.update_data(file_id=video_file_id)
        data = await state.get_data()

        title = data.get("title")
        genre = data.get("genre")
        year = data.get("year")
        country = data.get("country")
        file_id = data.get("file_id")
        language = data.get("language")
        attribute = data.get("attribute")

        message = (
            f"🎬 Kino nomi: {title}\n"
            f"🎭 Janri: {genre}\n"
            f"🌍 Tili: {language}\n"
            f"🏴 Davlati: {country}\n"
            f"🔎 Sifati: {attribute}"
        )
    

        # Send the video and the message
        await bot.send_video(
            chat_id=user,
            video=video_file_id,
            caption=message,reply_markup=kb.confirm
        )

        await state.set_state(admin_states.Kino.confirm)
    else:
        await message.answer("Iltimos, video yuklang.")

async def confirm_kino(message: Message, bot: Bot, state: FSMContext):
    if message.text == "✅ Tasdiqlash":
        user = message.from_user.id
        data = await state.get_data()

        title = data.get("title")
        genre = data.get("genre")
        year = data.get("year")
        country = data.get("country")
        file_id = data.get("file_id")
        language = data.get("language")
        attribute = data.get("attribute")


        await create_kino(title=title, janr=genre, year=year, country=country, download=1, attribute=attribute, language=language, file_id=file_id)
        
        
        kino = await find_kino(title=title)

        message = (
            f"<b>🎬 Kino nomi:{kino.title}</b>\n"
            f"🎭 Janri: {kino.janr}\n"
            f"🌍 Tili: {kino.language}\n"
            f"🏴 Davlati: {kino.country}\n"
            f"🔎 Sifati: {kino.attribute}\n"
            f"Kino kodi:{kino.code}\n"

        )
        await bot.send_video(
            chat_id=user,
            video=kino.file_id,
            caption=message,parse_mode='HTML',reply_markup=kb.menu_btn
        )
        await state.clear()



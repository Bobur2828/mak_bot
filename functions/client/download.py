import os
from pytube import YouTube
from aiogram import Bot, Router
from aiogram.types import Message, InputFile
from aiogram.fsm.context import FSMContext
import keyboards.client as kb
from states import client_states

router = Router()

async def start_down(message: Message, bot: Bot, state: FSMContext):
    await message.answer("🔘 Video linkini kiriting:", reply_markup=kb.kino_btn)
    await state.set_state(client_states.Download.start)

async def state_down(message: Message, bot: Bot, state: FSMContext):
    url = message.text

    if not url:
        await message.answer("❌ Iltimos, video linkini to'g'ri kiriting.")
        return

    # Video URL-ni YouTube obyektiga aylantirish
    try:
        yt = YouTube(url)
        # Eng yaxshi sifatdagi video oqimni tanlash
        video_stream = yt.streams.get_highest_resolution()
        
        # Video yuklab olish
        temp_file_path = "temp_video.mp4"
        video_stream.download(output_path='.', filename=temp_file_path)

        # Fayl mavjudligini tekshirish va yuborish
        if os.path.exists(temp_file_path):
            with open(temp_file_path, 'rb') as video_file:
                video = InputFile(video_file, filename='video.mp4')
                await bot.send_video(
                    chat_id=message.from_user.id,
                    video=video,
                    caption="📥 Siz so'ragan video yuklandi."
                )
            # Faylni o'chirish
            os.remove(temp_file_path)

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {str(e)}")

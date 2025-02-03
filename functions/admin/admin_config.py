from aiogram import  Bot,Router,F
from aiogram.types import Message, CallbackQuery
from states.admin_states import Admin
from aiogram.fsm.context import FSMContext
import keyboards.admin as kb
from database.requests.users import *
from database.requests.admin_request import is_config
router = Router()
from config import ADMIN
async def start_admin(message: Message, bot: Bot, state: FSMContext):
    if await is_config.is_admin(message.from_user.id):
        await message.answer("Tugmalardan birini tanlang", reply_markup=kb.admin_btn)
        await state.set_state(Admin.start)

async def state_admin(message: Message, bot: Bot, state: FSMContext):
    if message.text == "Ortga":
        await state.clear()
        await message.answer("Tugmalardan birini tanlang", reply_markup=kb.menu)
    
    elif message.text == "Adminlar ro'yhati":
        admins = await find_admins()
        if admins:
            for admin_id in admins:
                await message.answer(f"Admin: {admin_id}")
        else:
            await message.answer("Adminlar ro'yxati bo'sh.")
    else:

        await state.update_data(start=message.text)
        await message.answer("Foydalanuvchi CHAT ID sini kiriting",reply_markup=kb.menu_btn)
        await state.set_state(Admin.tg_id)

async def confirm_admin(message: Message, bot: Bot, state: FSMContext):
    if message.text=="Bosh menu":
        await state.clear()
        await message.answer("Tugmalardan birini tanlang", reply_markup=kb.menu)
    else:    
        await state.update_data(tg_id=message.text)

        data = await state.get_data()
        start_value = data.get('start')
        tg_id = data.get('tg_id')
        user = await find_user(tg_id)
        
        if start_value == "Admin qo'shish":
            if user is None:
                await message.answer("Foydalanuvchi bo'tda ro'yhatdan o'tmagan",reply_markup=kb.menu_btn)
            else:
                await update_user(tg_id=tg_id, new_role="admin")
                await message.answer("Foydalanuvchi admin qilib qo'shildi.",reply_markup=kb.menu_btn)
                await state.clear()
        elif start_value == "Admin o'chirish":
            if user is None:
                await message.answer("Foydalanuvchi bo'tda ro'yhatdan o'tmagan",reply_markup=kb.menu_btn)
            else:
                await update_user(tg_id=tg_id, new_role="member")
                await message.answer("Foydalanuvchi adminlikdan o'chirildi.",reply_markup=kb.menu_btn)
                await state.clear()
        

async def update_user(tg_id, new_role):
    query = update(User).where(User.tg_id == tg_id).values(role=new_role).execution_options(synchronize_session="fetch")
    
    try:
        async with async_session() as session:
            # Yangilash so'rovini bajarish
            await session.execute(query)
            await session.commit()  # O'zgarishlarni bazada saqlash
            return True
    except Exception as e:
        print(f"Ma'lumotlar bazasini yangilashda xatolik yuz berdi: {e}")
        return False



        
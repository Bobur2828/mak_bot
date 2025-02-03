from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext


class Kino(StatesGroup):
    start=State()
    code=State()
    confirm=State()


class Download(StatesGroup):
    start=State()
    code=State()
    confirm=State()
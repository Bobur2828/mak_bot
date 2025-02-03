from aiogram.fsm.state import State,StatesGroup
from aiogram.fsm.context import FSMContext


class Admin(StatesGroup):
    start=State()
    tg_id=State()
    confirm=State()

class AddChannel(StatesGroup):
    start=State()
    url=State()
    chat_id=State()
    confirm=State()

class FindChannel(StatesGroup):
    start=State()
    id=State()


class Reklama(StatesGroup):
    text = State()
    media = State()
    media_type=State()
    verify=State()


class Kino(StatesGroup):
    start1=State()
    title=State()
    attribute=State()
    genre=State()
    language=State()
    year=State()
    country=State()
    file_id=State()
    confirm=State()
    delete=State()
    delconfirmed=State()
    kinolist=State()


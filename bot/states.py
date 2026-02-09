from aiogram.fsm.state import StatesGroup, State

class Flow(StatesGroup):
    waiting_gender = State()
    waiting_media = State()
    waiting_caption = State()

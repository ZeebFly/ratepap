from aiogram.fsm.state import StatesGroup, State

class Flow(StatesGroup):
    waiting_media = State()
    waiting_caption = State()

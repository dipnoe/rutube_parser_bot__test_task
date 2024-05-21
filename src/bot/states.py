from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    waiting_for_link = State()
    waiting_for_videos_amount = State()

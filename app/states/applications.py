from aiogram.fsm.state import State, StatesGroup


class ApplicationState(StatesGroup):
    full_name = State()
    phone = State()
    message = State()
from aiogram.fsm.state import State, StatesGroup


class AdminJobState(StatesGroup):
    title = State()
    company = State()
    city = State()
    salary = State()
    profession = State()    
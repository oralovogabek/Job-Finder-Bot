from aiogram.fsm.state import State, StatesGroup


class JobSearchState(StatesGroup):
    city = State()
    salary = State()
    profession = State()
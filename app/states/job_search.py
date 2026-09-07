from aiogram.fsm.state import State, StatesGroup


class JobSearchState(StatesGroup):
    choosing = State()
    city = State()
    salary = State()
    profession = State()
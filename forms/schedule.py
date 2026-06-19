from aiogram.fsm.state import (
    State, 
    StatesGroup
)

 


class Form2(StatesGroup):
    day = State()
    activity = State()

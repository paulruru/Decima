from aiogram.fsm.state import (
    State, 
    StatesGroup
)

 


class Form(StatesGroup):
    photo_id = State()
    city = State()

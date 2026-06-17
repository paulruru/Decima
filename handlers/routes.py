from aiogram import (
    Router, 
    F,
    Bot
)

from aiogram.filters import (
    Command
)

from aiogram.types import (
    Message, 
    CallbackQuery,
    ReplyKeyboardMarkup, 
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile
)

from forms.user import (
    Form
)

from aiogram.fsm.context import (
    FSMContext
)

import aiohttp
import aiosqlite
import asyncio



router = Router()
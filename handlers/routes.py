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

from forms.schedule import (
    Form2
)

from aiogram.fsm.context import (
    FSMContext
)

from city import (
    get_city,
    get_time
)

import os
import aiohttp
import aiosqlite
import asyncio




router = Router()
registering = 0 #0-no, 1-yes, 2-re_registering
adding_friend = 0 

def start_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Профиль")],
            [KeyboardButton(text = "Активности")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def reg_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Зарегестрироваться")], 
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def photo_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Взять из профиля Telegram")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard
    

def city_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def profile_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Мое расписание")], 
            [KeyboardButton(text = "Заполнить профиль заново")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def re_photo_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Взять из профиля Telegram.")],
            [KeyboardButton(text = "Оставить текущее")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def re_city_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Оставить текущий")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def create_schedule_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Составить расписание")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def days_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Понедельник"), KeyboardButton(text = "Вторник")],
            [KeyboardButton(text = "Среда"), KeyboardButton(text = "Четверг"), KeyboardButton(text = "Пятница")],
            [KeyboardButton(text = "Суббота"), KeyboardButton(text = "Воскресенье"), KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def delete_days_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Понедельник."), KeyboardButton(text = "Вторник.")],
            [KeyboardButton(text = "Среда."), KeyboardButton(text = "Четверг."), KeyboardButton(text = "Пятница.")],
            [KeyboardButton(text = "Суббота."), KeyboardButton(text = "Воскресенье."), KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def types_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Зал"), KeyboardButton(text = "Бег"), KeyboardButton(text = "Турники")],
            [KeyboardButton(text = "Баскет"), KeyboardButton(text = "Валик"), KeyboardButton(text = "Футбол")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def saved_train_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Добавить тренировку")],
            [KeyboardButton(text = "Мое расписание")],
            [KeyboardButton(text = "Профиль")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard


def delete_day_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard = [
            [KeyboardButton(text = "Добавить тренировку")],
            [KeyboardButton(text = "Удалить тренировку")],
            [KeyboardButton(text = "Отмена")]
        ],
        resize_keyboard = True
    )
    return keyboard



@router.message(Command("start"))
async def start(message: Message):
    global registering
    registering = 0

    await message.answer(
        "1. Открыть профиль\n"
        "2. Мои активности\n",
        reply_markup = start_keyboard()
    )


@router.message(F.text.lower() == "профиль")
async def profile(message: Message):
    global registering
    registering = 0

    user_id = str(message.from_user.id)
    exist_users_id = [el.split(".")[0] for el in os.listdir('db/users')]
    for exist_user_id in exist_users_id:
        if user_id == exist_user_id:
            text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")

            await message.answer_photo(
                text[0], 
                caption = f"Город: {text[1].split()[0]}\nТекущий стрик: {text[2]}\nМаксимальный стрик: {text[3]}",
                reply_markup = profile_keyboard()
            )
            break
    else:
        await message.answer(
            "Вы еще не зарегестрированы",
            reply_markup = reg_keyboard()
        )
        return


@router.message(F.text.lower() == "активности")
async def active(message: Message):
    user_id = str(message.from_user.id)
    exist_users_id = [el.split(".")[0] for el in os.listdir('db/users')]
    for exist_user_id in exist_users_id:
        if user_id == exist_user_id:
            await my_schedule(message)
            break
    else:
        await message.answer(
            "Вы еще не зарегестрированы",
            reply_markup = reg_keyboard()
        )
        return
              

@router.message(F.text.lower() == "отмена")
async def cancel(message: Message, state: FSMContext):
    global registering
    registering = 0

    await state.clear()

    await start(message)


@router.message((F.text.lower() == "зарегестрироваться"))
async def register(message: Message, state: FSMContext):
    global registering
    registering = 1

    await message.answer(
            "Пришлите свое фото",
            reply_markup = photo_keyboard()
    )
    await state.set_state(Form.photo_id)


@router.message(F.text.lower() == "взять из профиля telegram")
async def auto_set_photo(message: Message, bot: Bot, state: FSMContext):
    global registering

    if registering == 1:
        photos = await bot.get_user_profile_photos(message.from_user.id)
        await state.update_data(photo_id = photos.photos[0][-1].file_id) # самое большое изображение первой (текущей) аватарки
        await message.answer(
                "Укажите ваш город",
                reply_markup = city_keyboard()
        )
        await state.set_state(Form.city)
    elif registering == 0:
        await state.clear()
        await start(message)


@router.message(Form.photo_id, F.photo)
async def proccess_photo(message: Message, state: FSMContext):
    global registering

    if registering == 1:
        photo = message.photo[-1]
        await state.update_data(photo_id = photo.file_id)
        await message.answer(
                "Укажите ваш город",
                reply_markup = city_keyboard()
        )
        await state.set_state(Form.city)
    elif registering == 2:
        await re_proccess_photo(message, state)
    else:
        await state.clear()
        await start(message)


@router.message(F.text.lower() == "оставить текущий")
async def re_keep_city(message: Message, bot: Bot, state: FSMContext):
    global registering

    if registering == 2:
        await state.update_data(city = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")[1])

        data = await state.get_data()
        await message.answer("Профиль обнавлен")
        await state.clear()

        registering = 0

        text = text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")
        open(f"db/users/{message.from_user.id}.txt", "a", encoding="utf-8").write(f"\n{data["photo_id"]}|{"".join(data["city"])}|{text[2]}|{text[3]}")

        text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")

        await message.answer_photo(
            text[0], 
            caption = f"Город: {text[1].split()[0]}\nТекущий стрик: {text[2]}\nМаксимальный стрик: {text[3]}",
            reply_markup = profile_keyboard()
        )
    elif registering == 0:
        await state.clear()
        await start(message)


@router.message(Form.city, F.text)
async def proccess_city(message: Message, state: FSMContext):
    global registering
    
    if registering == 1:
        city = get_city(message.text)
        if city:
            await state.update_data(city = city)
        else:
            await message.answer(
                "Не удалось найти город, попробуйте снова: ",
                reply_markup = city_keyboard()
            )
            return

        data = await state.get_data()
        await message.answer("Регистрация пройдена")
        await state.clear()

        registering = 0

        open(f"db/users/{message.from_user.id}.txt", "w", encoding="utf-8").write(f"{data["photo_id"]}|{" ".join(data["city"])}|0|0")
        text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")

        await message.answer_photo(
            text[0], 
            caption = f"Город: {text[1].split()[0]}\nТекущий стрик: {text[2]}\nМаксимальный стрик: {text[3]}",
            reply_markup = profile_keyboard()
        )
    elif registering == 2:
        await re_proccess_city(message, state)
    else:
        await state.clear()
        await start(message)


@router.message(F.text.lower() == "заполнить профиль заново")
async def re_register(message: Message, state: FSMContext):
    global registering
    registering = 2

    await message.answer(
            "Пришлите свое фото",
            reply_markup = re_photo_keyboard()
    )
    await state.set_state(Form.photo_id)


@router.message(Form.photo_id, F.photo)
async def re_proccess_photo(message: Message, state: FSMContext):
    if registering == 2:
        photo = message.photo[-1]
        await state.update_data(photo_id = photo.file_id)
        await message.answer(
                "Укажите ваш город",
                reply_markup = re_city_keyboard()
        )
        await state.set_state(Form.city)
    else:
        await state.clear()
        await start(message)


@router.message(F.text.lower() == "оставить текущее")
async def re_keep_photo(message: Message, state: FSMContext):
    global registering

    if registering == 2:
        await state.update_data(photo_id = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")[0])
        await message.answer(
                "Укажите ваш город",
                reply_markup = re_city_keyboard()
        )
        await state.set_state(Form.city)
    elif registering == 0:
        await state.clear()
        await start(message)


@router.message(F.text.lower() == "взять из профиля telegram.")
async def re_auto_set_photo(message: Message, bot: Bot, state: FSMContext):
    global registering

    if registering == 2: 
        photos = await bot.get_user_profile_photos(message.from_user.id)
        await state.update_data(photo_id = photos.photos[0][-1].file_id) # самое большое изображение первой (текущей) аватарки
        await message.answer(
                "Укажите ваш город",
                reply_markup = re_city_keyboard()
        )
        await state.set_state(Form.city)
    elif registering == 0:
        await state.clear()
        await start(message)


@router.message(Form.city, F.text)
async def re_proccess_city(message: Message, state: FSMContext):
    global registering

    if registering == 2:
        city = get_city(message.text)
        if city:
            await state.update_data(city = city)
        else:
            await message.answer(
                "Не удалось найти город, попробуйте снова: ",
                reply_markup = re_city_keyboard()
            )
            return

        data = await state.get_data()
        await message.answer("Профиль обнавлен")
        await state.clear()

        registering = 0

        text = text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")
        open(f"db/users/{message.from_user.id}.txt", "a", encoding="utf-8").write(f"\n{data["photo_id"]}|{" ".join(data["city"])}|{text[2]}|{text[3]}")

        text = open(f"db/users/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("\n")[-1].split("|")

        await message.answer_photo(
            text[0], 
            caption = f"Город: {text[1].split()[0]}\nТекущий стрик: {text[2]}\nМаксимальный стрик: {text[3]}\n",
            reply_markup = profile_keyboard()
        )
    else:
        await state.clear()
        await start(message)


@router.message(F.text.lower() == "мое расписание")
async def my_schedule(message: Message):
    if str(message.from_user.id) in [str(el.split(".")[0]) for el in os.listdir('db/schedule')]:
        activities = open(f"db/schedule/{message.from_user.id}.txt", "r", encoding="utf-8").read().split("|")
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        text = "".join([f"{days[i]}: {activities[i]}\n\n" for i in range(7)])
        await message.answer(
            text,
            reply_markup = delete_day_keyboard()
            )
    else:
        await message.answer(
            "Вы еще не составляли расписание",
            reply_markup = create_schedule_keyboard()
        )


@router.message(F.text.lower().in_({"составить расписание", "удалить тренировку"}))
async def create_schedule(message: Message, state: FSMContext):
    if message.text.lower() == "удалить тренировку":
        await message.answer(
            "Выбирете день недели",
            reply_markup = delete_days_keyboard()
        )
        await state.set_state(Form2.day)

    else:
        await message.answer(
            "Выбирете день недели",
            reply_markup = days_keyboard()
        )
        await state.set_state(Form2.day)


@router.message(F.text.lower().in_({"понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье", "понедельник.", "вторник.", "среда.", "четверг.", "пятница.", "суббота.", "воскресенье."}))
async def choose_day(message: Message, state: FSMContext):
    if message.text.lower() in {"понедельник.", "вторник.", "среда.", "четверг.", "пятница.", "суббота.", "воскресенье."}:
        day = message.text.lower()[:-1]
        await state.update_data(day = day)

        await state.set_state(Form2.activity)
        await state.update_data(activity = '0')

        data = await state.get_data()
        await state.clear()
        try:
            text = open(f"db/schedule/{message.from_user.id}.txt", "r", encoding="utf-8").read()
        except:
            text = f"0|0|0|0|0|0|0"

        text = text.split("|")
        days = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3, "пятница": 4, "суббота": 5, "воскресенье": 6}
        text = text[:days[data["day"]]] + [data["activity"]] + text[days[data["day"]]+1:]
        text = "|".join(text) + "\n"
        open(f"db/schedule/{message.from_user.id}.txt", "w", encoding="utf-8").write(text)

        await message.answer(
            "Тренировка удалена",
        )
        await my_schedule(message)

    else:
        day = message.text.lower()
        await state.update_data(day = day)

        await message.answer(
            "Выбирете тип тренировки",
            reply_markup = types_keyboard()
        )

        await state.set_state(Form2.activity)


@router.message(F.text.lower().in_({"зал", "бег", "турники", "баскет", "валик", "футбол"}))
async def choose_activity(message: Message, state: FSMContext):
    try:
        activity = message.text.lower()
        await state.update_data(activity = activity)

        data = await state.get_data()
        await state.clear()
        try:
            text = open(f"db/schedule/{message.from_user.id}.txt", "r", encoding="utf-8").read()
        except:
            text = f"0|0|0|0|0|0|0"

        text = text.split("|")
        days = {"понедельник": 0, "вторник": 1, "среда": 2, "четверг": 3, "пятница": 4, "суббота": 5, "воскресенье": 6}
        text = text[:days[data["day"]]] + [data["activity"]] + text[days[data["day"]]+1:]
        text = "|".join(text) + "\n"
        open(f"db/schedule/{message.from_user.id}.txt", "w", encoding="utf-8").write(text)

        await message.answer(
            "Тренировка сохранена",
        )

        await my_schedule(message)

    except Exception as e:
        print(e)
        await cancel(message, state)


@router.message(F.text.lower() == "добавить тренировку")
async def add_schedule(message: Message, state: FSMContext):
    await create_schedule(message, state)



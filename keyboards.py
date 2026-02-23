from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu(genres):
    buttons = [
        [InlineKeyboardButton(text=g, callback_data=f"genre:{g}")]
        for g in genres
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def movies_menu(movies, genre):
    buttons = [
        [InlineKeyboardButton(text=title, url=f"https://t.me/c/{message_id}")]
        for title, message_id in movies
    ]
    buttons.append([InlineKeyboardButton(text="⬅ Volver", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

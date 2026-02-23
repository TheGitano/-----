from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from database import add_movie, get_movies_by_genre, get_all_genres
from tmdb import get_movie_genre
from keyboards import main_menu, movies_menu
from config import CHANNEL_ID

router = Router()

@router.message(F.video | F.document)
async def new_movie(message: Message):
    if message.chat.id != CHANNEL_ID:
        return
    
    title = message.caption or message.video.file_name
    title = title.split("(")[0].strip()
    
    genre = await get_movie_genre(title)
    await add_movie(title, genre, message.message_id)

@router.message(F.text == "/menu")
async def show_menu(message: Message):
    genres = await get_all_genres()
    await message.answer("🎬 Selecciona un género:", reply_markup=main_menu(genres))

@router.callback_query(F.data.startswith("genre:"))
async def show_movies(callback: CallbackQuery):
    genre = callback.data.split(":")[1]
    movies = await get_movies_by_genre(genre)
    await callback.message.edit_text(
        f"🎬 {genre}",
        reply_markup=movies_menu(movies, genre)
    )

@router.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    genres = await get_all_genres()
    await callback.message.edit_text(
        "🎬 Selecciona un género:",
        reply_markup=main_menu(genres)
    )

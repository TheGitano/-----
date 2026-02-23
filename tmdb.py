import aiohttp
from config import TMDB_API_KEY

GENRE_MAP = {
    28: "Acción",
    12: "Aventura",
    16: "Animación",
    35: "Comedia",
    80: "Crimen",
    18: "Drama",
    10751: "Familiar",
    14: "Fantasía",
    27: "Terror",
    878: "Ciencia Ficción",
    53: "Suspenso"
}

async def get_movie_genre(title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}&language=es-ES"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if data["results"]:
                genre_ids = data["results"][0]["genre_ids"]
                if genre_ids:
                    return GENRE_MAP.get(genre_ids[0], "Otros")
    return "Otros"

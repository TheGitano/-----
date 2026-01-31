import os
import logging
import re
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import ParseMode
from datetime import datetime

# Configuración
TOKEN = os.environ.get('BOT_TOKEN', '8360813697:AAHN-KbnoZVIYDXBzwPXkna_4o-5b1jBYL0')
CHANNEL_ID = int(os.environ.get('CHANNEL_ID', '-1001760160216'))

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Diccionarios para almacenar contenido
peliculas = {}
apks = {}
exes = {}
htmls = {}
otros = {}

# ID del mensaje fijado
mensaje_fijado_id = None

# Géneros de películas con palabras clave
GENEROS = {
    'Acción': ['accion', 'action', 'pelea', 'fight', 'guerra', 'war', 'soldado', 'policia'],
    'Terror': ['terror', 'horror', 'miedo', 'suspenso', 'thriller', 'paranormal', 'zombi', 'demon'],
    'Comedia': ['comedia', 'comedy', 'risa', 'divertida', 'humor', 'funny'],
    'Drama': ['drama', 'emotional', 'familia', 'family'],
    'Ciencia Ficción': ['ciencia', 'ficcion', 'sci-fi', 'scifi', 'space', 'alien', 'futuro', 'robot'],
    'Animación': ['animacion', 'animation', 'animated', 'cartoon', 'disney', 'pixar'],
    'Aventura': ['aventura', 'adventure', 'viaje', 'journey', 'quest'],
    'Romance': ['romance', 'amor', 'love', 'romantica'],
    'Fantasía': ['fantasia', 'fantasy', 'magia', 'magic', 'dragon', 'wizard'],
    'Documental': ['documental', 'documentary', 'real', 'historia'],
    'Musical': ['musical', 'music', 'cantante', 'singer'],
    'Crimen': ['crimen', 'crime', 'detective', 'mafia', 'gangster'],
}

def detectar_genero(titulo):
    """Detecta el género de una película basándose en palabras clave"""
    titulo_lower = titulo.lower()
    
    # Buscar palabras clave en el título
    for genero, palabras in GENEROS.items():
        for palabra in palabras:
            if palabra in titulo_lower:
                return genero
    
    return 'Otros'

def limpiar_nombre(nombre):
    """Limpia el nombre del archivo para hacerlo más legible"""
    # Eliminar extensión
    nombre = re.sub(r'\.(mp4|mkv|avi|mov|wmv|flv|webm|apk|exe|html)$', '', nombre, flags=re.IGNORECASE)
    # Eliminar calidad y códecs comunes
    nombre = re.sub(r'\b(1080p|720p|480p|4K|HD|BluRay|WEB-DL|x264|x265|HEVC|AAC|AC3)\b', '', nombre, flags=re.IGNORECASE)
    # Eliminar caracteres especiales innecesarios
    nombre = re.sub(r'[\[\]()_]', ' ', nombre)
    # Eliminar espacios múltiples
    nombre = re.sub(r'\s+', ' ', nombre)
    return nombre.strip()

def crear_mensaje_organizado():
    """Crea el mensaje organizado con todas las categorías"""
    mensaje = "📚 **CONTENIDO ORGANIZADO** 📚\n"
    mensaje += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # PELÍCULAS
    if peliculas:
        mensaje += "🎬 **PELÍCULAS**\n\n"
        
        # Organizar por género
        peliculas_por_genero = {}
        for msg_id, data in peliculas.items():
            genero = data['genero']
            if genero not in peliculas_por_genero:
                peliculas_por_genero[genero] = []
            peliculas_por_genero[genero].append((msg_id, data))
        
        # Mostrar cada género
        for genero in sorted(peliculas_por_genero.keys()):
            mensaje += f"  🎭 **{genero}**\n"
            for msg_id, data in sorted(peliculas_por_genero[genero], key=lambda x: x[1]['nombre']):
                mensaje += f"     • [{data['nombre']}](https://t.me/c/{str(CHANNEL_ID)[4:]}/{msg_id})\n"
            mensaje += "\n"
        
        mensaje += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # APLICACIONES APK
    if apks:
        mensaje += "📱 **APLICACIONES (APK)**\n\n"
        for msg_id, data in sorted(apks.items(), key=lambda x: x[1]['nombre']):
            mensaje += f"  • [{data['nombre']}](https://t.me/c/{str(CHANNEL_ID)[4:]}/{msg_id})\n"
        mensaje += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # PROGRAMAS EXE
    if exes:
        mensaje += "💻 **PROGRAMAS (EXE)**\n\n"
        for msg_id, data in sorted(exes.items(), key=lambda x: x[1]['nombre']):
            mensaje += f"  • [{data['nombre']}](https://t.me/c/{str(CHANNEL_ID)[4:]}/{msg_id})\n"
        mensaje += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # ARCHIVOS HTML
    if htmls:
        mensaje += "🌐 **PÁGINAS WEB (HTML)**\n\n"
        for msg_id, data in sorted(htmls.items(), key=lambda x: x[1]['nombre']):
            mensaje += f"  • [{data['nombre']}](https://t.me/c/{str(CHANNEL_ID)[4:]}/{msg_id})\n"
        mensaje += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    # OTROS ARCHIVOS
    if otros:
        mensaje += "📦 **OTROS ARCHIVOS**\n\n"
        for msg_id, data in sorted(otros.items(), key=lambda x: x[1]['nombre']):
            mensaje += f"  • [{data['nombre']}](https://t.me/c/{str(CHANNEL_ID)[4:]}/{msg_id})\n"
        mensaje += "\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    mensaje += f"🔄 Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
    mensaje += "✨ Bot: @OrganizadordeGrupoBot"
    
    return mensaje

async def actualizar_mensaje_fijado(context: ContextTypes.DEFAULT_TYPE):
    """Actualiza o crea el mensaje fijado con el contenido organizado"""
    global mensaje_fijado_id
    
    mensaje = crear_mensaje_organizado()
    
    try:
        if mensaje_fijado_id:
            # Actualizar mensaje existente
            await context.bot.edit_message_text(
                chat_id=CHANNEL_ID,
                message_id=mensaje_fijado_id,
                text=mensaje,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            logger.info("Mensaje fijado actualizado")
        else:
            # Crear nuevo mensaje y fijarlo
            msg = await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=mensaje,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
            await context.bot.pin_chat_message(
                chat_id=CHANNEL_ID,
                message_id=msg.message_id,
                disable_notification=True
            )
            mensaje_fijado_id = msg.message_id
            logger.info(f"Nuevo mensaje fijado creado: {mensaje_fijado_id}")
    except Exception as e:
        logger.error(f"Error al actualizar mensaje fijado: {e}")

async def escanear_canal_completo(context: ContextTypes.DEFAULT_TYPE):
    """Escanea todo el historial del canal para organizar contenido existente"""
    logger.info("Iniciando escaneo completo del canal...")
    
    try:
        # Obtener información del chat
        chat = await context.bot.get_chat(CHANNEL_ID)
        logger.info(f"Escaneando canal: {chat.title}")
        
        # Telegram no permite obtener todo el historial directamente
        # Intentamos desde mensaje 1 hasta un número alto
        mensaje_count = 0
        for i in range(1, 10000):  # Ajusta según tu canal
            try:
                # Intentar reenviar el mensaje al bot (método indirecto)
                # Como no podemos hacer forward, usamos copy_message
                msg = await context.bot.copy_message(
                    chat_id=CHANNEL_ID,
                    from_chat_id=CHANNEL_ID,
                    message_id=i
                )
                # Eliminar el mensaje copiado inmediatamente
                await context.bot.delete_message(
                    chat_id=CHANNEL_ID,
                    message_id=msg.message_id
                )
                mensaje_count += 1
            except Exception:
                continue
        
        logger.info(f"Escaneo completado. Mensajes encontrados: {mensaje_count}")
    except Exception as e:
        logger.error(f"Error en escaneo completo: {e}")

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa cada mensaje nuevo en el canal"""
    message = update.channel_post or update.message
    
    if not message:
        return
    
    # Solo procesar mensajes del canal específico
    if message.chat.id != CHANNEL_ID:
        return
    
    logger.info(f"Procesando mensaje {message.message_id}")
    
    # Detectar tipo de contenido
    nombre = None
    tipo = None
    
    if message.document:
        nombre = message.document.file_name
        if nombre.lower().endswith('.apk'):
            tipo = 'apk'
        elif nombre.lower().endswith('.exe'):
            tipo = 'exe'
        elif nombre.lower().endswith('.html'):
            tipo = 'html'
        else:
            tipo = 'otro'
    
    elif message.video:
        nombre = message.caption or message.video.file_name or "Video sin título"
        tipo = 'pelicula'
    
    elif message.text and message.text.startswith('/'):
        # Ignorar comandos
        return
    
    # Si hay contenido para organizar
    if nombre and tipo:
        nombre_limpio = limpiar_nombre(nombre)
        msg_id = message.message_id
        
        data = {
            'nombre': nombre_limpio,
            'original': nombre,
            'fecha': datetime.now().strftime('%d/%m/%Y')
        }
        
        if tipo == 'pelicula':
            genero = detectar_genero(nombre_limpio)
            data['genero'] = genero
            peliculas[msg_id] = data
            logger.info(f"Película agregada: {nombre_limpio} - Género: {genero}")
        
        elif tipo == 'apk':
            apks[msg_id] = data
            logger.info(f"APK agregado: {nombre_limpio}")
        
        elif tipo == 'exe':
            exes[msg_id] = data
            logger.info(f"EXE agregado: {nombre_limpio}")
        
        elif tipo == 'html':
            htmls[msg_id] = data
            logger.info(f"HTML agregado: {nombre_limpio}")
        
        else:
            otros[msg_id] = data
            logger.info(f"Otro archivo agregado: {nombre_limpio}")
        
        # Actualizar mensaje fijado
        await actualizar_mensaje_fijado(context)

async def post_init(application: Application):
    """Se ejecuta después de iniciar el bot"""
    logger.info("Bot iniciado correctamente")
    # Escanear canal al iniciar (comentado por ahora, activar si es necesario)
    # await escanear_canal_completo(application)

def main():
    """Función principal"""
    logger.info("Iniciando bot organizador...")
    
    # Crear aplicación
    application = Application.builder().token(TOKEN).post_init(post_init).build()
    
    # Handlers para mensajes del canal
    application.add_handler(MessageHandler(
        filters.ChatType.CHANNEL & (filters.Document.ALL | filters.VIDEO),
        procesar_mensaje
    ))
    
    # Iniciar bot
    logger.info("Bot en ejecución...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()

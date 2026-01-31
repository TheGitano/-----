# 🤖 Bot Organizador de Contenido para Telegram

Bot automatizado que organiza todo el contenido de tu canal de Telegram (películas, APKs, EXEs, HTMLs) en categorías con enlaces directos.

## 🌟 Características

- ✅ **Organización automática** de contenido por tipo y género
- 🎬 **Películas** organizadas por género (Acción, Terror, Comedia, etc.)
- 📱 **APKs** - Aplicaciones Android
- 💻 **EXEs** - Programas Windows  
- 🌐 **HTMLs** - Páginas web
- 📌 **Mensaje fijado** actualizado automáticamente
- 🔍 **Búsqueda fácil** por nombre en el canal
- 🔄 **Detección automática** de contenido nuevo

## 📋 Requisitos

- Python 3.11+
- Cuenta de Telegram
- Bot de Telegram (creado con @BotFather)
- Cuenta de Railway (gratis)
- Cuenta de GitHub

## 🚀 Instalación y Despliegue

### 1️⃣ Preparar el repositorio en GitHub

1. Ve a [GitHub](https://github.com) e inicia sesión
2. Crea un nuevo repositorio:
   - Nombre: `telegram-content-organizer`
   - Visibilidad: Privado (recomendado)
   - ✅ Marca "Add a README file"
3. Clona o descarga este código
4. Sube los archivos al repositorio:
   - `bot.py`
   - `requirements.txt`
   - `Procfile`
   - `runtime.txt`
   - `.gitignore`
   - `README.md`

### 2️⃣ Configurar en Railway

1. Ve a [Railway.app](https://railway.app) e inicia sesión con GitHub
2. Click en "New Project"
3. Selecciona "Deploy from GitHub repo"
4. Elige tu repositorio `telegram-content-organizer`
5. Railway detectará automáticamente que es un proyecto Python

### 3️⃣ Configurar Variables de Entorno

En Railway, ve a tu proyecto → "Variables" y agrega:

```
BOT_TOKEN = 8360813697:AAHN-KbnoZVIYDXBzwPXkna_4o-5b1jBYL0
CHANNEL_ID = -1001760160216
```

### 4️⃣ Desplegar

1. Railway desplegará automáticamente el bot
2. Espera unos minutos
3. Verifica los logs en Railway para confirmar que está funcionando

## 🎯 Cómo Usar

### Configuración Inicial

1. **Agrega el bot como administrador** de tu canal con estos permisos:
   - ✅ Publicar mensajes
   - ✅ Editar mensajes
   - ✅ Eliminar mensajes
   - ✅ Fijar mensajes

2. **El bot organizará automáticamente**:
   - Todo el contenido que subas desde ahora
   - Detectará películas, APKs, EXEs y HTMLs
   - Creará un mensaje fijado con todas las categorías

### Subir Contenido

Simplemente sube archivos a tu canal:

- **🎬 Películas**: Videos con nombre (el bot detecta el género automáticamente)
- **📱 APKs**: Archivos .apk
- **💻 EXEs**: Archivos .exe
- **🌐 HTMLs**: Archivos .html

El bot los organizará automáticamente y actualizará el mensaje fijado.

## 📊 Estructura del Mensaje Fijado

```
📚 CONTENIDO ORGANIZADO 📚
━━━━━━━━━━━━━━━━━━━━━━━

🎬 PELÍCULAS

  🎭 Acción
     • Depredador: Tierras Salvajes
     • Avatar: El Sentido del Agua
  
  😱 Terror
     • [Próximamente]

━━━━━━━━━━━━━━━━━━━━━━━

📱 APLICACIONES (APK)
  • App 1
  • App 2

━━━━━━━━━━━━━━━━━━━━━━━

💻 PROGRAMAS (EXE)
  • Programa 1

🔄 Última actualización: 31/01/2026 17:30
```

## 🔧 Personalización

### Cambiar Géneros de Películas

Edita el diccionario `GENEROS` en `bot.py`:

```python
GENEROS = {
    'Tu Género': ['palabra1', 'palabra2', 'keyword'],
    # ...
}
```

### Cambiar Formato del Mensaje

Modifica la función `crear_mensaje_organizado()` en `bot.py`

## 🐛 Solución de Problemas

### El bot no responde
- Verifica que esté corriendo en Railway (logs)
- Confirma que las variables de entorno están configuradas
- Asegúrate que el bot sea admin del canal

### No organiza contenido antiguo
- El bot solo procesa contenido nuevo por defecto
- Para organizar contenido antiguo, descomenta la línea en `post_init()`

### Errores de permisos
- Verifica que el bot tenga todos los permisos de administrador
- Intenta removerlo y agregarlo de nuevo

## 📝 Notas

- El bot se ejecuta 24/7 en Railway (gratis con límites)
- Railway ofrece 500 horas gratis al mes
- Los datos se almacenan en memoria (se reinician al reiniciar el bot)
- Para persistencia permanente, considera agregar una base de datos

## 🤝 Soporte

Si tienes problemas:
1. Revisa los logs en Railway
2. Verifica que todas las configuraciones estén correctas
3. Asegúrate que el bot tenga permisos de admin

## 📜 Licencia

Uso personal y educativo.

---

**Creado con ❤️ para organizar tu contenido de Telegram**

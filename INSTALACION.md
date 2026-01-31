# 🚀 GUÍA RÁPIDA DE INSTALACIÓN

## Paso 1: Subir a GitHub

1. Ve a https://github.com
2. Click en "New repository"
3. Nombre: `organizador-telegram-bot`
4. Privado ✅
5. Click "Create repository"

6. Descarga todos estos archivos y súbelos:
   - bot.py
   - requirements.txt
   - Procfile
   - runtime.txt
   - .gitignore
   - README.md

## Paso 2: Conectar con Railway

1. Ve a https://railway.app
2. Inicia sesión con tu cuenta de GitHub
3. Click "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige `organizador-telegram-bot`

## Paso 3: Configurar Variables

En Railway, click en "Variables" y agrega:

```
BOT_TOKEN=8360813697:AAHN-KbnoZVIYDXBzwPXkna_4o-5b1jBYL0
CHANNEL_ID=-1001760160216
```

## Paso 4: Desplegar

Railway desplegará automáticamente. Espera 2-3 minutos.

## Paso 5: Verificar

1. Ve a "Logs" en Railway
2. Deberías ver: "Bot iniciado correctamente"
3. Sube un video a tu canal
4. El bot lo organizará automáticamente

## ✅ ¡Listo!

Tu bot ya está funcionando 24/7.

## 🎬 Prueba

1. Sube un video o archivo a tu canal
2. El bot lo detectará automáticamente
3. Verás el mensaje fijado actualizado
4. Cada archivo tendrá un enlace directo

---

## ⚠️ Importante

- El bot DEBE ser administrador del canal
- Dale estos permisos:
  - Publicar mensajes ✅
  - Editar mensajes ✅
  - Eliminar mensajes ✅
  - Fijar mensajes ✅

## 🆘 ¿Problemas?

1. Revisa los logs en Railway
2. Verifica que el bot sea admin
3. Confirma que las variables estén correctas

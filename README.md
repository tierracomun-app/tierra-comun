# 🌍 Tierra Común

Somos de la tierra. Migrar es compartir.

App web progresiva (PWA), gratuita y de código abierto, para personas migrantes, refugiadas y nómadas: guía de derechos con fuentes oficiales, recursos cercanos, comunidad anónima, modo emergencia y un asistente que funciona **sin internet**.

> ⚠️ No es asesoría legal. Usa solo abogados con licencia o representantes acreditados por el Departamento de Justicia (DOJ). Nunca un "notario".

## Funciones
- **Guía** (EE. UU. por ahora) con cada dato enlazado a su fuente oficial.
- **Recursos**: directorios oficiales (EOIR pro bono, HRSA, 211, Feeding America…).
- **Comunidad** (demo): foro por ciudad, anónimo, guardado solo en tu teléfono.
- **Asistente**: preguntas guiadas con botones + texto libre (sin acentos, con errores de escritura). 100 % sin conexión. IA en el dispositivo opcional (WebLLM, descarga grande).
- **Emergencia**: seguridad, documentos, derecho internacional de refugiados y desplazados, contactos (ACNUR, OIM, CICR) y lista de verificación.
- **Privacidad**: sin cuentas, sin rastreo, sin guardar conversaciones.

## Usar localmente
```
python3 -m http.server 8642   # luego abre http://localhost:8642
```
Para publicarla gratis: GitHub Pages o Netlify (solo archivos estáticos).

## Agregar países o idiomas
- País: `data/<pais>.json`, `data/emergency/<pais>.json`.
- Idioma: `i18n/<idioma>.json` y campos `<idioma>` en los datos.
- Al cambiar contenido, sube la versión de caché en `sw.js` (`tc-vN`).

## Servidor opcional
`server/server.py` es opcional. Solo si quieres conectar un modelo propio (por ejemplo Ollama local y gratuito) vía `LLM_BASE_URL`/`LLM_MODEL`.

## Licencias
Código: MIT. Contenido (`data/`, `i18n/`): CC BY-SA 4.0. Ver `LICENSE`.

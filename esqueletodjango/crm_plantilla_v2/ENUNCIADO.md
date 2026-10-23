# ENUNCIADO v2 – Adapta y amplía un CRM en Django (temática libre)

## 1. Punto de partida (ya funciona)
Arranca con `iniciar.sh` / `iniciar.bat`. Verás un CRM genérico con datos de ejemplo (usuario `admin`, clave `admin1234`). Antes de tocar nada, **recórrelo entero**: panel, listados, buscar, crear, editar, borrar y la ficha de un contacto.

Cada archivo está comentado línea a línea con los valores posibles. Las tareas están marcadas con `TODO-ALUMNO n` en el código.

## 2. Flujo de trabajo (repítelo siempre)
1. Cambia `models.py`.
2. `python manage.py makemigrations` y `python manage.py migrate` (o vuelve a ejecutar `iniciar`).
3. Refleja el cambio en `forms.py` (fields), `admin.py` (list_display) y `lista.html` (columnas).
4. Prueba en el navegador. Si algo falla, lee la **última línea** del error en la terminal.

## 3. Tareas

### Nivel 1 – Personalizar (obligatorio)
- **TODO 0**: en `settings.py` cambia `NOMBRE_CRM`, `COLOR_PRINCIPAL` y, si procede, `LANGUAGE_CODE`/`TIME_ZONE`. Escribe `TEMATICA.md` (5 líneas): qué es tu CRM y quiénes son los "contactos".
- **TODO 1**: en `contactos/models.py` cambia los `TIPOS` por los de tu temática.
- **TODO 2**: añade 2 campos propios al contacto (ej.: `fecha_nacimiento`, `ciudad`, `dorsal`, `matricula`). Llévalos a forms, admin, lista y detalle.
- **TODO 3**: cambia las `ETAPAS` de oportunidades a tu temática (mínimo 4). Ojo: el panel suma las oportunidades con etapa `ganado`; si renombras ese valor, actualiza `core/views.py`.
- **TODO 4**: añade un canal nuevo a interacciones.
- **TODO 5**: añade `prioridad` (con `choices`) a tareas.
- **TODO 10**: sustituye los datos de `cargar_ejemplo.py` por datos de tu temática (mín. 8 contactos). Para recargar: borra `db.sqlite3` y ejecuta `iniciar`.

### Nivel 2 – Ampliar (obligatorio)
- **TODO 6**: ajusta las columnas de los 4 listados a tus campos.
- **TODO 7**: filtro por `tipo` en contactos y por `etapa` en oportunidades (desplegable en el listado + `filter()` en la vista).
- **TODO 8**: en la ficha de la oportunidad, botón "Marcar como ganada" (vista que cambia `etapa` y guarda, solo por POST).
- **TODO 9**: añade al panel una métrica propia (ej.: tareas vencidas con `vence__lt=date.today()`).

### Nivel 3 – Funcionalidades CRM (elige 2)
- Importe total por etapa en oportunidades (`values('etapa').annotate(Sum('importe'))`).
- Paginación del listado de contactos (`Paginator`, 10 por página).
- Exportar contactos a CSV (`HttpResponse` con `content_type='text/csv'`).
- Etiquetas para contactos con `ManyToManyField`.
- Marcar tarea como hecha con un clic desde el listado.
- Que cada usuario vea solo sus tareas (nuevo campo `asignada_a`).

### Nivel 4 – Modular (opcional, +nota)
Crea un módulo nuevo propio (ej.: `eventos`, `productos`): `python manage.py startapp eventos`, copia la estructura de `tareas`, añade `'eventos'` a `MODULOS_CRM` y comprueba que aparece en el menú.

## 4. Reglas
- Comenta el código nuevo que escribas, igual que el existente.
- No subas `venv/` ni `db.sqlite3`.
- No uses `fields='__all__'` en el formulario de interacciones (el autor se asigna en la vista).
- Si desactivas un módulo, elimina su bloque en `contactos/templates/contactos/detalle.html`.

## 5. Entrega
`.zip` sin `venv/` ni `db.sqlite3`, con `TEMATICA.md` y `LEEME.txt` (credenciales + lista de TODOs hechos). Debe arrancar con `iniciar` en un equipo limpio.

## 6. Rúbrica (10 puntos)
| Criterio | Puntos |
|---|---|
| Personalización y temática coherente (Nivel 1) | 3 |
| Filtros, acción de ganar y métrica (Nivel 2) | 3 |
| Funcionalidades CRM elegidas (Nivel 3) | 2 |
| Comentarios y calidad del código | 1 |
| Datos de ejemplo y funcionamiento sin errores | 1 |
| Módulo propio (Nivel 4) | +1 |

## 7. Errores típicos
- `no such table` / `no such column`: falta `makemigrations` + `migrate`.
- `NoReverseMatch`: nombre de URL o `app_name` mal escrito en la etiqueta `url`.
- `TemplateDoesNotExist`: la ruta debe ser `<app>/templates/<app>/archivo.html`.
- `CSRF verification failed`: falta `csrf_token` en un formulario POST.
- Cambié un modelo y no lo veo en el formulario: olvidaste añadirlo a `fields` en `forms.py`.

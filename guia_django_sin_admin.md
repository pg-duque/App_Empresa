# Instalar Django en el PC de clase (sin permisos de administrador)

Funciona con un **entorno virtual (venv)**: todo se instala dentro de tu carpeta y no toca el sistema.

## Paso 0: instalar Python (solo si no lo tienes)

Comprueba primero si lo tienes. Abre Git Bash, PowerShell o cmd y escribe:

```
python --version
```

Si te devuelve algo como `Python 3.12.x`, salta al siguiente apartado. Si dice que no se reconoce, prueba con `py --version`. Si tampoco, instálalo **solo para tu usuario**, lo cual no necesita administrador:

1. Descarga el instalador de Windows (64-bit) desde https://www.python.org/downloads/
2. Ábrelo y, en la primera pantalla, **marca la casilla "Add python.exe to PATH"**.
3. Pulsa **Install Now** (no "Customize"). La opción por defecto instala en tu carpeta de usuario y no pide permisos de administrador.
4. Al terminar, **cierra y vuelve a abrir** la terminal (si no, no verá el cambio) y comprueba:

```
python --version
```

Si el instalador pide contraseña de administrador o está bloqueado, el PC tiene restricciones: pregunta al profe. Otra opción es la versión de Python de la **Microsoft Store**, si la tienda no está bloqueada.

> Ojo: la versión "embeddable/portable zip" de python.org **no sirve** para esto, porque no incluye `venv` ni `pip`.

## Opción rápida: script

1. Abre **Git Bash** (clic derecho en una carpeta → *Git Bash Here*, o desde el menú Inicio).
2. Ve a la carpeta donde esté `instalar_django.sh` y ejecuta:

```
bash instalar_django.sh /c/Django miproyecto
```

Los dos datos que le pasas son:

- **Primero: la carpeta** donde se instalará todo (`/c/Django`). Si no lo pones, usa una carpeta `django-clase` dentro de donde estés.
- **Segundo: el nombre del proyecto** (`miproyecto`). Sin espacios ni guiones, y que no se llame `django`.

Qué hace, en orden:

1. Busca Python (`python` o `py`). Si no lo encuentra, se para y te avisa: instálalo con el Paso 0.
2. Crea la carpeta y el entorno virtual `venv` (si ya existen, no los vuelve a crear).
3. Instala la **versión estable** de Django con `pip install django`.
4. Crea el proyecto (si ya existe, lo deja como está).
5. Al final imprime los comandos para activar el entorno y arrancar el servidor.

El script no deja el entorno activado en tu terminal: después tienes que activarlo tú (la tabla del apartado manual dice cómo según la terminal).

**Cuándo se ejecuta:** una sola vez, justo después de tener Python instalado. Es la instalación inicial, no algo que se lance cada vez que trabajes. Para el día a día mira el apartado "Cada vez que vuelvas a trabajar" (al final de esta guía).

> Si falla, usa la opción manual de abajo para ver en qué paso se atasca.

## Opción manual

**1. Comprueba Python**

```
python --version
```

Si no lo reconoce, prueba `py --version`.

**2. Crea la carpeta y el entorno virtual**

```
mkdir /c/Django
cd /c/Django
python -m venv venv
```

**3. Activa el entorno** (depende de la terminal que uses)

| Terminal | Comando |
|---|---|
| Git Bash (`MINGW64` en el prompt) | `source venv/Scripts/activate` |
| PowerShell (`PS C:\...>`) | `.\venv\Scripts\Activate.ps1` |
| cmd | `venv\Scripts\activate` |

Si PowerShell bloquea el script, ejecuta antes (solo afecta a esa ventana, sin admin):

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Sabrás que está activo porque verás **(venv)** al principio de la línea.

**4. Instala Django**

```
pip install django
python -m django --version
```

**5. Crea un proyecto y arráncalo**

```
django-admin startproject miproyecto
cd miproyecto
python manage.py runserver
```

Abre http://127.0.0.1:8000 : si ves el cohete de Django, funciona. Para parar el servidor: `Ctrl+C`.

## Usarlo con VS Code

1. *Archivo → Abrir carpeta* → `C:\Django\miproyecto`.
2. `Ctrl+Shift+P` → **Python: Select Interpreter** → `C:\Django\venv\Scripts\python.exe` (hace falta la extensión *Python* de Microsoft).
3. Terminal integrada: `Ctrl+ñ`.

## Errores típicos

- **`python` no se reconoce justo después de instalarlo**: cierra y abre la terminal. Si sigue igual, reinstala marcando "Add python.exe to PATH" o usa `py` en lugar de `python`.
- **`venvScriptsactivate: command not found`**: estás en Git Bash y has usado `\`. Usa `source venv/Scripts/activate`.
- **`source` no se reconoce**: estás en PowerShell. Usa `.\venv\Scripts\Activate.ps1`.
- **`does not appear to be a Python project`**: has hecho `pip install -e .` en una carpeta sin `pyproject.toml`. Para clase basta con `pip install django`.
- **pip no conecta**: puede haber proxy. Pregunta al profe o usa `pip install --proxy http://usuario:clave@servidor:puerto django`.
- **Se borra todo al reiniciar el PC** (el equipo restaura el disco): guarda tu proyecto en un pendrive, en tu carpeta de red o en GitHub. Al volver a empezar, vuelve a ejecutar el script (`bash instalar_django.sh /c/Django miproyecto`) para recrear el venv e instalar Django, y luego copia tu proyecto encima. Si Python tampoco se conserva tras el reinicio, hay que reinstalarlo antes con el Paso 0.

## Cada vez que vuelvas a trabajar

```
cd /c/Django
source venv/Scripts/activate      # o la versión de tu terminal
cd miproyecto
python manage.py runserver
```

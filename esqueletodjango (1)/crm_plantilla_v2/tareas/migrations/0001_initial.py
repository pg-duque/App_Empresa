# Archivo de migración generado automáticamente por Django.
# Registra cambios en los modelos para poder aplicarlos a la base de datos.

# Importa las opciones para definir qué ocurre al borrar objetos relacionados.
import django.db.models.deletion

# Importa las herramientas para describir cambios en modelos y campos.
from django.db import migrations, models


# Define esta migración, es decir, este conjunto de cambios para la base de datos.
class Migration(migrations.Migration):

    # Indica que es la primera migración de esta aplicación.
    initial = True

    # Migraciones que deben aplicarse antes que esta.
    # En este caso, primero debe existir el modelo Contacto de la app contactos.
    dependencies = [
        ('contactos', '0001_initial'),
    ]

    # Lista de cambios que esta migración aplicará.
    operations = [
        # Crea una tabla nueva para el modelo Tarea.
        migrations.CreateModel(
            # Nombre del modelo que se está creando.
            name='Tarea',

            # Define las columnas de la tabla.
            fields=[
                # Identificador único de cada tarea.
                # Django lo crea automáticamente: es la clave primaria de la tabla.
                # BigAutoField es un número entero grande que aumenta automáticamente.
                ('id', models.BigAutoField(
                    auto_created=True,
                    primary_key=True,
                    serialize=False,
                    verbose_name='ID'
                )),

                # Columna de texto para el título, con un máximo de 150 caracteres.
                ('titulo', models.CharField(max_length=150)),

                # Columna para guardar la fecha de vencimiento.
                # Como no tiene null=True ni blank=True, la fecha es obligatoria.
                ('vence', models.DateField()),

                # Columna verdadera/falsa que indica si la tarea está hecha.
                # Las tareas nuevas comienzan sin marcar como hechas.
                ('hecha', models.BooleanField(default=False)),

                # Relaciona la tarea con un contacto.
                # blank=True permite dejarlo vacío en formularios.
                # null=True permite que la base de datos guarde la tarea sin contacto.
                # CASCADE significa que, si se borra el contacto relacionado,
                # también se borran sus tareas.
                # related_name permite consultar las tareas desde un contacto:
                # contacto.tareas.all()
                ('contacto', models.ForeignKey(
                    blank=True,
                    null=True,
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='tareas',
                    to='contactos.contacto'
                )),
            ],

            # Opciones adicionales del modelo.
            options={
                # Ordena primero por el valor de "hecha" y después por "vence".
                # False va antes que True, así que las tareas pendientes aparecen
                # primero; dentro de cada grupo, las más próximas vencen antes.
                'ordering': ['hecha', 'vence'],
            },
        ),
    ]

# Herramientas para ejecutar una transformación de datos al migrar el proyecto.
from django.db import migrations


def normalizar_etapas(apps, schema_editor):
    """Corrige los valores antiguos sin borrar oportunidades del alumno."""
    # Obtiene la versión histórica del modelo que corresponde a esta migración.
    Oportunidad = apps.get_model('oportunidades', 'Oportunidad')
    # Usa la conexión de la migración, también al ejecutar las pruebas.
    objetos = Oportunidad.objects.using(schema_editor.connection.alias)
    # Sustituye la negociación de la plantilla por la etapa equivalente del club.
    objetos.filter(etapa='negociacion').update(etapa='en_proceso')
    # Conserva las ventas ganadas al renombrarlas como contactos fidelizados.
    objetos.filter(etapa='ganado').update(etapa='fidelizado')


# Django descubre esta clase y ejecuta sus operaciones en el orden indicado.
class Migration(migrations.Migration):
    # Primero deben existir las etapas personalizadas de la migración anterior.
    dependencies = [('oportunidades', '0002_alter_oportunidad_etapa')]
    # La adaptación es irreversible: fidelizado ya existía antes de migrar.
    operations = [migrations.RunPython(normalizar_etapas)]

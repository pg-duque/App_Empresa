"""Utilidades compartidas (ya hechas, no hace falta tocar)."""

def campos_de(obj):
    """Devuelve [(etiqueta, valor), ...] de un objeto para mostrarlo en la ficha de detalle."""
    resultado = []
    for f in obj._meta.fields:                 # _meta.fields = todas las columnas del modelo
        if f.name == 'id':                     # Ocultamos el id
            continue
        if f.choices:                          # Si el campo tiene choices, mostramos el texto visible
            valor = getattr(obj, f'get_{f.name}_display')()
        else:
            valor = getattr(obj, f.name)
        if isinstance(valor, bool):            # True/False -> Sí/No
            valor = 'Sí' if valor else 'No'
        elif valor in (None, ''):
            valor = '—'
        resultado.append((str(f.verbose_name).capitalize(), valor))
    return resultado

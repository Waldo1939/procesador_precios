def normalize_quantity(cantidad, unidad_original, pack=1):


    if cantidad is None or unidad_original is None:
        return None, None

    cantidad_total = cantidad * pack
    unidad_original = unidad_original.lower()


    if unidad_original in ["gr", "gramos", "g", "grs"]:
        return cantidad_total / 1000, "KG"

    if unidad_original in ["ml", "mililitros"]:
        return cantidad_total / 1000, "LT"

    if unidad_original in ["kg", "kilo", "kilos"]:
        return cantidad_total, "KG"

    if unidad_original in ["lt", "litros"]:
        return cantidad_total, "LT"

    if unidad_original in ["unidad", "un", "u"]:
        return cantidad_total, "UD"

    if unidad_original == "pack":
        return cantidad_total, "PAQ"

    return None, None

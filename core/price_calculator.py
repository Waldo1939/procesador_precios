def clean_price(precio):
    """
    Limpia strings tipo '$672.803.193' y los convierte a float correcto.
    """

    if precio is None:
        return None

    if isinstance(precio, str):
        precio = precio.replace("$", "").replace(".", "").replace(",", ".")
        try:
            return float(precio)
        except:
            return None

    return float(precio)


def calculate_standard_price(precio, cantidad_normalizada):
    """
    Calcula precio por unidad estándar (KG, LT o UD).
    """

    if precio is None or cantidad_normalizada in (None, 0):
        return None

    try:
        return precio / cantidad_normalizada
    except Exception:
        return None

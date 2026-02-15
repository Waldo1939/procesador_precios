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

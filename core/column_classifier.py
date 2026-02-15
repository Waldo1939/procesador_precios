def classify_columns(columns: list) -> dict:
    """
    Clasifica columnas detectadas en:
    producto, precio
    """

    mapping = {
        "producto": None,
        "precio": None,
        "codigo": None,
    }

    for col in columns:
        col_lower = col.lower()

        # Producto
        if any(word in col_lower for word in ["articulo", "producto", "descripcion", "item"]):
            mapping["producto"] = col

        # Precio
        elif any(word in col_lower for word in ["precio unit", "p. unit", "precio"]):
            mapping["precio"] = col

        # Código
        elif "codigo" in col_lower:
            mapping["codigo"] = col

    return mapping

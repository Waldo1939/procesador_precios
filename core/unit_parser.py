import re


def extract_quantity_and_unit(text: str):

    if not isinstance(text, str):
        return None, None, 1

    text = text.lower()

    # Detectar pack
    pack_pattern = r'(\d+)\s?[xX]\s?(\d+(?:[\.,]\d+)?)\s?(kg|kilo|kilos|gr|g|grs|ml|lt|litros|unidad|un|u)\b'
    pack_match = re.search(pack_pattern, text)

    if pack_match:
        pack = int(pack_match.group(1))
        cantidad = float(pack_match.group(2).replace(",", "."))
        unidad = pack_match.group(3)
        return cantidad, unidad, pack

    # Detectar simple
    pattern = r'(\d+(?:[\.,]\d+)?)\s?(kg|kilo|kilos|gr|g|grs|ml|lt|litros|unidad|un|u)\b'
    match = re.search(pattern, text)

    if match:
        cantidad = float(match.group(1).replace(",", "."))
        unidad = match.group(2)
        return cantidad, unidad, 1

    return None, None, 1

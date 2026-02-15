import os

def detect_provider(file_path: str):
    """
    Detecta proveedor basado en nombre del archivo.
    Ej: 'arcor_lista_enero.xlsx' → 'ARCOR'
    """
    filename = os.path.basename(file_path)
    provider_name = filename.split("_")[0]

    return provider_name.upper()

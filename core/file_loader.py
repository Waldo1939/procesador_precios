import os

SUPPORTED_EXTENSIONS = [".xlsx", ".xls", ".pdf"]

def list_input_files(input_folder: str):
    """
    Devuelve una lista de archivos válidos dentro de la carpeta input.
    """
    files = []

    for file in os.listdir(input_folder):
        ext = os.path.splitext(file)[1].lower()
        if ext in SUPPORTED_EXTENSIONS:
            files.append(os.path.join(input_folder, file))

    return files

import os
import pandas as pd
import pdfplumber


def extract_table(file_path: str) -> pd.DataFrame:
    """
    Detecta tipo de archivo y extrae tabla como DataFrame.
    """

    extension = os.path.splitext(file_path)[1].lower()

    if extension in [".xlsx", ".xls"]:
        return _extract_excel(file_path)

    elif extension == ".pdf":
        return _extract_pdf(file_path)

    else:
        raise ValueError(f"Formato no soportado: {extension}")


def _extract_excel(file_path: str) -> pd.DataFrame:
    try:
        df = pd.read_excel(file_path)
        df.columns = df.columns.str.strip().str.lower()
        return df
    except Exception as e:
        print(f"Error leyendo Excel: {e}")
        return pd.DataFrame()


def _extract_pdf(file_path: str) -> pd.DataFrame:
    rows = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    rows.extend(table)

        if not rows:
            return pd.DataFrame()

        df = pd.DataFrame(rows[1:], columns=rows[0])
        df.columns = df.columns.str.strip().str.lower()
        return df

    except Exception as e:
        print(f"Error leyendo PDF: {e}")
        return pd.DataFrame()

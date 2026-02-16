from core.file_loader import list_input_files
from core.provider_detector import detect_provider
from core.table_extractor import extract_table
from core.column_classifier import classify_columns
from core.unit_parser import extract_quantity_and_unit
from core.unit_normalizer import normalize_quantity
from core.price_calculator import calculate_standard_price, clean_price
from core.ai_extractor import extract_with_gemini
import pandas as pd


INPUT_FOLDER = "input_files"
def procesar_dataframe(df, producto_col="producto", precio_col="precio"):

        df["cantidad_normalizada"] = None
        df["unidad_estandar"] = None
        df["precio_estandar"] = None
        df["origen_precio"] = None

        for idx, row in df.iterrows():

            producto = row.get(producto_col)
            precio_unit = clean_price(row.get(precio_col))
            origen_precio = "directo"

            cantidad, unidad, pack = extract_quantity_and_unit(producto)
            cantidad_norm, unidad_std = normalize_quantity(cantidad, unidad, pack)

            precio_estandar = None
            if precio_unit and cantidad_norm:
                precio_estandar = calculate_standard_price(precio_unit, cantidad_norm)

            df.at[idx, "cantidad_normalizada"] = cantidad_norm
            df.at[idx, "unidad_estandar"] = unidad_std
            df.at[idx, "precio_estandar"] = precio_estandar
            df.at[idx, "origen_precio"] = origen_precio

        return df


def main():
    files = list_input_files(INPUT_FOLDER)
    print("Archivos detectados:", files)

    if not files:
        print("No se encontraron archivos.")
        return

    for file in files:
        print("Procesando:", file)

        provider = detect_provider(file)
        used_ai = False

        if file.lower().endswith(".pdf"):
            print("📄 Usando Gemini para PDF...")
            df = extract_with_gemini(file)

            if df is None:
                print("❌ Gemini no pudo procesar el archivo.")
                continue

            used_ai = True

            # En PDFs asumimos que Gemini devuelve "producto" y "precio"
            df = procesar_dataframe(df, "producto", "precio")

        else:
            df = extract_table(file)

            column_map = classify_columns(df.columns.tolist())

            if not column_map["producto"] or not column_map["precio"]:
                print("⚠️ No se pudieron detectar columnas obligatorias.")
                continue

            producto_col = column_map["producto"]
            precio_col = column_map["precio"]

            df = procesar_dataframe(df, producto_col, precio_col)

        # 📊 OUTLIERS
        precios_validos = df["precio_estandar"].dropna()

        if len(precios_validos) > 0:
            q1 = precios_validos.quantile(0.25)
            q3 = precios_validos.quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            df["flag_outlier"] = df["precio_estandar"].apply(
                lambda x: "OUTLIER" if pd.notnull(x) and (x < lower_bound or x > upper_bound) else "OK"
            )
        else:
            df["flag_outlier"] = None

        df["procesado_con_ia"] = used_ai

        output_path = f"output_{provider}.csv"
        df.to_csv(output_path, index=False, decimal=".")

        print(f"Archivo procesado guardado como {output_path}")



if __name__ == "__main__":
    
    main()

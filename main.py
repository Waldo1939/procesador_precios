from core.file_loader import list_input_files
from core.provider_detector import detect_provider
from core.table_extractor import extract_table
from core.column_classifier import classify_columns
from core.unit_parser import extract_quantity_and_unit
from core.unit_normalizer import normalize_quantity
from core.price_calculator import calculate_standard_price
from core.price_calculator import calculate_standard_price, clean_price





INPUT_FOLDER = "input_files"

def main():
    files = list_input_files(INPUT_FOLDER)
    print("Archivos detectados:", files)

    if not files:
        print("No se encontraron archivos.")
        return

    for file in files:
        print("Procesando:", file)

        provider = detect_provider(file)
        df = extract_table(file)

        column_map = classify_columns(df.columns.tolist())

        if not column_map["producto"] or not column_map["precio"]:
            print("⚠️ No se pudieron detectar columnas obligatorias.")
            continue

        producto_col = column_map["producto"]
        precio_col = column_map["precio"]

        df["cantidad_normalizada"] = None
        df["unidad_estandar"] = None
        df["precio_estandar"] = None

        for idx, row in df.iterrows():
            producto = row[producto_col]
            precio_raw = row[precio_col]
            precio = clean_price(precio_raw)


            cantidad, unidad, pack = extract_quantity_and_unit(producto)
            cantidad_norm, unidad_std = normalize_quantity(cantidad, unidad, pack)
            precio_estandar = calculate_standard_price(precio, cantidad_norm)

            df.at[idx, "cantidad_normalizada"] = cantidad_norm
            df.at[idx, "unidad_estandar"] = unidad_std
            df.at[idx, "precio_estandar"] = precio_estandar

        output_path = f"output_{provider}.csv"
        df.to_csv(output_path, index=False)

        print(f"Archivo procesado guardado como {output_path}")


if __name__ == "__main__":
    main()


from core.file_loader import list_input_files
from core.provider_detector import detect_provider
from core.table_extractor import extract_table
from core.column_classifier import classify_columns
from core.unit_parser import extract_quantity_and_unit
from core.unit_normalizer import normalize_quantity
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
        df["origen_precio"] = None

        for idx, row in df.iterrows():
            producto = row[producto_col]

            precio_unit = None
            origen_precio = None

            # 1️⃣ Intentar precio unitario directo (si existe)
            if "precio unitario" in df.columns:
                precio_unit = clean_price(row.get("precio unitario"))
                if precio_unit:
                    origen_precio = "unitario"

            # 2️⃣ Si no hay unitario válido, usar precio caja / uxb
            if (precio_unit is None or precio_unit == 0) and "precio caja" in df.columns and "uxb" in df.columns:
                precio_caja = clean_price(row.get("precio caja"))
                uxb = row.get("uxb")

                if precio_caja and uxb and uxb != 0:
                    precio_unit = precio_caja / uxb
                    origen_precio = "caja_dividido"

            # 3️⃣ Fallback: usar la columna precio detectada automáticamente
            if precio_unit is None:
                precio_unit = clean_price(row.get(precio_col))
                origen_precio = "columna_detectada"

            cantidad, unidad, pack = extract_quantity_and_unit(producto)
            cantidad_norm, unidad_std = normalize_quantity(cantidad, unidad, pack)

            precio_estandar = None
            if precio_unit and cantidad_norm:
                precio_estandar = calculate_standard_price(precio_unit, cantidad_norm)

            df.at[idx, "cantidad_normalizada"] = cantidad_norm
            df.at[idx, "unidad_estandar"] = unidad_std
            df.at[idx, "precio_estandar"] = precio_estandar
            df.at[idx, "origen_precio"] = origen_precio

        output_path = f"output_{provider}.csv"

                # --- DETECCIÓN DE OUTLIERS ---
        precios_validos = df["precio_estandar"].dropna()

        if len(precios_validos) > 0:
            q1 = precios_validos.quantile(0.25)
            q3 = precios_validos.quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            def detectar_outlier(valor):
                if valor is None:
                    return None
                if valor < lower_bound or valor > upper_bound:
                    return "OUTLIER"
                return "OK"

            df["flag_outlier"] = df["precio_estandar"].apply(detectar_outlier)
        else:
            df["flag_outlier"] = None

        df.to_csv(output_path, index=False, decimal=".")

        print(f"Archivo procesado guardado como {output_path}")


if __name__ == "__main__":
    main()


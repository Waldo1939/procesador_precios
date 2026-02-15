from core.file_loader import list_input_files
from core.provider_detector import detect_provider
from core.table_extractor import extract_table
from core.column_classifier import classify_columns
from core.unit_parser import extract_quantity_and_unit
from core.unit_normalizer import normalize_quantity



INPUT_FOLDER = "input_files"

def main():

    #Prueba rapida. BORRAR
    print(extract_quantity_and_unit("ACEITE 6x250ML"))
    print(extract_quantity_and_unit("GALLETAS 12 x 500gr"))
    #BORRAR

    files = list_input_files(INPUT_FOLDER)

    if not files:
        print("No se encontraron archivos.")
        return

    for file in files:
        provider = detect_provider(file)
        df = extract_table(file)

        print(f"Archivo: {file}")
        print(f"Proveedor: {provider}")
        print(f"Filas detectadas: {len(df)}")
        print(f"Columnas detectadas: {list(df.columns)}")
        print("-" * 50)

        column_map = classify_columns(df.columns.tolist())
        print("Columnas clasificadas:", column_map)

        # Validación obligatoria
        if not column_map["producto"] or not column_map["precio"]:
            print("⚠️ No se pudieron detectar columnas obligatorias.")
            continue

        producto_col = column_map["producto"]
        precio_col = column_map["precio"]

        print("\nEjemplo de fila detectada:")
        print("-" * 50)

        for idx, row in df.iterrows():
            producto = row[producto_col]
            precio = row[precio_col]

            cantidad, unidad, pack = extract_quantity_and_unit(producto)

            cantidad_norm, unidad_std = normalize_quantity(cantidad, unidad, pack)

            print(f"Producto: {producto}")
            print(f"Precio: {precio}")
            print(f"Cantidad detectada: {cantidad}")
            print(f"Unidad original: {unidad}")
            print(f"Cantidad normalizada: {cantidad_norm}")
            print(f"Unidad estándar: {unidad_std}")

            break



if __name__ == "__main__":
    main()


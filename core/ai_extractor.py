import os
import json
import mimetypes
import pandas as pd
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def extract_with_gemini(file_path):

    # Detectar tipo MIME automáticamente
    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type is None:
        print("❌ No se pudo detectar el tipo de archivo.")
        return None

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    prompt = """
    Analiza el archivo adjunto.

    Extrae todas las tablas de productos y devuelve EXCLUSIVAMENTE un JSON
    con esta estructura:

    [
      {
        "producto": string,
        "precio": number,
        "precio_unitario": number or null,
        "precio_caja": number or null,
        "uxb": number or null
      }
    ]

    Devuelve solo JSON válido.
    """

    file_part = types.Part.from_bytes(
        data=file_bytes,
        mime_type=mime_type
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt, file_part],
    )

    try:
            raw_text = response.text.strip()

            # Si viene envuelto en ```json ... ```
            if raw_text.startswith("```"):
                raw_text = raw_text.replace("```json", "")
                raw_text = raw_text.replace("```", "")
                raw_text = raw_text.strip()

            data = json.loads(raw_text)
            return pd.DataFrame(data)

    except Exception as e:
            print("❌ Error parseando JSON")
            print("Error:", e)
            print("Respuesta cruda:")
            print(response.text)
            return None


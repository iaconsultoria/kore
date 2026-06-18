import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/facturas/mcp/"
TOKEN = "H3RwsaN6yW9EqWX40LX-uBJ80UICiS1oFifYT8RK1X0"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

def probar_ocr():
    print("\n" + "="*60)
    print("0. EXTRAER_FACTURA_DE_IMAGEN (OCR)")
    print("="*60)

    import base64
    import os

    ruta_imagen = "C:/Users/manue/Desktop/factura2.png"
    if not os.path.exists(ruta_imagen):
        print(f"ERROR: Imagen no encontrada")
        return

    with open(ruta_imagen, "rb") as f:
        imagen_b64 = base64.b64encode(f.read()).decode()

    payload = {
        "name": "extraer_factura_de_imagen",
        "arguments": {"imagen_base64": imagen_b64}
    }

    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def probar_listar_facturas():
    print("\n" + "="*60)
    print("1. LISTAR_FACTURAS")
    print("="*60)
    payload = {
        "name": "listar_facturas",
        "arguments": {"limit": 5}
    }
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def probar_buscar_por_proveedor():
    print("\n" + "="*60)
    print("2. BUSCAR_POR_PROVEEDOR")
    print("="*60)
    payload = {
        "name": "buscar_por_proveedor",
        "arguments": {"nombre": "Telefónica"}
    }
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def probar_resumen_fiscal():
    print("\n" + "="*60)
    print("3. RESUMEN_FISCAL")
    print("="*60)
    payload = {
        "name": "resumen_fiscal",
        "arguments": {"mes": 6, "anio": 2026}
    }
    response = requests.post(BASE_URL, json=payload, headers=HEADERS)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("PROBANDO SERVIDOR MCP - Facturas")
    probar_ocr()
    probar_listar_facturas()
    probar_buscar_por_proveedor()
    probar_resumen_fiscal()
    print("\n" + "="*60)
    print("FIN DE PRUEBAS")
    print("="*60 + "\n")

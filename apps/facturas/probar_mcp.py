import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000/facturas/mcp/"

def probar_listar_facturas():
    print("\n" + "="*60)
    print("1. LISTAR_FACTURAS")
    print("="*60)
    payload = {
        "name": "listar_facturas",
        "arguments": {"limit": 5}
    }
    response = requests.post(BASE_URL, json=payload)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def probar_buscar_por_proveedor():
    print("\n" + "="*60)
    print("2. BUSCAR_POR_PROVEEDOR")
    print("="*60)
    payload = {
        "name": "buscar_por_proveedor",
        "arguments": {"nombre": "Manuel"}
    }
    response = requests.post(BASE_URL, json=payload)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def probar_resumen_fiscal():
    print("\n" + "="*60)
    print("3. RESUMEN_FISCAL")
    print("="*60)
    payload = {
        "name": "resumen_fiscal",
        "arguments": {"mes": 6, "anio": 2026}
    }
    response = requests.post(BASE_URL, json=payload)
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    print("PROBANDO SERVIDOR MCP - Facturas")
    probar_listar_facturas()
    probar_buscar_por_proveedor()
    probar_resumen_fiscal()
    print("\n" + "="*60)
    print("FIN DE PRUEBAS")
    print("="*60 + "\n")

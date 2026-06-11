import requests
import os

BASE = "http://127.0.0.1:8000/calendario/mcp/"
FECHA = "2026-06-16"
TOKEN = os.environ["MCP_SECRET_TOKEN"]

def llamar(herramienta, fecha):
    response = requests.post(
        BASE,
        json={"tool": herramienta, "params": {"fecha": fecha}},
        headers={"Authorization": f"Bearer {TOKEN}"},
    )
    return response.json()


if __name__ == "__main__":
    print("=== listar_citas ===")
    print(llamar("listar_citas", FECHA))

    print("\n=== detectar_sobrecarga ===")
    print(llamar("detectar_sobrecarga", FECHA))

    print("\n=== resumen_dia ===")
    print(llamar("resumen_dia", FECHA))
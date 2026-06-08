import json
from mcp.server import Server
from mcp.types import Tool, TextContent, ToolUseBlock
from django.db.models import Q
from .models import Factura


def crear_servidor_mcp():
    """Crea y retorna el servidor MCP con las herramientas."""
    server = Server("kore-facturas")

    # Listar_facturas
    @server.list_tools()
    async def list_tools():
        return [
            Tool(
                name="listar_facturas",
                description="Devuelve las últimas N facturas con proveedor, número, fecha, total y categoría",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "limit": {
                            "type": "integer",
                            "description": "Número máximo de facturas a retornar",
                            "default": 10
                        }
                    }
                }
            ),
            Tool(
                name="buscar_por_proveedor",
                description="Devuelve facturas cuyo proveedor contenga el texto buscado",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "nombre": {
                            "type": "string",
                            "description": "Texto a buscar en el nombre del proveedor"
                        }
                    },
                    "required": ["nombre"]
                }
            )
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "listar_facturas":
            limit = arguments.get("limit", 10)
            facturas = Factura.objects.select_related("proveedor", "categoria").order_by("-fecha_emision")[:limit]
            resultado = []
            for f in facturas:
                resultado.append({
                    "id": f.id,
                    "numero_factura": f.numero_factura,
                    "proveedor": f.proveedor.nombre,
                    "fecha_emision": f.fecha_emision.isoformat(),
                    "total": float(f.total),
                    "categoria": f.categoria.nombre if f.categoria else None
                })
            return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

        elif name == "buscar_por_proveedor":
            nombre = arguments.get("nombre", "")
            facturas = Factura.objects.filter(
                proveedor__nombre__icontains=nombre
            ).select_related("proveedor", "categoria").order_by("-fecha_emision")
            resultado = []
            for f in facturas:
                resultado.append({
                    "id": f.id,
                    "numero_factura": f.numero_factura,
                    "proveedor": f.proveedor.nombre,
                    "fecha_emision": f.fecha_emision.isoformat(),
                    "total": float(f.total),
                    "categoria": f.categoria.nombre if f.categoria else None
                })
            return [TextContent(type="text", text=json.dumps(resultado, ensure_ascii=False, indent=2))]

        else:
            return [TextContent(type="text", text=json.dumps({"error": f"Herramienta {name} no encontrada"}))]

    return server


# Instancia global del servidor
servidor_mcp = crear_servidor_mcp()

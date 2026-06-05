import json
from unittest.mock import patch, MagicMock, mock_open
from django.test import TestCase
from apps.facturas.servicios.extractor import extraer_factura


RESPUESTA_MOCK = {
    "numero_factura": "F-2026-001",
    "fecha_factura": "2026-01-15",
    "proveedor": "Servicios Informáticos SL",
    "fecha_emision": "2026-01-15",
    "nif_emisor": "12345678B",
    "nombre_emisor": "Servicios Informáticos SL",
    "base_imponible": 1000.00,
    "iva_porcentaje": 21,
    "iva_total": 210.00,
    "total": 1210.00
}


class ExtractorFacturaTest(TestCase):

    @patch("builtins.open", mock_open(read_data=b"contenido_falso"))
    @patch("apps.facturas.servicios.extractor.litellm.completion")
    def test_extractor_devuelve_dict_con_campos_correctos(self, mock_completion):
        mock_mensaje = MagicMock()
        mock_mensaje.choices[0].message.content = json.dumps(RESPUESTA_MOCK)
        mock_completion.return_value = mock_mensaje

        resultado = extraer_factura("factura_prueba.pdf")

        self.assertEqual(resultado["numero_factura"], "F-2026-001")
        self.assertEqual(resultado["nif_emisor"], "12345678B")
        self.assertEqual(resultado["total"], 1210.00)
        self.assertIn("fecha_emision", resultado)


    @patch("builtins.open", mock_open(read_data=b"contenido_falso"))
    @patch("apps.facturas.servicios.extractor.litellm.completion")
    def test_extractor_respuesta_vacia_devuelve_extraccion_fallida(self, mock_completion):
        mock_mensaje = MagicMock()
        mock_mensaje.choices[0].message.content = ""
        mock_completion.return_value = mock_mensaje

        resultado = extraer_factura("factura_prueba.pdf")

        self.assertEqual(resultado["extraccion_fallida"], True)
        self.assertEqual(resultado["error"], "respuesta no válida del modelo")

    @patch("builtins.open", mock_open(read_data=b"contenido_falso"))
    @patch("apps.facturas.servicios.extractor.litellm.completion")
    def test_extractor_sin_numero_factura_devuelve_campos_ausentes(self, mock_completion):
        mock_mensaje = MagicMock()
        mock_mensaje.choices[0].message.content = json.dumps({
            "proveedor": "Empresa SL",
            "fecha_factura": "2026-01-15"
        })
        mock_completion.return_value = mock_mensaje

        resultado = extraer_factura("factura_prueba.pdf")

        self.assertEqual(resultado["extraccion_fallida"], True)
        self.assertEqual(resultado["error"], "campos obligatorios ausentes")

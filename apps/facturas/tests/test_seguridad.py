import time
import unittest
import json
import os
import hmac
from django.test import TestCase, Client
from django.urls import reverse
from apps.facturas.models import Factura, Proveedor
from datetime import date


TOKEN = os.getenv('FACTURAS_MCP_TOKEN', '')


class TestE11TimingAttackToken(TestCase):
    """
    E1.1 — Timing attack en token MCP.
    BUG: la comparación usa != en lugar de hmac.compare_digest().
    FIX PENDIENTE lunes: usar hmac.compare_digest()
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('mcp_endpoint')
        self.payload = json.dumps({
            "name": "listar_facturas",
            "arguments": {"limit": 10, "offset": 0}
        })

    def test_token_incorrecto_devuelve_401(self):
        """Control: token inválido siempre devuelve 401."""
        response = self.client.post(
            self.url,
            data=self.payload,
            content_type="application/json",
            HTTP_AUTHORIZATION="Bearer token_completamente_incorrecto"
        )
        self.assertEqual(response.status_code, 401)
        self.assertIn("error", response.json())

    @unittest.expectedFailure
    def test_codigo_usa_compare_digest(self):
        """
        BUG ACTIVO E1.1: El código usa != en lugar de hmac.compare_digest().
        Este test lee el código fuente y verifica que el fix NO está aplicado.
        Fallará (expectedFailure) hasta que se aplique hmac.compare_digest().
        """
        import inspect
        from apps.facturas import views

        source = inspect.getsource(views.mcp_endpoint)

        # Con el bug: usa !=  (comparación normal, timing predecible)
        # Con el fix: usará hmac.compare_digest()
        self.assertIn("hmac.compare_digest", source)


class TestE21SQLInjectionIcontains(TestCase):
    """
    E2.1 — Data exfiltration via icontains en buscar_por_proveedor().
    BUG: validar_parametros() solo rechaza vacío, pero no caracteres
    especiales ni longitud mínima de 2. "%" y "a" pasan la validación.
    FIX PENDIENTE lunes: longitud >= 2 y regex solo alfanumérico.
    """

    def setUp(self):
        self.client = Client()
        self.url = reverse('mcp_endpoint')

        p1 = Proveedor.objects.create(nombre="Telefonica España")
        p2 = Proveedor.objects.create(nombre="Google LLC")
        p3 = Proveedor.objects.create(nombre="Proveedor Secreto XYZ")

        for p, num in [(p1, "F-001"), (p2, "F-002"), (p3, "F-003")]:
            Factura.objects.create(
                numero_factura=num,
                proveedor=p,
                fecha_emision=date(2026, 6, 1),
                base_imponible=1000,
                iva_total=210,
                total=1210
            )

    def _post(self, nombre):
        return self.client.post(
            self.url,
            data=json.dumps({
                "name": "buscar_por_proveedor",
                "arguments": {"nombre": nombre}
            }),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {TOKEN}"
        )

    def test_busqueda_legitima_funciona(self):
        """Control: búsqueda normal devuelve solo lo que corresponde."""
        if not TOKEN:
            self.skipTest("FACTURAS_MCP_TOKEN no definido en entorno")
        response = self._post("Telefonica")
        self.assertEqual(response.status_code, 200)
        resultado = response.json().get('resultado', [])
        self.assertEqual(len(resultado), 1)
        self.assertIn("Telefonica", resultado[0]['proveedor'])

    @unittest.expectedFailure
    def test_wildcard_porcentaje_no_rechazado(self):
        """
        BUG ACTIVO E2.1: "%" tiene longitud 1 y no está vacío,
        pasa validar_parametros() y devuelve todas las facturas.
        Con el fix (len >= 2 + regex), debería devolver 400.
        """
        if not TOKEN:
            self.skipTest("FACTURAS_MCP_TOKEN no definido en entorno")
        response = self._post("%")
        # Con el bug: 200 y dump completo
        # Con el fix: 400 "nombre debe tener 2-50 caracteres"
        self.assertEqual(response.status_code, 400)

    @unittest.expectedFailure
    def test_una_letra_enumera_proveedores(self):
        """
        BUG ACTIVO E2.1: nombre="a" pasa la validación (no está vacío)
        y devuelve todas las facturas cuyos proveedores contienen "a".
        Con el fix (len >= 2), debería devolver 400.
        """
        if not TOKEN:
            self.skipTest("FACTURAS_MCP_TOKEN no definido en entorno")
        response = self._post("a")
        # Con el bug: 200 y facturas de proveedores con "a"
        # Con el fix: 400
        self.assertEqual(response.status_code, 400)

    @unittest.expectedFailure
    def test_codigo_valida_longitud_minima(self):
        """
        BUG ACTIVO E2.1: validar_parametros() comprueba que nombre no esté
        vacío, pero no impone longitud mínima de 2 ni rechaza caracteres
        especiales como %. Fix pendiente lunes.
        """
        import inspect
        from apps.facturas import views

        source = inspect.getsource(views.validar_parametros)

        # Con el fix habrá validación de longitud mínima >= 2
        # y regex para caracteres permitidos
        self.assertIn("len(nombre) < 2", source)

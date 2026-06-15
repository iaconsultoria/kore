from django.conf import settings
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
import json

from .models import Categoria, Cita


class CategoriaYCitaTest(TestCase):
    def test_crear_categoria_y_cita(self):
        categoria = Categoria.objects.create(
            nombre="Cliente",
            color="#2563EB",
            prioridad=3,
            politica_reprog="rigida",
        )
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(categoria.nombre, "Cliente")

        cita = Cita.objects.create(
            titulo="Reunión con cliente",
            inicio=date(2026, 6, 9),
            fin=date(2026, 6, 9),
            categoria=categoria,
            prioridad=2,
        )
        self.assertEqual(Cita.objects.count(), 1)
        self.assertEqual(cita.titulo, "Reunión con cliente")
        self.assertEqual(cita.categoria, categoria)


class CitaDesdeTextoTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cita_desde_texto_devuelve_formulario(self):
        response = self.client.post(
            reverse("calendario:cita_desde_texto"),
            {"texto": "Reunión el lunes a las 10"},
        )
        self.assertEqual(response.status_code, 200)
        context_keys = list(response.context.keys()) if response.context else []
        self.assertTrue(
            "form" in context_keys or "pregunta" in context_keys,
            f"El contexto debe contener 'form' o 'pregunta'. Claves encontradas: {context_keys}"
        )


class TranscribirAudioVacioTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_audio_vacio_devuelve_400(self):
        response = self.client.post(reverse("calendario:transcribir"))
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)


class McpBodyMalFormadoTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_body_no_json_devuelve_400(self):
        response = self.client.post(
            reverse("calendario:mcp"),
            data="esto no es json",
            content_type="text/plain",
            HTTP_AUTHORIZATION=f"Bearer {settings.MCP_SECRET_TOKEN}",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)


class McpFechaInvalidaTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_fecha_ausente_devuelve_400(self):
        response = self.client.post(
            reverse("calendario:mcp"),
            data=json.dumps({"tool": "listar_citas", "params": {}}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {settings.MCP_SECRET_TOKEN}",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_fecha_formato_invalido_devuelve_400(self):
        response = self.client.post(
            reverse("calendario:mcp"),
            data=json.dumps({"tool": "listar_citas", "params": {"fecha": "no-es-fecha"}}),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {settings.MCP_SECRET_TOKEN}",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)


class TranscribirArchivoInvalidoTest(TestCase):
    def setUp(self):
        self.client = Client()

    # TODO: este test falla porque la vista no valida el tipo de archivo
    def test_archivo_no_audio_devuelve_400(self):
        archivo_falso = SimpleUploadedFile(
            "malware.exe",
            b"esto no es audio",
            content_type="application/octet-stream",
        )
        response = self.client.post(
            reverse("calendario:transcribir"),
            {"audio": archivo_falso},
        )
        self.assertEqual(response.status_code, 400)

    # TODO: este test falla porque la vista no valida el tamaño del archivo
    def test_archivo_muy_grande_devuelve_400(self):
        archivo_grande = SimpleUploadedFile(
            "audio.webm",
            b"x" * (11 * 1024 * 1024),
            content_type="audio/webm",
        )
        response = self.client.post(
            reverse("calendario:transcribir"),
            {"audio": archivo_grande},
        )
        self.assertEqual(response.status_code, 400)


class ParserTextoLargoTest(TestCase):
    def setUp(self):
        self.client = Client()

    # TODO: este test falla porque cita_desde_texto no limita la longitud del texto
    def test_texto_muy_largo_no_rompe_la_vista(self):
        texto_largo = "reunión el lunes a las 10 " * 500
        response = self.client.post(
            reverse("calendario:cita_desde_texto"),
            {"texto": texto_largo},
        )
        self.assertNotEqual(response.status_code, 500)
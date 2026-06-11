from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date
from .models import Categoria, Cita
 
 
class CategoriaYCitaTest(TestCase):
    def test_crear_categoria_y_cita(self):
        # Crear categoría
        categoria = Categoria.objects.create(
            nombre="Cliente",
            color="#2563EB",
            prioridad=3,
            politica_reprog="rigida",
        )
        self.assertEqual(Categoria.objects.count(), 1)
        self.assertEqual(categoria.nombre, "Cliente")
 
        # Crear cita asociada
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
        # La respuesta debe contener el formulario o la clarificación
        self.assertIn(
            response.status_code, [200],
            "La vista debe devolver 200"
        )
        # Verificar que el contexto contiene form o pregunta
        context_keys = list(response.context.keys()) if response.context else []
        self.assertTrue(
            "form" in context_keys or "pregunta" in context_keys,
            f"El contexto debe contener 'form' o 'pregunta'. Claves encontradas: {context_keys}"
        )

from django.test import TestCase, Client
from django.urls import reverse
import json



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
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)

    def test_fecha_formato_invalido_devuelve_400(self):
        response = self.client.post(
            reverse("calendario:mcp"),
            data=json.dumps({"tool": "listar_citas", "params": {"fecha": "no-es-fecha"}}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn("error", data)        
from __future__ import annotations

import unittest
import shutil
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from models.formulario import ESTADO_PENDIENTE_OPERARIO, Formulario
from models.plantilla_preguntas import PlantillaPreguntas
from presenters.admin_preguntas_presenter import AdminPreguntasPresenter
from presenters.formulario_operario_presenter import FormularioOperarioPresenter
from repositories.formulario_repository import FormularioRepository
from repositories.plantilla_preguntas_repository import PlantillaPreguntasRepository
from repositories.pregunta_repository import PreguntaRepository
from repositories.respuesta_repository import RespuestaRepository
from services.forms.formulario_service import FormularioService
from services.forms.plantilla_preguntas_service import PlantillaPreguntasService
from services.forms.pregunta_service import PreguntaService
from services.forms.respuesta_service import RespuestaService
from services.reporting.reporte_service import ReporteService
from ui.detalle_formulario import DetalleFormularioView


WORKSPACE_TMP = Path(__file__).resolve().parent / ".test_tmp"


@contextmanager
def _temporary_workspace_dir() -> Iterator[Path]:
    WORKSPACE_TMP.mkdir(exist_ok=True)
    tmp_path = WORKSPACE_TMP / f"test-{uuid.uuid4().hex}"
    tmp_path.mkdir()
    try:
        yield tmp_path
    finally:
        shutil.rmtree(tmp_path)


def _crear_service(tmp_path: Path) -> FormularioService:
    formulario_repository = FormularioRepository(tmp_path / "formularios.json")
    plantilla_repository = PlantillaPreguntasRepository(
        tmp_path / "plantillas_preguntas.json"
    )
    plantilla_repository.guardar(
        PlantillaPreguntas(
            id_plantilla="TPL-SETOR-REC-V001",
            clave_plantilla="TPL-SETOR-REC",
            cod_recurso="REC",
            cod_setor="SETOR",
            version=1,
            activa=True,
            items=[],
        )
    )
    plantilla_service = PlantillaPreguntasService(plantilla_repository)
    return FormularioService(formulario_repository, plantilla_service)


def _crear_servicios_flujo(tmp_path: Path) -> tuple[
    AdminPreguntasPresenter,
    FormularioService,
    PreguntaService,
    PlantillaPreguntasService,
    RespuestaService,
    ReporteService,
]:
    formulario_repository = FormularioRepository(tmp_path / "formularios.json")
    pregunta_repository = PreguntaRepository(tmp_path / "preguntas.json")
    respuesta_repository = RespuestaRepository(tmp_path / "respuestas.json")
    plantilla_repository = PlantillaPreguntasRepository(
        tmp_path / "plantillas_preguntas.json"
    )
    plantilla_service = PlantillaPreguntasService(plantilla_repository)
    pregunta_service = PreguntaService(pregunta_repository, plantilla_service)
    formulario_service = FormularioService(formulario_repository, plantilla_service)
    respuesta_service = RespuestaService(respuesta_repository)
    reporte_service = ReporteService(
        formulario_service=formulario_service,
        respuesta_service=respuesta_service,
        pregunta_service=pregunta_service,
        plantilla_preguntas_service=plantilla_service,
    )
    admin_presenter = AdminPreguntasPresenter(pregunta_service)

    return (
        admin_presenter,
        formulario_service,
        pregunta_service,
        plantilla_service,
        respuesta_service,
        reporte_service,
    )


class FormularioServicePlantillaTest(unittest.TestCase):
    def test_crear_formulario_desde_apontamento_asigna_plantilla_activa(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            service = _crear_service(tmp_dir)

            resultado = service.crear_formulario_pendiente_desde_registro_apontamento(
                {
                    "id_apontamento": "123",
                    "num_ordem": "OP-123",
                    "cod_recurso": "REC",
                    "cod_setor": "SETOR",
                }
            )

            formulario = resultado["formulario"]

            self.assertFalse(resultado["ya_existia"])
            self.assertEqual(formulario.id_plantilla_preguntas, "TPL-SETOR-REC-V001")
            self.assertEqual(formulario.version_plantilla_preguntas, 1)

    def test_crear_formulario_desde_apontamento_falla_sin_plantilla_activa(
        self,
    ) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            service = _crear_service(tmp_dir)

            with self.assertRaisesRegex(
                ValueError,
                "No existe una plantilla activa",
            ):
                service.crear_formulario_pendiente_desde_registro_apontamento(
                    {
                        "id_apontamento": "124",
                        "num_ordem": "OP-124",
                        "cod_recurso": "OTRO",
                        "cod_setor": "SETOR",
                }
            )

    def test_crear_formulario_desde_apontamento_falla_sin_campos_base(self) -> None:
        casos = [
            (
                {
                    "id_apontamento": "",
                    "num_ordem": "OP-125",
                    "cod_recurso": "REC",
                    "cod_setor": "SETOR",
                },
                "IdApontamento",
            ),
            (
                {
                    "id_apontamento": "125",
                    "num_ordem": "",
                    "cod_recurso": "REC",
                    "cod_setor": "SETOR",
                },
                "identificador",
            ),
            (
                {
                    "id_apontamento": "125",
                    "num_ordem": "OP-125",
                    "cod_recurso": "",
                    "cod_setor": "SETOR",
                },
                "CodRecurso",
            ),
            (
                {
                    "id_apontamento": "125",
                    "num_ordem": "OP-125",
                    "cod_recurso": "REC",
                    "cod_setor": "",
                },
                "CodSetor",
            ),
        ]

        with _temporary_workspace_dir() as tmp_dir:
            service = _crear_service(tmp_dir)
            for registro, mensaje in casos:
                with self.subTest(mensaje=mensaje):
                    with self.assertRaisesRegex(ValueError, mensaje):
                        service.crear_formulario_pendiente_desde_registro_apontamento(
                            registro
                        )

    def test_guardar_formulario_nuevo_falla_sin_plantilla(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            service = _crear_service(tmp_dir)

            formulario = Formulario(
                id_formulario="FORM-MANUAL",
                identificador="OP-MANUAL",
                id_apontamento="MANUAL",
                fecha_formulario="2026-04-14",
                cod_recurso="REC",
                cod_setor="SETOR",
            )

            with self.assertRaisesRegex(ValueError, "id_plantilla_preguntas"):
                service.guardar_formulario(formulario)

    def test_guardar_formulario_nuevo_falla_sin_campos_base(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            service = _crear_service(tmp_dir)

            formulario = Formulario(
                id_formulario="FORM-MANUAL",
                identificador="OP-MANUAL",
                id_apontamento="MANUAL",
                fecha_formulario="2026-04-15",
                cod_recurso="REC",
                cod_setor="",
                id_plantilla_preguntas="TPL-SETOR-REC-V001",
                version_plantilla_preguntas=1,
            )

            with self.assertRaisesRegex(ValueError, "CodSetor"):
                service.guardar_formulario(formulario)

    def test_preparar_formulario_no_repara_plantilla_automaticamente(self) -> None:
        formulario = Formulario(
            id_formulario="FORM-LEGACY",
            identificador="OP-LEGACY",
            id_apontamento="LEGACY",
            fecha_formulario="2026-04-14",
            estado=ESTADO_PENDIENTE_OPERARIO,
        )
        formulario_service = _FormularioServiceSinReparacion(formulario)
        presenter = FormularioOperarioPresenter(
            formulario_service=formulario_service,
        )

        preparado = presenter.preparar_formulario(
            formulario=formulario,
            operario_seleccionado="",
        )

        self.assertEqual(preparado, formulario)
        self.assertFalse(formulario_service.reparacion_llamada)

    def test_flujo_gestion_apontamento_operario_usa_nueva_plantilla(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            (
                admin_presenter,
                formulario_service,
                pregunta_service,
                plantilla_service,
                respuesta_service,
                reporte_service,
            ) = _crear_servicios_flujo(tmp_dir)
            filtros = {"cod_setor": ["SETOR"], "cod_recurso": ["REC"]}

            payload_inicial = admin_presenter.construir_payload_pregunta(
                texto="Pregunta inicial",
                tipo="seleccion_unica",
                obligatoria=True,
                activa=True,
                orden=1,
                filtros_contexto=filtros,
                opciones_respuesta=[
                    {"id_opcion": "OPC-001", "valor": "OK"},
                    {"id_opcion": "OPC-002", "valor": "NOK"},
                ],
            )
            admin_presenter.guardar_pregunta(None, payload_inicial)
            pregunta_inicial = pregunta_service.listar_preguntas(solo_activas=True)[0]
            plantilla_inicial = plantilla_service.obtener_activa("REC", "SETOR")

            self.assertIsNotNone(plantilla_inicial)
            self.assertEqual(plantilla_inicial.version, 1)
            self.assertEqual(
                plantilla_inicial.items[0].id_pregunta,
                pregunta_inicial["id_pregunta"],
            )
            resultado_formulario_inicial = (
                formulario_service.crear_formulario_pendiente_desde_registro_apontamento(
                    {
                        "id_apontamento": "AP-000",
                        "num_ordem": "OP-000",
                        "cod_recurso": "REC",
                        "cod_setor": "SETOR",
                    }
                )
            )
            formulario_inicial = resultado_formulario_inicial["formulario"]
            respuesta_service.crear_respuesta(
                id_formulario=formulario_inicial.id_formulario,
                id_pregunta=pregunta_inicial["id_pregunta"],
                respuesta_texto="OK",
                id_opcion="OPC-001",
            )

            payload_editado = admin_presenter.construir_payload_pregunta(
                texto="Pregunta editada",
                tipo="seleccion_unica",
                obligatoria=True,
                activa=True,
                orden=1,
                filtros_contexto=filtros,
                opciones_respuesta=[
                    {"id_opcion": "OPC-001", "valor": "Conforme"},
                    {"id_opcion": "OPC-002", "valor": "No conforme"},
                ],
            )
            admin_presenter.guardar_pregunta(
                pregunta_inicial["id_pregunta"],
                payload_editado,
            )

            preguntas = pregunta_service.listar_preguntas(solo_activas=False)
            pregunta_anterior = pregunta_service.obtener_pregunta(
                pregunta_inicial["id_pregunta"]
            )
            pregunta_nueva = next(pregunta for pregunta in preguntas if pregunta["activa"])
            plantilla_nueva = plantilla_service.obtener_activa("REC", "SETOR")

            self.assertFalse(pregunta_anterior["activa"])
            self.assertEqual(pregunta_nueva["texto"], "Pregunta editada")
            self.assertIsNotNone(plantilla_nueva)
            self.assertEqual(plantilla_nueva.version, 2)
            self.assertEqual(
                plantilla_nueva.items[0].id_pregunta,
                pregunta_nueva["id_pregunta"],
            )
            plantillas_auditoria = (
                plantilla_service.repository.listar_por_contexto("REC", "SETOR")
            )
            self.assertEqual(
                [plantilla.version for plantilla in plantillas_auditoria],
                [1, 2],
            )
            self.assertFalse(plantillas_auditoria[0].activa)
            self.assertTrue(plantillas_auditoria[1].activa)
            self.assertEqual(
                plantillas_auditoria[0].items[0].id_pregunta,
                pregunta_inicial["id_pregunta"],
            )
            self.assertEqual(
                plantillas_auditoria[1].items[0].id_pregunta,
                pregunta_nueva["id_pregunta"],
            )

            resultado_formulario = (
                formulario_service.crear_formulario_pendiente_desde_registro_apontamento(
                    {
                        "id_apontamento": "AP-001",
                        "num_ordem": "OP-001",
                        "cod_recurso": "REC",
                        "cod_setor": "SETOR",
                    }
                )
            )
            formulario = resultado_formulario["formulario"]

            self.assertEqual(
                formulario.id_plantilla_preguntas,
                plantilla_nueva.id_plantilla,
            )
            self.assertEqual(
                formulario.version_plantilla_preguntas,
                plantilla_nueva.version,
            )

            operario_presenter = FormularioOperarioPresenter(
                formulario_service=formulario_service,
                pregunta_service=pregunta_service,
            )
            preguntas_operario = operario_presenter.obtener_preguntas_para_formulario(
                formulario,
            )

            self.assertEqual(len(preguntas_operario), 1)
            self.assertEqual(preguntas_operario[0]["texto"], "Pregunta editada")
            self.assertEqual(
                preguntas_operario[0]["id_pregunta"],
                pregunta_nueva["id_pregunta"],
            )

            detalle_formulario_inicial = (
                reporte_service.obtener_detalle_auditoria_formulario(
                    formulario_inicial,
                )
            )
            detalle_formulario_nuevo = (
                reporte_service.obtener_detalle_auditoria_formulario(
                    formulario,
                )
            )

            self.assertEqual(formulario_inicial.version_plantilla_preguntas, 1)
            self.assertEqual(
                detalle_formulario_inicial[0]["pregunta"],
                "Pregunta inicial",
            )
            self.assertEqual(detalle_formulario_inicial[0]["version_pregunta"], 1)
            self.assertEqual(detalle_formulario_inicial[0]["respuesta"], "OK")
            self.assertEqual(detalle_formulario_inicial[0]["opcion"], "OK")
            self.assertEqual(
                detalle_formulario_inicial[0]["opciones_disponibles"],
                "OK, NOK",
            )

            self.assertEqual(formulario.version_plantilla_preguntas, 2)
            self.assertEqual(detalle_formulario_nuevo[0]["pregunta"], "Pregunta editada")
            self.assertEqual(detalle_formulario_nuevo[0]["version_pregunta"], 2)
            self.assertEqual(
                detalle_formulario_nuevo[0]["opciones_disponibles"],
                "Conforme, No conforme",
            )

    def test_respuesta_multiple_antigua_conserva_opciones_tras_edicion(self) -> None:
        with _temporary_workspace_dir() as tmp_dir:
            (
                admin_presenter,
                formulario_service,
                pregunta_service,
                plantilla_service,
                respuesta_service,
                reporte_service,
            ) = _crear_servicios_flujo(tmp_dir)
            filtros = {"cod_setor": ["SETOR"], "cod_recurso": ["REC"]}

            payload_inicial = admin_presenter.construir_payload_pregunta(
                texto="Selecciona defectos detectados",
                tipo="seleccion_multiple",
                obligatoria=True,
                activa=True,
                orden=1,
                filtros_contexto=filtros,
                opciones_respuesta=[
                    {"id_opcion": "OPC-001", "valor": "Tinta"},
                    {"id_opcion": "OPC-002", "valor": "Solvente"},
                    {"id_opcion": "OPC-003", "valor": "Envase"},
                ],
            )
            admin_presenter.guardar_pregunta(None, payload_inicial)
            pregunta_inicial = pregunta_service.listar_preguntas(solo_activas=True)[0]
            plantilla_inicial = plantilla_service.obtener_activa("REC", "SETOR")
            resultado_formulario_inicial = (
                formulario_service.crear_formulario_pendiente_desde_registro_apontamento(
                    {
                        "id_apontamento": "AP-MULTI-001",
                        "num_ordem": "OP-MULTI-001",
                        "cod_recurso": "REC",
                        "cod_setor": "SETOR",
                    }
                )
            )
            formulario_inicial = resultado_formulario_inicial["formulario"]

            respuesta_service.crear_respuesta(
                id_formulario=formulario_inicial.id_formulario,
                id_pregunta=pregunta_inicial["id_pregunta"],
                respuesta_texto="Tinta",
                id_opcion="OPC-001",
            )
            respuesta_service.crear_respuesta(
                id_formulario=formulario_inicial.id_formulario,
                id_pregunta=pregunta_inicial["id_pregunta"],
                respuesta_texto="Envase",
                id_opcion="OPC-003",
            )

            payload_editado = admin_presenter.construir_payload_pregunta(
                texto="Selecciona hallazgos detectados",
                tipo="seleccion_multiple",
                obligatoria=True,
                activa=True,
                orden=1,
                filtros_contexto=filtros,
                opciones_respuesta=[
                    {"id_opcion": "OPC-001", "valor": "Color"},
                    {"id_opcion": "OPC-002", "valor": "Limpieza"},
                    {"id_opcion": "OPC-003", "valor": "Rotulado"},
                ],
            )
            admin_presenter.guardar_pregunta(
                pregunta_inicial["id_pregunta"],
                payload_editado,
            )
            plantilla_nueva = plantilla_service.obtener_activa("REC", "SETOR")

            self.assertEqual(plantilla_inicial.version, 1)
            self.assertEqual(plantilla_nueva.version, 2)
            self.assertNotEqual(
                plantilla_inicial.id_plantilla,
                plantilla_nueva.id_plantilla,
            )

            detalle_formulario_inicial = (
                reporte_service.obtener_detalle_auditoria_formulario(
                    formulario_inicial,
                )
            )

            self.assertEqual(len(detalle_formulario_inicial), 2)
            self.assertEqual(formulario_inicial.version_plantilla_preguntas, 1)
            self.assertEqual(
                {fila["pregunta"] for fila in detalle_formulario_inicial},
                {"Selecciona defectos detectados"},
            )
            self.assertEqual(
                {fila["version_pregunta"] for fila in detalle_formulario_inicial},
                {1},
            )
            self.assertEqual(
                {fila["opcion"] for fila in detalle_formulario_inicial},
                {"Tinta", "Envase"},
            )
            self.assertEqual(
                {
                    fila["opciones_disponibles"]
                    for fila in detalle_formulario_inicial
                },
                {"Tinta, Solvente, Envase"},
            )

    def test_estado_plantilla_detalle_formulario_es_explicito(self) -> None:
        formulario_sin_plantilla = Formulario(
            id_formulario="FORM-SIN",
            identificador="OP-SIN",
            id_apontamento="AP-SIN",
            fecha_formulario="2026-04-15",
        )
        formulario_con_plantilla = Formulario(
            id_formulario="FORM-CON",
            identificador="OP-CON",
            id_apontamento="AP-CON",
            fecha_formulario="2026-04-15",
            id_plantilla_preguntas="TPL-SETOR-REC-V001",
            version_plantilla_preguntas=1,
        )
        vista_sin_plantilla = DetalleFormularioView.__new__(DetalleFormularioView)
        vista_sin_plantilla.formulario = formulario_sin_plantilla
        vista_con_plantilla = DetalleFormularioView.__new__(DetalleFormularioView)
        vista_con_plantilla.formulario = formulario_con_plantilla

        self.assertEqual(
            vista_sin_plantilla._resolver_estado_plantilla({}),
            "Sin plantilla",
        )
        self.assertEqual(
            vista_con_plantilla._resolver_estado_plantilla({}),
            "No encontrada",
        )
        self.assertEqual(
            vista_con_plantilla._resolver_estado_plantilla({"activa": False}),
            "Historica",
        )
        self.assertEqual(
            vista_con_plantilla._resolver_estado_plantilla({"activa": True}),
            "Activa actualmente",
        )


class _FormularioServiceSinReparacion:
    def __init__(self, formulario: Formulario) -> None:
        self.formulario = formulario
        self.reparacion_llamada = False

    def obtener_formulario_por_id(self, id_formulario: str) -> Formulario | None:
        if id_formulario == self.formulario.id_formulario:
            return self.formulario
        return None

    def asignar_plantilla_activa_si_falta(self, id_formulario: str) -> Formulario:
        self.reparacion_llamada = True
        raise AssertionError("No debe reparar plantilla automaticamente.")


if __name__ == "__main__":
    unittest.main()

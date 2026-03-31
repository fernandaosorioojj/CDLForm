from launcher.app_launcher import AppLauncher
from services.catalogo_contexto_service import CatalogoContextoService
from services.evento_op_service import EventoOPService
from services.formulario_service import FormularioService


class DisparadorService:
    def __init__(self) -> None:
        self.evento_service = EventoOPService()
        self.launcher = AppLauncher()
        self.catalogo_service = CatalogoContextoService()
        self.formulario_service = FormularioService()

    def normalizar_estado(self, estado: str | None) -> str:
        return str(estado or "").strip().lower()

    def es_transicion_valida(self, estado_anterior: str, estado_nuevo: str) -> bool:
        anterior = self.normalizar_estado(estado_anterior)
        nuevo = self.normalizar_estado(estado_nuevo)
        return anterior != "terminado" and nuevo == "terminado"

    def debe_disparar(self, evento: dict) -> bool:
        if not self.es_transicion_valida(
            evento.get("estado_anterior", ""),
            evento.get("estado_nuevo", ""),
        ):
            return False

        contexto = self.catalogo_service.resolver_contexto(
            cod_setor=evento.get("cod_setor"),
            cod_recurso=evento.get("cod_recurso"),
            cod_ativ=evento.get("cod_ativ"),
            turno=evento.get("turno"),
        )

        if not contexto.get("cod_setor"):
            return False

        if not contexto.get("cod_recurso"):
            return False

        return True

    def procesar_evento(self, evento: dict, operario: str = "PENDIENTE") -> dict:
        resultado = {
            "debe_disparar": False,
            "formulario": None,
            "contexto_resuelto": None,
            "mensaje": "",
        }

        if not self.es_transicion_valida(
            evento.get("estado_anterior", ""),
            evento.get("estado_nuevo", ""),
        ):
            resultado["mensaje"] = "La transición de estado no es válida para disparar."
            return resultado

        contexto = self.catalogo_service.resolver_contexto(
            cod_setor=evento.get("cod_setor"),
            cod_recurso=evento.get("cod_recurso"),
            cod_ativ=evento.get("cod_ativ"),
            turno=evento.get("turno"),
        )

        resultado["contexto_resuelto"] = contexto

        if not contexto.get("cod_setor"):
            resultado["mensaje"] = "No se pudo homologar el cod_setor del evento."
            return resultado

        if not contexto.get("cod_recurso"):
            resultado["mensaje"] = "No se pudo homologar el cod_recurso del evento."
            return resultado

        formulario = self.formulario_service.crear_formulario(
            identificador=str(evento.get("num_ordem", "")).strip(),
            operario=operario,
            contexto=contexto,
            evento_origen=str(evento.get("id_evento", "")).strip(),
            estado="pendiente",
        )

        self.evento_service.actualizar_evento(
            str(evento.get("id_evento", "")).strip(),
            {
                "contexto_resuelto": contexto,
                "id_formulario_generado": formulario.id_formulario,
                "mensaje_error": None,
                "procesado": True,
            },
        )

        resultado["debe_disparar"] = True
        resultado["formulario"] = formulario.to_dict()
        resultado["mensaje"] = "Formulario generado correctamente."
        return resultado
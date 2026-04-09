from __future__ import annotations

from typing import Any

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QButtonGroup,
    QComboBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QRadioButton,
    QScrollArea,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from models.formulario import (
    ESTADO_EN_APERTURA,
    ESTADO_PENDIENTE_OPERARIO,
    Formulario,
)
from services.formulario_service import FormularioService
from services.pregunta_service import PreguntaService
from services.respuesta_service import RespuestaService


class FormularioOperarioView(QWidget):
    def __init__(
        self,
        formulario: Formulario | None = None,
        operario: str = "",
        contexto: dict[str, Any] | None = None,
        formulario_service: FormularioService | None = None,
        pregunta_service: PreguntaService | None = None,
        respuesta_service: RespuestaService | None = None,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.formulario_service = formulario_service or FormularioService()
        self.pregunta_service = pregunta_service or PreguntaService()
        self.respuesta_service = respuesta_service or RespuestaService()

        self.formulario = self._resolver_formulario_inicial(
            formulario=formulario,
            contexto=contexto,
        )
        self.operario_seleccionado = str(operario).strip()
        self.preguntas: list[dict[str, Any]] = []
        self.controles_respuesta: list[dict[str, Any]] = []

        self.setWindowTitle("Formulario Operario")
        self.resize(980, 720)

        self._configurar_ui()
        self._cargar_formulario()
        self._cargar_preguntas()

    def _resolver_formulario_inicial(
        self,
        formulario: Formulario | None,
        contexto: dict[str, Any] | None,
    ) -> Formulario | None:
        if formulario is not None:
            return formulario

        if contexto:
            id_formulario = str(contexto.get("id_formulario", "")).strip()
            if id_formulario:
                existente = self.formulario_service.obtener_formulario_por_id(
                    id_formulario
                )
                if existente:
                    return existente

            return Formulario.from_dict(
                {
                    "id_formulario": str(
                        contexto.get("id_formulario", "FORM-TEST")
                    ).strip()
                    or "FORM-TEST",
                    "identificador": str(
                        contexto.get("identificador")
                        or contexto.get("num_ordem")
                        or ""
                    ).strip(),
                    "id_apontamento": str(
                        contexto.get("id_apontamento")
                        or contexto.get("IdApontamento")
                        or "TEST"
                    ).strip(),
                    "fecha_formulario": str(
                        contexto.get("fecha_formulario")
                        or contexto.get("DtProducao")
                        or ""
                    ).strip(),
                    "area": str(
                        contexto.get("area")
                        or contexto.get("cod_setor")
                        or contexto.get("CodSetor")
                        or ""
                    ).strip(),
                    "maquina": str(
                        contexto.get("maquina")
                        or contexto.get("cod_recurso")
                        or contexto.get("CodRecurso")
                        or ""
                    ).strip(),
                    "cod_recurso": str(
                        contexto.get("cod_recurso")
                        or contexto.get("CodRecurso")
                        or contexto.get("maquina")
                        or ""
                    ).strip(),
                    "cod_setor": str(
                        contexto.get("cod_setor")
                        or contexto.get("CodSetor")
                        or contexto.get("area")
                        or ""
                    ).strip(),
                    "cod_ativ": contexto.get("cod_ativ") or contexto.get("CodAtiv"),
                    "turno": contexto.get("turno") or contexto.get("Turno"),
                    "hora_fim": contexto.get("hora_fim") or contexto.get("HoraFim"),
                    "operario": str(
                        contexto.get("operario") or contexto.get("operador") or ""
                    ).strip(),
                    "estacion": str(contexto.get("estacion", "")).strip(),
                    "evento_origen": str(
                        contexto.get("evento_origen", "test")
                    ).strip(),
                    "estado": str(
                        contexto.get("estado", ESTADO_EN_APERTURA)
                    ).strip()
                    or ESTADO_EN_APERTURA,
                    "descripcion_op": str(
                        contexto.get("descripcion_op")
                        or contexto.get("DescricaoOP")
                        or ""
                    ).strip(),
                    "descripcion_proceso": str(
                        contexto.get("descripcion_proceso")
                        or contexto.get("DescricaoProcesso")
                        or ""
                    ).strip(),
                    "observacion_general": str(
                        contexto.get("observacion_general")
                        or contexto.get("obs")
                        or ""
                    ).strip(),
                    "fecha_creacion": str(
                        contexto.get("fecha_creacion", "")
                    ).strip(),
                    "fecha_actualizacion": str(
                        contexto.get("fecha_actualizacion", "")
                    ).strip(),
                }
            )

        return self.formulario_service.obtener_siguiente_formulario_pendiente_operario()

    def _configurar_ui(self) -> None:
        self.layout_principal = QVBoxLayout(self)

        self.lbl_titulo = QLabel("Formulario de Operario")
        self.lbl_titulo.setAlignment(Qt.AlignCenter)
        self.lbl_titulo.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.layout_principal.addWidget(self.lbl_titulo)

        self.marco_info = QFrame()
        self.layout_info = QFormLayout(self.marco_info)

        self.lbl_id_formulario = QLabel("-")
        self.lbl_identificador = QLabel("-")
        self.lbl_id_apontamento = QLabel("-")
        self.lbl_fecha = QLabel("-")
        self.lbl_area = QLabel("-")
        self.lbl_maquina = QLabel("-")
        self.lbl_operario = QLabel("-")
        self.lbl_estado = QLabel("-")
        self.lbl_descripcion_op = QLabel("-")
        self.lbl_descripcion_proceso = QLabel("-")

        self.layout_info.addRow("ID Formulario:", self.lbl_id_formulario)
        self.layout_info.addRow("OP:", self.lbl_identificador)
        self.layout_info.addRow("IdApontamento:", self.lbl_id_apontamento)
        self.layout_info.addRow("Fecha:", self.lbl_fecha)
        self.layout_info.addRow("Área:", self.lbl_area)
        self.layout_info.addRow("Máquina:", self.lbl_maquina)
        self.layout_info.addRow("Operario:", self.lbl_operario)
        self.layout_info.addRow("Estado:", self.lbl_estado)
        self.layout_info.addRow("Descripción OP:", self.lbl_descripcion_op)
        self.layout_info.addRow("Descripción proceso:", self.lbl_descripcion_proceso)

        self.layout_principal.addWidget(self.marco_info)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        self.contenedor_preguntas = QWidget()
        self.layout_preguntas = QVBoxLayout(self.contenedor_preguntas)
        self.layout_preguntas.setContentsMargins(8, 8, 8, 8)
        self.layout_preguntas.setSpacing(12)
        self.scroll.setWidget(self.contenedor_preguntas)

        self.layout_principal.addWidget(self.scroll, 1)

        self.txt_observacion_general = QPlainTextEdit()
        self.txt_observacion_general.setPlaceholderText(
            "Observación general del formulario"
        )
        self.txt_observacion_general.setFixedHeight(110)
        self.layout_principal.addWidget(QLabel("Observación general:"))
        self.layout_principal.addWidget(self.txt_observacion_general)

        self.layout_botones = QHBoxLayout()
        self.btn_enviar = QPushButton("Enviar")
        self.btn_cancelar = QPushButton("Cancelar")

        self.btn_enviar.clicked.connect(self._enviar_formulario)
        self.btn_cancelar.clicked.connect(self.close)

        self.layout_botones.addStretch()
        self.layout_botones.addWidget(self.btn_enviar)
        self.layout_botones.addWidget(self.btn_cancelar)

        self.layout_principal.addLayout(self.layout_botones)

    def _cargar_formulario(self) -> None:
        if not self.formulario:
            QMessageBox.information(
                self,
                "Formulario",
                "No hay formularios pendientes para el operario.",
            )
            self.btn_enviar.setEnabled(False)
            return

        if self.operario_seleccionado:
            self.formulario = self.formulario_service.asignar_operario(
                self.formulario.id_formulario,
                self.operario_seleccionado,
            )

        if self.formulario.estado == ESTADO_EN_APERTURA:
            self.formulario = (
                self.formulario_service.marcar_formulario_pendiente_operario(
                    self.formulario.id_formulario
                )
            )
        elif self.formulario.estado != ESTADO_PENDIENTE_OPERARIO:
            self.formulario = self.formulario_service.obtener_formulario_por_id(
                self.formulario.id_formulario
            ) or self.formulario

        self.lbl_id_formulario.setText(self.formulario.id_formulario)
        self.lbl_identificador.setText(self.formulario.identificador)
        self.lbl_id_apontamento.setText(self.formulario.id_apontamento)
        self.lbl_fecha.setText(self.formulario.fecha_formulario)
        self.lbl_area.setText(self.formulario.area)
        self.lbl_maquina.setText(self.formulario.maquina)
        self.lbl_operario.setText(
            self.formulario.operario or self.operario_seleccionado or "-"
        )
        self.lbl_estado.setText(self.formulario.estado)
        self.lbl_descripcion_op.setText(self.formulario.descripcion_op or "-")
        self.lbl_descripcion_proceso.setText(
            self.formulario.descripcion_proceso or "-"
        )
        self.txt_observacion_general.setPlainText(
            self.formulario.observacion_general or ""
        )

    def _cargar_preguntas(self) -> None:
        while self.layout_preguntas.count():
            item = self.layout_preguntas.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        self.controles_respuesta.clear()

        if not self.formulario:
            return

        self.preguntas = self._obtener_preguntas_para_formulario()

        if not self.preguntas:
            self.layout_preguntas.addWidget(
                QLabel("No hay preguntas configuradas para este contexto.")
            )
            self.layout_preguntas.addStretch()
            return

        for indice, pregunta in enumerate(self.preguntas, start=1):
            widget = self._crear_bloque_pregunta(indice, pregunta)
            self.layout_preguntas.addWidget(widget)

        self.layout_preguntas.addStretch()

    def _obtener_preguntas_para_formulario(self) -> list[dict[str, Any]]:
        area = self.formulario.area if self.formulario else ""
        maquina = self.formulario.maquina if self.formulario else ""
        operario = self.formulario.operario if self.formulario else ""

        candidatos = [
            (
                "listar_preguntas_para_contexto",
                {"area": area, "maquina": maquina, "operario": operario},
            ),
            (
                "listar_preguntas_operario",
                {"area": area, "maquina": maquina, "operario": operario},
            ),
            ("listar_preguntas", {"solo_activas": True}),
            ("obtener_preguntas_activas", {}),
        ]

        for nombre_metodo, kwargs in candidatos:
            metodo = getattr(self.pregunta_service, nombre_metodo, None)
            if callable(metodo):
                try:
                    preguntas = metodo(**kwargs)
                except TypeError:
                    try:
                        preguntas = metodo()
                    except Exception:
                        continue
                except Exception:
                    continue

                if isinstance(preguntas, list):
                    return self._filtrar_preguntas_por_contexto(preguntas)

        return []

    def _filtrar_preguntas_por_contexto(
        self,
        preguntas: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        if not self.formulario:
            return preguntas

        area_actual = (self.formulario.area or "").strip()
        maquina_actual = (self.formulario.maquina or "").strip()

        def extraer_lista(valor: Any) -> list[str]:
            if valor is None:
                return []
            if isinstance(valor, list):
                resultado: list[str] = []
                for item in valor:
                    if isinstance(item, dict):
                        for clave in (
                            "id_area",
                            "id_maquina",
                            "nombre",
                            "codigo",
                            "id",
                        ):
                            texto = str(item.get(clave, "")).strip()
                            if texto:
                                resultado.append(texto)
                                break
                    else:
                        texto = str(item).strip()
                        if texto:
                            resultado.append(texto)
                return resultado

            texto = str(valor).strip()
            return [texto] if texto else []

        def coincide_contexto(pregunta: dict[str, Any]) -> bool:
            areas = []
            maquinas = []

            for clave in (
                "areas_asociadas",
                "areas",
                "id_areas",
                "area",
                "id_area",
            ):
                areas.extend(extraer_lista(pregunta.get(clave)))

            for clave in (
                "maquinas_asociadas",
                "maquinas",
                "id_maquinas",
                "maquina",
                "id_maquina",
            ):
                maquinas.extend(extraer_lista(pregunta.get(clave)))

            coincide_area = True if not areas else area_actual in areas
            coincide_maquina = True if not maquinas else maquina_actual in maquinas
            return coincide_area and coincide_maquina

        preguntas_filtradas = [
            pregunta
            for pregunta in preguntas
            if bool(pregunta.get("activa", True)) and coincide_contexto(pregunta)
        ]

        preguntas_filtradas.sort(
            key=lambda pregunta: (
                int(pregunta.get("orden", 9999))
                if str(pregunta.get("orden", "")).isdigit()
                else 9999,
                str(pregunta.get("id_pregunta", "")),
            )
        )
        return preguntas_filtradas

    def _crear_bloque_pregunta(
        self, indice: int, pregunta: dict[str, Any]
    ) -> QWidget:
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)

        layout = QVBoxLayout(frame)

        texto = str(
            pregunta.get("texto")
            or pregunta.get("pregunta")
            or pregunta.get("enunciado")
            or f"Pregunta {indice}"
        ).strip()
        obligatoria = self._pregunta_es_obligatoria(pregunta)

        lbl_pregunta = QLabel(f"{indice}. {texto}{' *' if obligatoria else ''}")
        lbl_pregunta.setWordWrap(True)
        lbl_pregunta.setStyleSheet("font-weight: bold;")
        layout.addWidget(lbl_pregunta)

        ayuda = str(pregunta.get("ayuda") or pregunta.get("descripcion") or "").strip()
        if ayuda:
            lbl_ayuda = QLabel(ayuda)
            lbl_ayuda.setWordWrap(True)
            layout.addWidget(lbl_ayuda)

        control_info = self._crear_control_respuesta(pregunta)
        layout.addWidget(control_info["widget"])

        self.controles_respuesta.append(
            {
                "pregunta": pregunta,
                "tipo_control": control_info["tipo_control"],
                "widget": control_info["widget"],
                "meta": control_info.get("meta", {}),
            }
        )

        return frame

    def _crear_control_respuesta(self, pregunta: dict[str, Any]) -> dict[str, Any]:
        tipo = str(
            pregunta.get("tipo")
            or pregunta.get("tipo_pregunta")
            or pregunta.get("tipo_respuesta")
            or "texto"
        ).strip().lower()

        if tipo in {"numero", "num", "entero"}:
            widget = QSpinBox()
            widget.setMinimum(0)
            widget.setMaximum(999999999)
            return {"tipo_control": "numero", "widget": widget}

        if tipo in {"textarea", "texto_largo", "observacion"}:
            widget = QPlainTextEdit()
            widget.setFixedHeight(100)
            return {"tipo_control": "texto_largo", "widget": widget}

        if tipo in {"combo", "seleccion", "seleccion_unica", "opcion", "lista"}:
            combo = QComboBox()
            combo.addItem("Seleccione una opción", "")
            for opcion in self._obtener_opciones_pregunta(pregunta):
                combo.addItem(opcion["texto"], opcion["id_opcion"])
            return {"tipo_control": "combo", "widget": combo}

        if tipo in {"si_no", "booleano", "bool"}:
            contenedor = QWidget()
            layout = QHBoxLayout(contenedor)
            layout.setContentsMargins(0, 0, 0, 0)

            grupo = QButtonGroup(contenedor)
            rb_si = QRadioButton("Sí")
            rb_no = QRadioButton("No")

            grupo.addButton(rb_si)
            grupo.addButton(rb_no)

            layout.addWidget(rb_si)
            layout.addWidget(rb_no)
            layout.addStretch()

            return {
                "tipo_control": "booleano",
                "widget": contenedor,
                "meta": {
                    "grupo": grupo,
                    "rb_si": rb_si,
                    "rb_no": rb_no,
                },
            }

        widget = QLineEdit()
        return {"tipo_control": "texto", "widget": widget}

    def _obtener_opciones_pregunta(
        self, pregunta: dict[str, Any]
    ) -> list[dict[str, str]]:
        opciones_crudas = (
            pregunta.get("opciones")
            or pregunta.get("opciones_pregunta")
            or pregunta.get("alternativas")
            or []
        )

        opciones: list[dict[str, str]] = []

        for item in opciones_crudas:
            if isinstance(item, dict):
                id_opcion = str(
                    item.get("id_opcion")
                    or item.get("id")
                    or item.get("codigo")
                    or item.get("valor")
                    or ""
                ).strip()
                texto = str(
                    item.get("texto")
                    or item.get("descripcion")
                    or item.get("nombre")
                    or item.get("label")
                    or id_opcion
                ).strip()
                opciones.append(
                    {
                        "id_opcion": id_opcion,
                        "texto": texto,
                    }
                )
            else:
                texto = str(item).strip()
                if texto:
                    opciones.append(
                        {
                            "id_opcion": texto,
                            "texto": texto,
                        }
                    )

        return opciones

    def _pregunta_es_obligatoria(self, pregunta: dict[str, Any]) -> bool:
        return bool(
            pregunta.get("obligatoria", False)
            or pregunta.get("requerida", False)
            or pregunta.get("required", False)
        )

    def _obtener_valor_control(
        self, control: dict[str, Any]
    ) -> tuple[str | None, int | None, str | None]:
        tipo_control = control["tipo_control"]
        widget = control["widget"]
        meta = control.get("meta", {})

        if tipo_control == "numero":
            valor_numero = int(widget.value())
            return None, valor_numero, None

        if tipo_control == "texto_largo":
            texto = str(widget.toPlainText()).strip()
            return texto or None, None, None

        if tipo_control == "combo":
            id_opcion = str(widget.currentData() or "").strip()
            texto = str(widget.currentText()).strip()
            if not id_opcion:
                return None, None, None
            return texto or None, None, id_opcion

        if tipo_control == "booleano":
            if meta["rb_si"].isChecked():
                return "Sí", None, "SI"
            if meta["rb_no"].isChecked():
                return "No", None, "NO"
            return None, None, None

        texto = str(widget.text()).strip()
        return texto or None, None, None

    def _validar_respuestas(self) -> tuple[bool, str]:
        for control in self.controles_respuesta:
            pregunta = control["pregunta"]
            if not self._pregunta_es_obligatoria(pregunta):
                continue

            texto, numero, id_opcion = self._obtener_valor_control(control)
            if texto is None and numero is None and not id_opcion:
                texto_pregunta = str(
                    pregunta.get("texto")
                    or pregunta.get("pregunta")
                    or pregunta.get("enunciado")
                    or pregunta.get("id_pregunta")
                    or "Sin texto"
                ).strip()
                return False, f"Debes responder la pregunta: {texto_pregunta}"

        return True, ""

    def _guardar_respuesta(
        self,
        id_pregunta: str,
        texto: str | None,
        numero: int | None,
        id_opcion: str | None,
    ) -> None:
        self.respuesta_service.crear_respuesta(
            id_formulario=self.formulario.id_formulario,
            id_pregunta=id_pregunta,
            respuesta_texto=texto,
            respuesta_numero=numero,
            id_opcion=id_opcion,
            accion_correctiva_aplicada=None,
        )

    def _enviar_formulario(self) -> None:
        if not self.formulario:
            QMessageBox.warning(self, "Formulario", "No hay un formulario cargado.")
            return

        ok, mensaje = self._validar_respuestas()
        if not ok:
            QMessageBox.warning(self, "Validación", mensaje)
            return

        try:
            for control in self.controles_respuesta:
                pregunta = control["pregunta"]
                texto, numero, id_opcion = self._obtener_valor_control(control)

                if texto is None and numero is None and not id_opcion:
                    continue

                id_pregunta = str(pregunta.get("id_pregunta", "")).strip()
                if not id_pregunta:
                    continue

                self._guardar_respuesta(
                    id_pregunta=id_pregunta,
                    texto=texto,
                    numero=numero,
                    id_opcion=id_opcion,
                )

            observacion_general = str(
                self.txt_observacion_general.toPlainText()
            ).strip()
            self.formulario = self.formulario_service.marcar_formulario_completado(
                self.formulario.id_formulario,
                observacion_general=observacion_general,
            )

            QMessageBox.information(
                self,
                "Formulario",
                "Formulario enviado correctamente.",
            )
            self.close()

        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo enviar el formulario.\n\n{exc}",
            )
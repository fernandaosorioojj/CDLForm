from __future__ import annotations

from datetime import datetime

from PyQt5.QtCore import QObject, QSize, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon, QPainter, QPen
from PyQt5.QtWidgets import (
    QFrame,
    QGraphicsDropShadowEffect,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from presenters.dashboard_gestion_presenter import DashboardGestionPresenter
from utils.assets import image_path
from widgets.asset_image import AssetImage
from widgets.base_window import BaseWindow


class DashboardKpiWorker(QObject):
    finished = pyqtSignal(dict)
    failed = pyqtSignal(str)

    def __init__(self, presenter: DashboardGestionPresenter) -> None:
        super().__init__()
        self.presenter = presenter

    def run(self) -> None:
        try:
            self.finished.emit(self.presenter.obtener_metricas_dashboard())
        except Exception as exc:
            self.failed.emit(str(exc))


class DashboardMetricChip(QFrame):
    def __init__(self, title: str, value: str = "--", parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("dashboardMetricChip")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(10)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("dashboardMetricTitle")
        title_label.setWordWrap(True)

        icon_shell = QFrame()
        icon_shell.setObjectName("dashboardCardIconShell")
        icon_layout = QHBoxLayout(icon_shell)
        icon_layout.setContentsMargins(8, 8, 8, 8)
        icon_layout.setSpacing(0)
        icon_layout.addWidget(AssetImage("leaf-accent.svg", 18, 18), 0, Qt.AlignCenter)

        self.value_label = QLabel(value)
        self.value_label.setObjectName("dashboardMetricValue")

        header.addWidget(title_label, 1)
        header.addWidget(icon_shell, 0, Qt.AlignTop)

        layout.addLayout(header)
        layout.addWidget(self.value_label)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)


class MiniBarChart(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._series: list[dict[str, object]] = []
        self.setMinimumHeight(180)
        self.setObjectName("dashboardBarChart")

    def set_series(self, series: list[dict[str, object]]) -> None:
        self._series = series
        self.update()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        rect = self.rect().adjusted(12, 14, -12, -18)
        if rect.width() <= 0 or rect.height() <= 0:
            return

        label_height = 26
        value_height = 24
        chart_rect = rect.adjusted(0, value_height, 0, -label_height)

        painter.setPen(QPen(QColor(110, 133, 154, 58), 1))
        for step in range(1, 4):
            y = chart_rect.bottom() - int(chart_rect.height() * (step / 4))
            painter.drawLine(chart_rect.left(), y, chart_rect.right(), y)

        if not self._series:
            painter.setPen(QColor(92, 109, 126, 195))
            painter.drawText(rect, Qt.AlignCenter, "Sin datos")
            return

        max_value = max(int(item.get("value", 0) or 0) for item in self._series)
        max_value = max(max_value, 1)

        spacing = 12
        total_spacing = spacing * max(len(self._series) - 1, 0)
        bar_width = max(22, int((chart_rect.width() - total_spacing) / max(len(self._series), 1)))
        total_width = bar_width * len(self._series) + total_spacing
        start_x = chart_rect.left() + max(0, int((chart_rect.width() - total_width) / 2))

        value_font = QFont(self.font())
        value_font.setPointSize(9)
        value_font.setBold(True)
        label_font = QFont(self.font())
        label_font.setPointSize(8)

        for index, item in enumerate(self._series):
            value = int(item.get("value", 0) or 0)
            label = str(item.get("label", ""))
            color = QColor(str(item.get("color", "#B5D7F4")))

            bar_height = int((value / max_value) * max(28, chart_rect.height() - 10))
            x = start_x + index * (bar_width + spacing)
            y = chart_rect.bottom() - bar_height

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(255, 255, 255, 28))
            painter.drawRoundedRect(x, chart_rect.top(), bar_width, chart_rect.height(), 8, 8)

            painter.setBrush(color)
            painter.drawRoundedRect(x, y, bar_width, bar_height, 8, 8)

            painter.setFont(value_font)
            painter.setPen(QColor(70, 88, 106, 235))
            painter.drawText(x - 6, y - 18, bar_width + 12, 16, Qt.AlignCenter, str(value))

            painter.setFont(label_font)
            painter.setPen(QColor(92, 109, 126, 220))
            painter.drawText(
                x - 10,
                chart_rect.bottom() + 8,
                bar_width + 20,
                label_height,
                Qt.AlignCenter | Qt.TextWordWrap,
                label,
            )


class DashboardChartPanel(QFrame):
    def __init__(
        self,
        *,
        title: str,
        subtitle: str,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("dashboardChartPanel")

        sombra = QGraphicsDropShadowEffect(self)
        sombra.setBlurRadius(30)
        sombra.setOffset(0, 12)
        sombra.setColor(QColor(72, 86, 102, 48))
        self.setGraphicsEffect(sombra)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(12)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("dashboardChartTitle")
        title_label.setWordWrap(True)

        icon_shell = QFrame()
        icon_shell.setObjectName("dashboardCardIconShell")
        icon_layout = QHBoxLayout(icon_shell)
        icon_layout.setContentsMargins(10, 10, 10, 10)
        icon_layout.setSpacing(0)
        icon_layout.addWidget(AssetImage("leaf-accent.svg", 20, 20), 0, Qt.AlignCenter)

        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("dashboardChartSubtitle")
        subtitle_label.setWordWrap(True)

        self.chart = MiniBarChart()

        header.addWidget(title_label, 1)
        header.addWidget(icon_shell, 0, Qt.AlignTop)

        layout.addLayout(header)
        layout.addWidget(subtitle_label)
        layout.addWidget(self.chart)

    def set_series(self, series: list[dict[str, object]]) -> None:
        self.chart.set_series(series)


class DashboardGestionView(BaseWindow):
    qss_files = ("base.qss", "dashboard_gestion.qss")

    def __init__(self, usuario: str = "") -> None:
        super().__init__()

        self.presenter = DashboardGestionPresenter()
        self.usuario = str(usuario or "").strip()
        self.admin_preguntas_view = None
        self.reportes_view = None
        self.auditoria_formularios_view = None
        self.acciones_correctivas_view = None
        self.login_view = None
        self.metric_acciones = None
        self.metric_formularios = None
        self.metric_completados = None
        self.chart_acciones = None
        self.chart_formularios = None
        self.status_text = None
        self.hero_title_label = None
        self.hero_subtitle_label = None
        self._kpi_thread = None
        self._kpi_worker = None

        self.setObjectName("dashboardGestionView")
        self.setWindowTitle("CDLform - Gestion")
        self.resize(1320, 780)

        self._init_ui()
        self.apply_styles()
        self._aplicar_kpis_demo()
        QTimer.singleShot(250, self._cargar_kpis_dashboard_async)

    def _init_ui(self) -> None:
        root = QHBoxLayout(self)
        root.setContentsMargins(24, 20, 24, 20)
        root.setSpacing(18)

        root.addWidget(self._build_side_panel())
        root.addLayout(self._build_center_column(), 1)

    def _build_nav_rail(self) -> QFrame:
        rail = QFrame()
        rail.setObjectName("dashboardNavRail")
        rail.setFixedWidth(96)

        layout = QVBoxLayout(rail)
        layout.setContentsMargins(12, 16, 12, 16)
        layout.setSpacing(14)

        brand = QLabel("CDL")
        brand.setObjectName("dashboardBrand")
        brand.setAlignment(Qt.AlignCenter)
        layout.addWidget(brand)

        nav_items = [
            ("Inicio", "icon-reports.svg", True),
            ("Preguntas", "icon-questions.svg", False),
            ("Reportes", "icon-reports.svg", False),
            ("Acciones", "icon-corrective.svg", False),
            ("Auditoria", "icon-audit.svg", False),
        ]
        for texto, icono, activo in nav_items:
            boton = self._crear_boton_nav(texto, icono, activo)
            layout.addWidget(boton)

        layout.addStretch()

        salir = self._crear_boton_nav("Salir", "icon-audit.svg", False)
        salir.clicked.connect(self.close)
        layout.addWidget(salir)

        return rail

    def _build_center_column(self) -> QVBoxLayout:
        center = QVBoxLayout()
        center.setSpacing(18)

        center.addWidget(self._build_hero_card())

        placeholder_row = QHBoxLayout()
        placeholder_row.setSpacing(18)

        self.metric_acciones = DashboardMetricChip("Acciones correctivas", "--")
        self.metric_formularios = DashboardMetricChip("Formularios del dia", "--")
        self.metric_completados = DashboardMetricChip("Seguimiento", "--")

        placeholder_row.addWidget(self.metric_acciones, 1)
        placeholder_row.addWidget(self.metric_formularios, 1)
        placeholder_row.addWidget(self.metric_completados, 1)
        center.addLayout(placeholder_row)

        charts_row = QHBoxLayout()
        charts_row.setSpacing(18)

        self.chart_acciones = DashboardChartPanel(
            title="Acciones correctivas - 7 dias",
            subtitle="Conteo diario de acciones correctivas registradas recientemente.",
        )
        self.chart_formularios = DashboardChartPanel(
            title="Formularios del dia por estado",
            subtitle="Distribucion visual del trabajo actual segun el estado operativo.",
        )

        charts_row.addWidget(self.chart_acciones, 1)
        charts_row.addWidget(self.chart_formularios, 1)
        center.addLayout(charts_row)

        return center

    def _obtener_saludo_dashboard(self) -> str:
        hora = datetime.now().hour
        nombre = self.usuario or "equipo"

        if hora < 12:
            return f"Buenos dias, {nombre}"
        if hora < 20:
            return f"Buenas tardes, {nombre}"
        return f"Buenas noches, {nombre}"

    def _aplicar_kpis_demo(
        self,
        *,
        acciones: str = "--",
        formularios: str = "--",
        completados: str = "--",
    ) -> None:
        if self.metric_acciones is not None:
            self.metric_acciones.set_value(str(acciones))
        if self.metric_formularios is not None:
            self.metric_formularios.set_value(str(formularios))
        if self.metric_completados is not None:
            self.metric_completados.set_value(str(completados))

    def _aplicar_kpis_dashboard(self, metricas: dict) -> None:
        kpis = metricas.get("kpis", {})
        if self.metric_acciones is not None:
            self.metric_acciones.set_value(str(kpis.get("acciones_total", 0)))
        if self.metric_formularios is not None:
            self.metric_formularios.set_value(str(kpis.get("formularios_hoy_total", 0)))
        if self.metric_completados is not None:
            self.metric_completados.set_value(
                str(kpis.get("formularios_hoy_completados", 0))
            )

        if self.chart_formularios is not None:
            estado_colors = {
                "Pendiente": "#B5D7F4",
                "Apertura": "#D8C7E8",
                "En progreso": "#E6D7C6",
                "Completado": "#C6D4E5",
                "Cancelado": "#E8D8E5",
            }
            formularios_serie = [
                {
                    "label": item.get("label", ""),
                    "value": item.get("value", 0),
                    "color": estado_colors.get(str(item.get("label")), "#B5D7F4"),
                }
                for item in metricas.get("formularios_hoy", [])
            ]
            self.chart_formularios.set_series(formularios_serie)

        if self.chart_acciones is not None:
            acciones_colors = [
                "#B5D7F4",
                "#D8C7E8",
                "#E6D7C6",
                "#D8E1EE",
                "#F0D9E8",
                "#C6D4E5",
                "#D8D1C6",
            ]
            acciones_serie = [
                {
                    "label": item.get("label", ""),
                    "value": item.get("value", 0),
                    "color": acciones_colors[index % len(acciones_colors)],
                }
                for index, item in enumerate(metricas.get("acciones_semana", []))
            ]
            self.chart_acciones.set_series(acciones_serie)

        if self.status_text is not None:
            self.status_text.setText(
                f"Ultima actualizacion: {datetime.now().strftime('%H:%M:%S')}"
            )

    def _cargar_kpis_dashboard(self) -> None:
        metricas = self.presenter.obtener_metricas_dashboard()
        self._aplicar_kpis_dashboard(metricas)

    def _cargar_kpis_dashboard_async(self) -> None:
        if self._kpi_thread is not None and self._kpi_thread.isRunning():
            return

        self._kpi_thread = QThread(self)
        self._kpi_worker = DashboardKpiWorker(self.presenter)
        self._kpi_worker.moveToThread(self._kpi_thread)

        self._kpi_thread.started.connect(self._kpi_worker.run)
        self._kpi_worker.finished.connect(self._aplicar_kpis_dashboard)
        self._kpi_worker.finished.connect(self._kpi_thread.quit)
        self._kpi_worker.finished.connect(self._kpi_worker.deleteLater)
        self._kpi_worker.failed.connect(self._manejar_error_kpis_dashboard)
        self._kpi_worker.failed.connect(self._kpi_thread.quit)
        self._kpi_worker.failed.connect(self._kpi_worker.deleteLater)
        self._kpi_thread.finished.connect(self._finalizar_carga_kpis_dashboard)
        self._kpi_thread.finished.connect(self._kpi_thread.deleteLater)

        if self.status_text is not None:
            self.status_text.setText("Actualizando KPI...")

        self._kpi_thread.start()

    def _manejar_error_kpis_dashboard(self, _error: str) -> None:
        self._aplicar_kpis_demo()
        if self.status_text is not None:
            self.status_text.setText(
                "No fue posible actualizar los KPI."
            )

    def _finalizar_carga_kpis_dashboard(self) -> None:
        self._kpi_worker = None
        self._kpi_thread = None

    def _build_hero_card(self) -> QFrame:
        hero = QFrame()
        hero.setObjectName("dashboardHero")
        hero_layout = QHBoxLayout(hero)
        hero_layout.setContentsMargins(28, 24, 28, 24)
        hero_layout.setSpacing(26)

        textos = QVBoxLayout()
        textos.setSpacing(10)

        eyebrow = QLabel("Gestion central")
        eyebrow.setObjectName("dashboardEyebrow")

        self.hero_title_label = QLabel(self._obtener_saludo_dashboard())
        self.hero_title_label.setObjectName("dashboardHeroTitle")
        self.hero_title_label.setWordWrap(True)

        self.hero_subtitle_label = QLabel(
            "Hoy es un buen momento para revisar el pulso del turno y mantener la operacion en movimiento."
        )
        self.hero_subtitle_label.setObjectName("dashboardHeroSubtitle")
        self.hero_subtitle_label.setWordWrap(True)

        cta_row = QHBoxLayout()
        cta_row.setContentsMargins(0, 6, 0, 0)
        cta_row.setSpacing(10)

        abrir_acciones = QPushButton("Ver acciones")
        abrir_acciones.setObjectName("dashboardPrimaryAction")
        abrir_acciones.clicked.connect(self.abrir_acciones_correctivas)

        abrir_reportes = QPushButton("Abrir reportes")
        abrir_reportes.setObjectName("dashboardSecondaryAction")
        abrir_reportes.clicked.connect(self.abrir_reportes)

        cta_row.addWidget(abrir_acciones)
        cta_row.addWidget(abrir_reportes)
        cta_row.addStretch()

        textos.addWidget(eyebrow)
        textos.addWidget(self.hero_title_label)
        textos.addWidget(self.hero_subtitle_label)
        textos.addLayout(cta_row)
        textos.addStretch()

        hero_layout.addLayout(textos, 1)

        visual = AssetImage("workflow-illustration.svg", 340, 200)
        visual.setObjectName("dashboardHeroVisual")
        hero_layout.addWidget(visual, 0, Qt.AlignRight | Qt.AlignVCenter)

        return hero

    def _build_side_panel(self) -> QFrame:
        panel = QFrame()
        panel.setObjectName("dashboardSidePanel")
        panel.setFixedWidth(248)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(16)

        brand = QLabel("CDLform")
        brand.setObjectName("dashboardSidebarBrand")
        layout.addWidget(brand)

        profile = QFrame()
        profile.setObjectName("dashboardProfile")
        profile_layout = QVBoxLayout(profile)
        profile_layout.setContentsMargins(16, 16, 16, 16)
        profile_layout.setSpacing(18)

        avatar = AssetImage("leaf-accent.svg", 72, 72)
        avatar.setObjectName("dashboardProfileAvatar")
        avatar.setMaximumHeight(72)

        perfil_titulo = QLabel(self.usuario or "Usuario")
        perfil_titulo.setObjectName("dashboardProfileTitle")

        profile_layout.addWidget(avatar, 0, Qt.AlignCenter)
        profile_layout.addWidget(perfil_titulo, 0, Qt.AlignLeft)
        layout.addWidget(profile)

        quick_buttons = [
            ("Preguntas", self.abrir_admin_preguntas),
            ("Reportes", self.abrir_reportes),
            ("Acciones", self.abrir_acciones_correctivas),
            ("Auditoria", self.abrir_auditoria_formularios),
        ]
        for texto, callback in quick_buttons:
            boton = QPushButton(texto)
            boton.setObjectName("dashboardQuickButton")
            boton.clicked.connect(callback)
            layout.addWidget(boton)

        btn_cargar_kpis = QPushButton("Actualizar graficas")
        btn_cargar_kpis.setObjectName("dashboardQuickButton")
        btn_cargar_kpis.clicked.connect(self._cargar_kpis_dashboard_async)
        layout.addWidget(btn_cargar_kpis)

        status = QFrame()
        status.setObjectName("dashboardStatus")
        status_layout = QVBoxLayout(status)
        status_layout.setContentsMargins(16, 16, 16, 16)
        status_layout.setSpacing(8)

        status_tag = QLabel("Estado")
        status_tag.setObjectName("dashboardStatusTag")
        status_title = QLabel("Ultima actualizacion")
        status_title.setObjectName("dashboardStatusTitle")
        self.status_text = QLabel(
            "Esperando primera carga de KPI."
        )
        self.status_text.setWordWrap(True)
        self.status_text.setObjectName("dashboardStatusText")

        status_layout.addWidget(status_tag)
        status_layout.addWidget(status_title)
        status_layout.addWidget(self.status_text)
        layout.addStretch()
        layout.addWidget(status)

        btn_logout = QPushButton("Log out")
        btn_logout.setObjectName("dashboardQuickButton")
        btn_logout.clicked.connect(self.cerrar_sesion)
        layout.addWidget(btn_logout)

        return panel

    def _crear_boton_nav(self, texto: str, icono: str, activo: bool) -> QPushButton:
        boton = QPushButton(texto)
        boton.setObjectName("dashboardNavButton")
        boton.setProperty("active", activo)
        boton.setCursor(Qt.PointingHandCursor)
        boton.setIcon(QIcon(image_path(icono)))
        boton.setIconSize(QSize(20, 20))

        if texto == "Preguntas":
            boton.clicked.connect(self.abrir_admin_preguntas)
        elif texto == "Reportes":
            boton.clicked.connect(self.abrir_reportes)
        elif texto == "Acciones":
            boton.clicked.connect(self.abrir_acciones_correctivas)
        elif texto == "Auditoria":
            boton.clicked.connect(self.abrir_auditoria_formularios)

        return boton


    def abrir_admin_preguntas(self) -> None:
        try:
            self.admin_preguntas_view = self.presenter.crear_admin_preguntas_view()
            self.admin_preguntas_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir la administracion de preguntas.\n\n{exc}",
            )

    def abrir_reportes(self) -> None:
        try:
            self.reportes_view = self.presenter.crear_reportes_view()
            self.reportes_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir el modulo de reportes.\n\n{exc}",
            )

    def abrir_auditoria_formularios(self) -> None:
        try:
            self.auditoria_formularios_view = (
                self.presenter.crear_auditoria_formularios_view()
            )
            self.auditoria_formularios_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir la auditoria de formularios.\n\n{exc}",
            )

    def abrir_acciones_correctivas(self) -> None:
        try:
            self.acciones_correctivas_view = (
                self.presenter.crear_acciones_correctivas_view()
            )
            self.acciones_correctivas_view.show()
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Error",
                f"No fue posible abrir las acciones correctivas.\n\n{exc}",
            )

    def cerrar_sesion(self) -> None:
        from ui.login import LoginView

        self.login_view = LoginView()
        self.login_view.show()
        self.close()

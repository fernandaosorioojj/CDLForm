from utils.style_loader import load_qss_files


def apply_view_style(widget, *qss_files: str) -> None:
    qss = load_qss_files(*qss_files)
    if qss:
        widget.setStyleSheet(qss)


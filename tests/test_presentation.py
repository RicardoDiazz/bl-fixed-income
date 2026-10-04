import os


def test_presentation_dashboard_exists():
    path = "dashboard/presentation.py"
    assert os.path.exists(path), f"Falta el dashboard de presentacion: {path}"
    assert os.path.getsize(path) > 100, f"El archivo {path} esta vacio"


def test_static_reports_exist_and_valid():
    html_path = "dashboard/report/report.html"
    pdf_path = "dashboard/report/report.pdf"

    assert os.path.exists(html_path), f"Falta el reporte HTML: {html_path}"
    assert os.path.exists(pdf_path), f"Falta el reporte PDF: {pdf_path}"

    assert os.path.getsize(html_path) > 200, "El reporte HTML es demasiado pequeno"
    assert os.path.getsize(pdf_path) > 200, "El reporte PDF es demasiado pequeno"

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    assert "Black-Litterman" in html_content, "El HTML no contiene los terminos clave"


def test_makefile_has_deploy_and_report_targets():
    assert os.path.exists("Makefile"), "No existe el Makefile"
    with open("Makefile", "r", encoding="utf-8") as f:
        makefile_content = f.read()
    assert "report:" in makefile_content, "Falta la regla report: en el Makefile"
    assert "deploy:" in makefile_content, "Falta la regla deploy: en el Makefile"

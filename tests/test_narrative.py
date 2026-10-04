import os


def test_s16_narrative_files_exist_and_non_empty():
    required_files = [
        "configs/regime_analysis.md",
        "configs/omega_analysis.md",
        "configs/weights_analysis.md",
        "configs/main_narrative.md",
    ]
    for path in required_files:
        assert os.path.exists(path), f"Falta el archivo requerido: {path}"
        assert os.path.getsize(path) > 100, f"El archivo {path} esta vacio o incompleto"


def test_main_narrative_key_sections():
    with open("configs/main_narrative.md", "r", encoding="utf-8") as f:
        content = f.read()
    assert "Ricardo Delgadillo" in content, "Falta el encabezado de autores"
    assert "Black-Litterman" in content, "Falta la seccion conceptual principal"
    assert (
        "Diebold-Mariano" in content or "Omega_t" in content
    ), "Falta la sintesis de resultados"

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
DOC_DIR = DATA_DIR / "docs"
EXCEL_DIR = DATA_DIR / "excels"

DIRECTORY_BY_SUFFIX = {
    ".pdf": PDF_DIR,
    ".docx": DOC_DIR,
    ".xlsx": EXCEL_DIR,
    ".xls": EXCEL_DIR,
}


def ensure_document_directories() -> None:
    for directory in (PDF_DIR, DOC_DIR, EXCEL_DIR):
        directory.mkdir(parents=True, exist_ok=True)


def get_target_directory(filename: str) -> Path:
    suffix = Path(filename).suffix.lower()
    if suffix not in DIRECTORY_BY_SUFFIX:
        raise ValueError(
            "Unsupported file type. Allowed extensions: .pdf, .docx, .xlsx, .xls."
        )
    return DIRECTORY_BY_SUFFIX[suffix]


def iter_document_paths() -> list[Path]:
    ensure_document_directories()

    paths: list[Path] = []
    for directory in (PDF_DIR, DOC_DIR, EXCEL_DIR):
        for file_path in sorted(directory.iterdir()):
            if file_path.is_file():
                paths.append(file_path)
    return paths


def find_document_path(filename: str) -> Path:
    for file_path in iter_document_paths():
        if file_path.name == filename:
            return file_path

    raise FileNotFoundError(f"Document `{filename}` was not found.")

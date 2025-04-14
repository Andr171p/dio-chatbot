from src.settings import BASE_DIR


UPLOADED_FILES_DIR = BASE_DIR / "uploaded_files"


ALLOWED_EXTENSIONS = {
    "txt",
    "pdf",
    "doc",
    "docx",
    "xls",
    "xlsx",
    "ppt",
    "pptx"
}

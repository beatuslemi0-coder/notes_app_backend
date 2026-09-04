from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".doc",
    ".docx",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def save_uploaded_file(
    file: UploadFile
) -> str:

    if not file.filename:
        raise ValueError("File name is required")

    extension = Path(file.filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(
            "File type is not allowed"
        )

    file_content = await file.read()

    if len(file_content) > MAX_FILE_SIZE:
        raise ValueError(
            "File size must not exceed 5 MB"
        )

    UPLOAD_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    filename = f"{uuid4()}{extension}"

    file_path = UPLOAD_DIR / filename

    file_path.write_bytes(file_content)

    return str(file_path)
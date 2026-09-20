from pathlib import Path
from uuid import uuid4
from fastapi import UploadFile, HTTPException

ALLOWED_EXTENSIONS = {".jpg",".jpeg",".png",".webp",".gif"}
MAX_FILE_SIZE = 5 * 1024 * 1024

async def save_upload(file: UploadFile, directory: Path):
    if not file.filename:
        raise HTTPException(400, "No filename supplied")
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, "Invalid image type")
    data = await file.read()
    if len(data) > MAX_FILE_SIZE:
        raise HTTPException(400, "Maximum image size is 5 MB")
    directory.mkdir(parents=True, exist_ok=True)
    filename = uuid4().hex + ext
    (directory / filename).write_bytes(data)
    return f"/uploads/{directory.name}/{filename}"

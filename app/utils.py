from fastapi import UploadFile, HTTPException


def validate_file_type(file: UploadFile, allowed_extensions: set):
    ext = file.filename.split(".")[-1].lower()
    if ext not in allowed_extensions:
        raise HTTPException(status_code=415, detail="Invalid file type")


def validate_file_size(file_data: bytes, max_file_size: int):
    if len(file_data) > max_file_size:
        raise HTTPException(status_code=413, detail="File too large")


def validate_image_dimensions(width: int, height: int):
    if width <= 0 or height <= 0:
        raise HTTPException(status_code=400, detail="Width and height must be positive integers")

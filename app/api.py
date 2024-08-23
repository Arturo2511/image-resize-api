from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.security import APIKeyHeader
from PIL import Image
import io
import os
from dotenv import load_dotenv
from tempfile import NamedTemporaryFile
from app.utils import validate_file_type, validate_file_size, validate_image_dimensions

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("API_KEY")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE"))
ALLOWED_EXTENSIONS = set(os.getenv("ALLOWED_EXTENSIONS").split(','))

header_scheme = APIKeyHeader(name="X-API-Key", auto_error=False)

async def get_api_key(api_key: str = Depends(header_scheme)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")

'''
The code above defines a new API endpoint that resizes an image. The endpoint is a POST request to /resize-image, and it requires the following parameters:

width: The width of the resized image.
height: The height of the resized image.
file: The image file to resize.
The endpoint also requires an API key to be passed in the X-API-Key header. The API key is validated using the get_api_key dependency.
'''
@router.post("/resize-image")
async def resize_image(width: int, height: int, file: UploadFile, api_key: str = Depends(get_api_key)):
    validate_image_dimensions(width, height)

    file_data = await file.read()

    validate_file_size(file_data, MAX_FILE_SIZE)
    validate_file_type(file, ALLOWED_EXTENSIONS)


    try:
        image = Image.open(io.BytesIO(file_data))
        resized_image = image.resize((width, height))

        with NamedTemporaryFile(delete=False) as temp_file:
            resized_image.save(temp_file, format=image.format)

        return FileResponse(temp_file.name, media_type=file.content_type, filename=f"resized_{file.filename}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An internal server error occurred: {str(e)}")
    finally:
        file.file.close()

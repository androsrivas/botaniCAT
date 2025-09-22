import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import cloudinary.api

load_dotenv()

cloudinary.config(
    cloud_name = os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key = os.getenv("CLOUDINARY_API_KEY"),
    api_secret = os.getenv("CLOUDINARY_API_SECRET"),
    secure = True
)

def upload_image(image_path, public_id=None, folder="botaniCAT/img"):
    result = cloudinary.uploader.upload(
        image_path,
        public_id = public_id,
        folder = folder,
        overwrite = True,
        resource_type = "image"
    )

    return result

def delete_image(public_id):
    return cloudinary.uploader.destroy(public_id)
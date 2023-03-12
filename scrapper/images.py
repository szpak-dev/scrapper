from os import getenv

from dotenv import load_dotenv


class ImageUploader:
    def __init__(self):
        load_dotenv()
        cloudinary_url = getenv('CLOUDINARY_URL')
        if cloudinary_url is None:
            raise RuntimeError('Define CLOUDINARY_URL if you want to use Image Uploader')

    def upload(self):
        pass

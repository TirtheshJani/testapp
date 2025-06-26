import os
import uuid
from werkzeug.utils import secure_filename

class MediaService:
    BASE_DIR = 'storage'

    @staticmethod
    def athlete_media_path(athlete_id, media_type):
        return os.path.join(MediaService.BASE_DIR, 'athletes', athlete_id, media_type)

    @staticmethod
    def save_file(file_storage, athlete_id, media_type):
        directory = MediaService.athlete_media_path(athlete_id, media_type)
        os.makedirs(directory, exist_ok=True)
        ext = os.path.splitext(file_storage.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        path = os.path.join(directory, secure_filename(filename))
        file_storage.save(path)
        return path, filename

    @staticmethod
    def delete_file(path):
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

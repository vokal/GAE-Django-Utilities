from google.appengine.ext import db, blobstore
from google.appengine.api import files
from google.appengine.api.images import get_serving_url

from django.http import HttpResponse

class BlobModel(db.Model):
    '''
    Superclass for models that store a blobfile
    '''
    image = blobstore.BlobReferenceProperty()
    url = db.StringProperty()

    def upload_image(self, blob):
        # Create the file
        file_name = files.blobstore.create(mime_type='image/png')

        # Open the file and write to it
        with files.open(file_name, 'a') as f:
            f.write(blob)

        # Finalize the file. Do this before attempting to read it.
        files.finalize(file_name)

        # Get the file's blob key
        blob_key = files.blobstore.get_blob_key(file_name)
        # Store it
        self.image = blob_key
        self.url = get_serving_url(blob_key)

    def get_blob_response(self):
        response = HttpResponse()
        response[blobstore.BLOB_KEY_HEADER] = self.image.key()
        response['Content-Type'] = "image/png"

        return response

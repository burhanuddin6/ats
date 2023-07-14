# import settings
from django.conf import settings
import os
path = os.path.join(settings.MEDIA_ROOT, 'documents')
print(path)
print(settings.BASE_DIR)
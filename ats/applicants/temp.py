# import settings
import os
from django.conf import settings
path = os.path.join(settings.MEDIA_ROOT, 'documents')
print(path)
print(settings.BASE_DIR)

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)


<<<<<<< HEAD
__version__ = "0.3.0-pre1"
=======
__version__ = "0.3.0-pre2"
>>>>>>> origin/dev

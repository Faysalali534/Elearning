import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo_register.settings.dev')

app = Celery('demo_register')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'every-15-seconds': {
        'task': 'accounts.tasks.convert_time',
        'schedule': 15,
    },
    'every-27-seconds': {
        'task': 'accounts.tasks.inactive_users',
        'schedule': 27,
    },

}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

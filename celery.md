## Introduction

Celery is an asynchronous task queue/job queue based on distributed message passing. It is focused on real-time operation but supports scheduling as well. The execution units, called tasks, are executed concurrently on one or more worker nodes using multiprocessing, Eventlet, or gevent. Celery is commonly used to handle background tasks in Django applications.

## Prerequisites

- Python 3.x
- Django 3.x or higher
- Redis or RabbitMQ as the message broker

## Installation

1. **Install Celery and Redis**:

   You can install Celery and the Redis message broker using pip:

   ```bash
   pip install celery redis
   ```

2. **Install Celery Django Integration**:

   Install the Celery Django integration package:

   ```bash
   pip install django-celery-beat
   ```

## Configuration

1. **Configure Celery in Django Settings**:

   Open your Django `settings.py` file and add the following configurations:

   ```python
   # settings.py

   CELERY_BROKER_URL = 'redis://localhost:6379/0'
   CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
   CELERY_ACCEPT_CONTENT = ['json']
   CELERY_TASK_SERIALIZER = 'json'
   CELERY_RESULT_SERIALIZER = 'json'
   CELERY_TIMEZONE = 'UTC'
   ```

2. **Create a Celery Configuration Module**:

   Create a new file `celery.py` in your Django project’s main directory (where `settings.py` is located):

   ```python
   # celery.py

   from __future__ import absolute_import, unicode_literals
   import os
   from celery import Celery

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')

   app = Celery('your_project_name')

   app.config_from_object('django.conf:settings', namespace='CELERY')

   app.autodiscover_tasks()

   @app.task(bind=True)
   def debug_task(self):
       print(f'Request: {self.request!r}')
   ```

3. **Autodiscover Tasks**:

   In the `__init__.py` file of your project directory, add the following code to ensure Celery discovers tasks automatically:

   ```python
   # __init__.py

   from __future__ import absolute_import, unicode_literals
   from .celery import app as celery_app

   __all__ = ('celery_app',)
   ```

## Creating Tasks

1. **Define Celery Tasks**:

   In your Django app, create a `tasks.py` file and define your tasks:

   ```python
   # your_app_name/tasks.py

   from celery import shared_task

   @shared_task
   def add(x, y):
       return x + y

   @shared_task
   def multiply(x, y):
       return x * y
   ```

2. **Calling Tasks**:

   You can call tasks asynchronously from anywhere in your Django code:

   ```python
   from your_app_name.tasks import add

   add.delay(4, 4)
   ```

## Running Celery Worker

Start the Celery worker to begin processing tasks:

```bash
celery -A your_project_name worker --loglevel=info
```

Replace `your_project_name` with the name of your Django project.

## Scheduling Tasks

1. **Setup Celery Beat**:

   In `settings.py`, configure Celery Beat settings:

   ```python
   CELERY_BEAT_SCHEDULE = {
       'add-every-30-seconds': {
           'task': 'your_app_name.tasks.add',
           'schedule': 30.0,
           'args': (16, 16)
       },
   }
   ```

2. **Start Celery Beat**:

   Run Celery Beat to schedule tasks:

   ```bash
   celery -A your_project_name beat --loglevel=info
   ```


## Best Practices

- **Use Proper Task Naming**: Use meaningful names for tasks.
- **Handle Exceptions**: Implement proper error handling in your tasks.
- **Limit Concurrency**: Use `worker_concurrency` and `task_acks_late` settings for better control.

from celery import Celery

celery = Celery('tasks', broker='redis://redis:6379')

# Just a template for celery tasks. Maybe in the future

@celery.task
def add(x, y):
    return x + y

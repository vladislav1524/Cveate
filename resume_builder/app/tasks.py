from celery import shared_task, Celery


app = Celery('tasks', broker='redis://localhost:6379/0')

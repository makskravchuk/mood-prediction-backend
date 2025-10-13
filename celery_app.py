import os
from api import emotional_state
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    "tasks",
    broker=os.getenv("CELERY_BROKER_URL"),   # queue
    backend=os.getenv("CELERY_RESULT_BACKEND"),  # results
)
celery_app.autodiscover_tasks(['api.emotional_state.tasks'])
celery_app.conf.update(
    task_track_started=True,
    result_expires=300,
    worker_prefetch_multiplier=1,
)
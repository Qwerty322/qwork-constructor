from celery import Celery
from celery.schedules import crontab

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.timezone = 'UTC'

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.invest_task": "main-queue",
    "app.worker.notification_task": "main-queue",
}

celery_app.conf.beat_schedule = {
    "calculation": {
        'task': 'app.worker.invest_task',
        'schedule': crontab(hour="1-13", minute=30, day_of_week="1-5"),
    },
    "notification": {
        'task': 'app.worker.notification_task',
        'schedule': crontab(hour="1-13", minute=0, day_of_week="1-5"),
    },
    "testing_beat": {
        'task': 'app.worker.test_celery',
        'schedule': crontab(hour="1-13", minute="*/2", day_of_week="1-5"),
    },

}

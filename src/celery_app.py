from celery import Celery

celery_app = Celery("application")

celery_app.config_from_object("settings")

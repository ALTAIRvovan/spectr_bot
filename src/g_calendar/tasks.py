import datetime

from celery.schedules import crontab

import settings
from celery_app import celery_app
from .helpers import load_events_for_next_day
from vk.tasks import create_survey_before_training as vk_create_survey_before_training


@celery_app.task
def create_survey_before_training():
    events = load_events_for_next_day()
    for event in events:
        event_start_time = datetime.datetime.fromisoformat(event["start"]["dateTime"])
        time_of_creating_survey = event_start_time - datetime.timedelta(minutes=settings.BEFORE_TRAIN_NOTIFY_MINUTES)
        vk_create_survey_before_training.apply_async(args=[event_start_time, event], eta=time_of_creating_survey)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=3),
        create_survey_before_training.apply_async()
    )

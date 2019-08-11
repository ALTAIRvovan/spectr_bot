import random

from celery_app import celery_app
from .vk_app import vk_app
from settings import VK_CURRENT_SPECTRUM_TEAM_CHAT


@celery_app.task
def send_vk_msg(peer_id, text):
    try:
        random_id = random.randrange(1 << 63)
        vk_app.messages.send(peer_id=peer_id, message=text, random_id=random_id)
    except Exception as ex:
        print("Exception happen:", ex)


@celery_app.task
def create_survey_before_training(event_time, event):
    question = "Тренировка {}".format(event_time.strftime("%d.%m в %H:%M"))
    answers = ["Приду", "Не могу"]
    end_date = event_time.timestamp()
    poll = vk_app.polls.create(question=question, end_date=end_date, add_answers=answers)

    vk_app.messages.send(peer_id=VK_CURRENT_SPECTRUM_TEAM_CHAT,
                         attachment="poll{}_{}".format(poll.owner_id, poll.id))

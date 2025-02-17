import json

from flask import request, abort, make_response

import settings
from .flask_app import app
from vk.tasks import send_vk_msg, repost_new_post_into_team_chat


def parse_cmd(token, event_object):
    if token == "/chat_info":
        resp_text = "Chat chat_id: {}".format(event_object["peer_id"])
        peer_id = event_object["peer_id"] if event_object["peer_id"] > 2000000000 else event_object["from_id"]
        send_vk_msg.apply_async(args=[peer_id, resp_text])


def process_message_new(event_object):
    text = event_object["text"]
    tokens = str.split(text)
    if str.startswith(tokens[0], "[") and str.startswith(tokens[1], "/"):
        parse_cmd(tokens[1], event_object)
    elif str.startswith(tokens[0], "/"):
        parse_cmd(tokens[0], event_object)
    return make_response("ok", 200)


def process_wall_post_new(event_object, event):
    if event_object["owner_id"] != event["group_id"]:
        return make_response("wrong owner", 401)
    repost_new_post_into_team_chat.apply_async(args=[event_object["id"], event_object["owner_id"]])
    return make_response("ok", 200)


def process_confirmation(event_obj):
    if event_obj["group_id"] != settings.VK_GROUP_ID:
        abort(400)
    return make_response(settings.VK_CONFIRMATION_TOKEN, 200)


@app.route("/spectrum_bot/vk/callback", methods=["POST"])
def vk_callback():
    if not request.json:
        abort(400)

    event_type = request.json.get("type", None)

    if event_type == "confirmation":
        return process_confirmation(request.json)

    event_obj = request.json.get("object", None)
    if not event_type or not event_obj:
        abort(400)

    if request.json.get("secret", None) != settings.VK_CALLBACK_SECRET:
        abort(401)

    if event_type == "message_new":
        return process_message_new(event_obj)
    elif event_type == "wall_post_new":
        return process_wall_post_new(event_obj, request.json)
    make_response("ok", 200)

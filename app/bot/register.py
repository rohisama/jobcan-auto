# Standard library imports.
import os
import sys
import re
from logging import getLogger

# Related third party imports.
from slackbot.bot import respond_to

# Local application/library specific imports.
import slackbot_settings
from service.user_management import UserManagement

logger = getLogger(__name__)

@respond_to(r'\A登録')
def start_registration(message):
    user_id = message.user['id']
    um = UserManagement()
    reply = um.start_registration(user_id)
    um.release()

    if not _is_dm(message):
        message.reply("DMしますね")
        client = message._client
        channel = client.open_dm_channel(user_id)
        client.rtm_send_message(channel, reply)

    else:
        message.send(reply)


@respond_to(r'\A<mailto:.*@.* .*\Z')
def user_ragistration(message):
    if not _is_dm(message):
        message.reply("DMで教えてください")

    user_id = message.user['id']
    message_str = re.split(r'\s', message.body['text'], 2)
    um = UserManagement()
    reply =  um.user_ragistration(user_id, message_str[0], message_str[1])
    um.release()
    message.send(reply)


def _is_dm(message):
    return 'is_im' in message.channel._body and message.channel._body['is_im']
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



@respond_to(r'\A出勤\Z')
def start_registration(message):

    user_id = message.user['id']
    um = UserManagement()
    reply = um.work(user_id, "start")
    um.release()
    message.reply(reply)

@respond_to(r'\A退勤\Z')
def end_registration(message):

    user_id = message.user['id']
    um = UserManagement()
    reply = um.work(user_id, "end")
    um.release()
    message.reply(reply)

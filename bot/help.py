# Standard library imports.
from logging import getLogger


# Related third party imports.
from slackbot.bot import default_reply

# Local application/library specific imports.

logger = getLogger(__name__)


@default_reply
def help(message):
     message.send("使い方(TBD)")
from slackbot.bot import Bot

import logging
from logging import getLogger, INFO, DEBUG, Formatter, basicConfig


formatter = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
logging.basicConfig(level=DEBUG, filename='log/logger.log', format=formatter)

logger = getLogger(__name__)


def main():
    bot = Bot()
    bot.run()

if __name__ == "__main__":
    print('start jobcan-auto')
    main()

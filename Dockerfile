FROM python:3.7

ENV SLACKBOT_API_TOKEN=""
VOLUME /app/db

RUN set -x && \
  curl https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
  echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
  apt update && \
  apt install -y google-chrome-stable && \
  CHROME_VERSION=$(apt policy google-chrome-stable | grep Installed | awk '{print $2}' | awk -F . '{print $1"."$2}') && \
  apt install -y fonts-ipafont fonts-ipaexfont && \
  fc-cache -fv && \
  pip install selenium && \
  pip install chromedriver-binary~=$CHROME_VERSION && \
  pip install python-dotenv && \
  pip install slackbot && \
  apt clean && \
  rm -rf /var/lib/apt/lists/*

COPY app /app

WORKDIR /app
CMD  ["python", "jobcan-bot.py"]

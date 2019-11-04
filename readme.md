# Jobcanの出退勤を自動化するなにか

## 動作確認環境
 - Windows10 + Python3.7(Anaconda)
 - ubuntu 16.04(server) + Python3.7(Anaconda)

## 準備
- Dockerのインストール
- Slackbotをワークスペースにインストール  
分からない人は[筆者ブログ](https://ma-hiro.com/python%e3%81%a7slack-bot%e3%82%92%e4%bd%9c%e3%82%8b/)でも参考にしてください  
APIトークンを控えておくこと

## docker buildする
以下コマンド例
~~~
docker build -t jobcan-bot .
~~~

## 実行する(docker run)
- ポイント
  - API TOKENを環境変数にセットする
  - DB用のディレクトリはマウントしておく

以下コマンド例
~~~
docker run -d -e -v /storage/docker/jobcan/db:/app/db SLACKBOT_API_TOKEN="xoxb-xxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx" jobcan-bot
~~~

<details>
<summary>仮想環境を使わない場合</summary>

### インストールするもの
- python3.7
  - Anaconda入れました。インストール方法は割愛  
    ubuntuにAnacondaインストールした時のパス設定とかはうまいことやること
  - Selenium
  - 以下コマンドでインストール
    ~~~
    pip install selenium
    ~~~
- google chrome  
  Windowsのインストール手順は割愛  
  ubuntuは以下手順にてインストール(rootでやってます)
   ~~~bash
   curl https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
   echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list
   apt update
   apt install google-chrome-stable
   ~~~
- Chrome driver  
  [ここ](http://chromedriver.chromium.org/downloads)から使用しているChromeのバージョンにあったものをインストール  
  pipでもインストール可能な為、作者は以下コマンドからインストールしてます
  ~~~
  pip install chromedriver-binary==76.0.3809.68.0
  ~~~
- Slackbot  
  Slack連携する場合に必要。以下コマンドでインストール
  ~~~
  pip install slackbot
  ~~~

### 事前準備
- jobcanユーザ情報(jobcan_settings.py)  
  ログインに必要なメールアドレス及びパスワードを設定する
  Slack連携時は不要
- SlackAppの情報(slackbot_settings.py)  
  Slackbot用のAPIトークンを設定する([https://api.slack.com/apps](https://api.slack.com/apps))


### 起動コマンド
~~~
nohup python jobcan-auto.py &
~~~
</details>

</details>

### 使い方(Slackbot)
  1. 登録  
    1. botに対してDMで「登録」と送信します。botユーザがいるチャンネルの場合はメンションを付けて「登録」と送信します。  
    ![registration_1](https://user-images.githubusercontent.com/51410784/67299065-22ed0880-f527-11e9-8de8-226f620f2386.png)  
    2. DMで返信が来るのでメールアドレスとパスワードをスペースで区切って送信します  
    ![registration_2](https://user-images.githubusercontent.com/51410784/67299312-74959300-f527-11e9-86d2-03b0f9b91362.png)
  1. 出勤時  
  botに対してDMまたはメンションを付けて「出勤」と送信します  
  ![image](https://user-images.githubusercontent.com/51410784/67622733-fa7f4a00-f857-11e9-8bfa-3d457174d561.png)
  1. 退勤時  
  botに対してDMまたはメンションを付けて「退勤」と送信します  
  ![image](https://user-images.githubusercontent.com/51410784/67622743-14209180-f858-11e9-9166-2a18e18c5f50.png)

### 使い方(コマンド実行)

  1. 出勤時  
    python jobcan.py start
  1. 退勤時  
    python jobcan.py end

# Jobcanの出退勤を自動化するなにか

## 動作確認環境
 - Windows10 + Python3.7(Anaconda)
 - ubuntu 16.04(server) + Python3.7(Anaconda)

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

- jobcanユーザ情報(jobcan_settings.py)  
ログインに必要なメールアドレス及びパスワードを設定する

## 使い方
### 出勤時
~~~
python jobcan.py start
~~~
### 退勤時
~~~
python jobcan.py end
~~~
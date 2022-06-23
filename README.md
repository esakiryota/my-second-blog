# my-second-blog
deploy用はryota

# README
```
pip install djangorestframework
pip install django-filter
```

## 環境構築

```
$ python3 -m venv myvenv
$ source myvenv/bin/activate
$ python manage.py runserver
```

## AWSでの設定
インスタンスを停止→再起動する時、
```
$ systemctl start mariadb
```
を行い、mariadbを再起動させる必要がある。


## redis server 起動
```
$ docker run -p 6379:6379 -d redis:5
```

# deploy手順（随時更新）

1. AWSのEC2でubuntuサーバーを立ち上げ
2. 以下のコマンドを入力し、サーバーシステムの準備
```
$ sudo apt update
$ sudo apt install nginx supervisor
```

3. supervisorの設定ファイルを /etc/supervisor/conf.d/ の中に作成。以下の内容を記述
```
[fcgi-program:asgi]
# TCP socket used by Nginx backend upstream
socket=tcp://localhost:8000

# Directory where your site's project files are located
directory=/myproject/my-second-blog

# Each process needs to have a separate socket file, so we use process_num
# Make sure to update "mysite.asgi" to match your project name
command=daphne -u /run/daphne/daphne%(process_num)d.sock --fd 0 --access-log - --proxy-headers mysite.asgi:application

# Number of processes to startup, roughly the number of CPUs you have
numprocs=4

# Give each process a unique name so they can be told apart
process_name=asgi%(process_num)d

# Automatically start and recover processes
autostart=true
autorestart=true

# Choose where you want your log to go
stdout_logfile=/log/asgi.log
redirect_stderr=true
```
4. gitでプロジェクトをクローンする
```
$ sudo mkdir /myproject
$ cd /myproject
$ sudo git clone https://github.com/esakiryota/my-second-blog.git
$ sudo git pull origin ryota
```

5. 以下のコマンドを作成し、supervisorの実行コマンドのログファイルを作成
```
$ sudo mkdir /log
$ cd /log
$ sudo touch asgi.log
```

6. supervisorで実行するのdaphneのディレクトリを作成し、権限を変更
```
$ sudo mkdir /run/daphne/
$ sudo chown <user>.<group> /run/daphne/
```

7. daphneフォルダーを永続化
```
$ d /run/daphne 0755 <user> <group>
```

8. supervisorを更新
```
$ sudo supervisorctl reread
$ sudo supervisorctl update
```

9. nginxの設定ファイルを編集。daphneプロジェクトに接続するようにリバースプロキシ設定
```
$ cd /etc/nginx/sites-available
$ sudo vi default
```
以下のように編集
```
upstream channels-backend {
    server localhost:8000;
}
server {
    location / {
        try_files $uri @proxy_to_app;
    }
    location @proxy_to_app {
        proxy_pass http://channels-backend;

        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        proxy_redirect off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $server_name;
    }
}
```
その後、更新
```
$ sudo service nginx reload
```

10. redis-serverをインストール
```
$ sudo apt install redis-server
```

11. プロジェクトの権限を変更
```
$ cd /myproject
$ sudo chown -R <user>:<group> my-second-blog/
```

12. ipadressに接続し、表示を確認




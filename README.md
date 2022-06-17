# my-second-blog
url: https://esakiryota.pythonanywhere.com
loginId: esakiryota
loginPassword: esaki1217

ryota branchはpythonanywhere用
master branchはheroku用


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

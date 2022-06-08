# my-second-blog
url: https://esakiryota.pythonanywhere.com
loginId: esakiryota
loginPassword: esaki1217

ryota branchはpythonanywhere用
master branchはheroku用


# README

## 環境構築

```
$ python3 -m venv myvenv
$ source myvenv/bin/activate
$ python manage.py runserver
```

## redis server 起動
```
$ docker run -p 6379:6379 -d redis:5
```

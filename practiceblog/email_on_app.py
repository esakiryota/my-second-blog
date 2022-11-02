from django.core.mail import send_mail


class Email():
    def __init__(self) -> None:
        pass

    def send_email(self, name, address, title, content):
        send_mail(
            "ボードミート管理",
            "メールを受け付けました。貴重なご意見ありがとうございます。",
            address,
            [address],
            fail_silently=False,
        )
    
    def send_email_admin(self, name, address, title, content):
        send_mail(
            title,
            content,
            "bm_admin@board-meet.com",
            ["bm_admin@board-meet.com"],
            fail_silently=False,
        )



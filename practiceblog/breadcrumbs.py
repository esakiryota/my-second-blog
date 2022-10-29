

class BreadCrumbs():
    bread_crumbs = {
        "login" : "<a href='/'>HOME</a><span>＞</span><div>ログイン</div>",
        "logout" : "<a href='/'>HOME</a><span>＞</span><div>ログアウト</div>",
        "explanation" : "<a href='/'>HOME</a><span>＞</span><div>サイト概要</div>",
        "register" : "<a href='/'>HOME</a><span>＞</span><div>アカウント作成</div>",
        "profile" : "<a href='/'>HOME</a><span>＞</span><div>プロフィール</div>",
        "board_list" : "<a href='/'>HOME</a><span>＞</span><div>ボードリスト</div>",
        "user_list" : "<a href='/'>HOME</a><span>＞</span><div>ユーザーリスト</div>",
    }
    def breadCrumbsView(self, request):
        param = self.getCurrentUrl(request)
        bread_crumbs_html = self.bread_crumbs[param]
        return bread_crumbs_html
    
    def getCurrentUrl(self, request):
        url = request.get_full_path()
        url_list = url.split('/')
        main_param = url_list[0]
        return  main_param

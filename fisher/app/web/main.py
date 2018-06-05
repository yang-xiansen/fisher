from flask import render_template
from flask_login import current_user, login_required

from app.models.gift import Gift
from app.view_models.book import BookViewModel
from app.web import web



@web.route('/')
def index():
    """
            首页视图函数
            这里使用了缓存，注意缓存必须是贴近index函数的
        """
    recent_gifts = Gift.recent()
    books = [BookViewModel(gift.book) for gift in recent_gifts]
    return render_template('index.html', recent=books)



@web.route('/personal')
@login_required
def personal_center():
    return render_template('personal.html', user=current_user.summary)

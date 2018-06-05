from flask import Blueprint, render_template

#蓝图 blueprint
web = Blueprint('web', __name__, template_folder='templates')


#自定义404
@web.app_errorhandler(404)
def not_found(e):
    #AOP思想（切片思想）
    return render_template('404.html'), 404   #链接web/auth.py中的first_or_404

#注册
from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
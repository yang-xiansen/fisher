from flask import current_app, flash, redirect, url_for, render_template
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.gift import MyGifts
from app.view_models.trade import MyTrades
from . import web
from flask_login import login_required, current_user


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required #检验用户是否登陆
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        #事务
        #rollback
        # try:
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id #current_user 与user中的模型get_user方法相对
            # current_user.beans +=0.5  #鱼豆
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
        #     db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:

        flash('这本书已存在你的赠送清单，或者你的心愿清单，请不要重复添加')
    # ajax技术不刷新页面返回数据  或者将整个页面缓存起来，从而提高服务器性能
    return redirect(url_for('web.book_detail', isbn=isbn))

@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):  #撤销礼物
    gift = Gift.query.filter_by(id=gid, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id = gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先到鱼漂中完成该交易')
    with db.auto_commit():
        current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
        gift.delete()
    return redirect(url_for('web.my_gifts'))




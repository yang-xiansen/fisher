from flask import jsonify, request, current_app, url_for, render_template, flash
from flask_login import current_user
from app.forms.books import SearchForm
import json
from app.libs.helper import is_isbn_or_key
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.yushu_book import YuShuBook
from app.view_models.book import BookViewModel, BookCollection, _BookViewModel
from app.view_models.trade import TradeInfo
from . import web


@web.route('/book/search')
def search():
    """
        q :普通关键字 isbn
        page
        ?q=金庸&page=1
    """

    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        yushu_book = YuShuBook()
        isbn_or_key = is_isbn_or_key(q)

        if isbn_or_key == 'isbn':
            yushu_book.search_by_isbn(q)
            # result = yushu_book.search_by_isbn(q)
            # result = _BookViewModel.package_single(result, q)
        else:
            yushu_book.search_by_keyword(q, page)
            # result = yushu_book.search_by_keyword(q, page)
            # result = _BookViewModel.package_collection(result, q)
        # return jsonify(result)
        books.fill(yushu_book, q)
        # return json.dumps(books, default=lambda o:o.__dict__)

    else:
        flash('搜索的关键字不符合要求，请重新输入关键字')
        # return jsonify(form.errors)\
    return render_template('search_result.html', books=books)


@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False


    #取书籍的详情页面
    yushu_book = YuShuBook()
    yushu_book.search_by_isbn(isbn)
    book = BookViewModel(yushu_book.first)

    if current_user.is_authenticated:
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn, launched=False):
            has_in_gifts = True

        if Wish.query.filter_by(uid=current_user.id, isbn=isbn, launched=False):
            has_in_wishes = True

    #查出所有要赠送书的名单和索要书的名单
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    trade_gifts_models = TradeInfo(trade_gifts)
    trade_wishes_models = TradeInfo(trade_wishes)



#mvc    m是models    v是templates视图层   c是视图函数
    return render_template('book_detail.html', book=book, wishes=trade_wishes_models,
                           gifts=trade_gifts_models, has_in_gifts=has_in_gifts, has_in_wishes=has_in_wishes)



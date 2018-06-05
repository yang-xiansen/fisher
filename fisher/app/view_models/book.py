#view_models  东西的详情页面
#显示书籍的详情页面

class BookViewModel:
    def __init__(self, book):
        self.title = book['title']
        self.publisher = book['publisher']
        self.author = '，'.join(book['author'])
        self.price = book['price']
        self.pages = book['pages']
        self.summary = book['summary']
        self.image = book['image']
        self.isbn = book['isbn']
        self.pubdate = book['pubdate']
        self.binding = book['binding']

    @property #将方法变成属性
    def intro(self):
        intros = filter(lambda x:True if x else False, [self.author, self.publisher, self.price])
        return ' / '.join(intros)
        # if self.publisher:
        #     pass
        # if self.price:
        #     pass


class BookCollection:
    def __init__(self):
        self.total = 0
        self.books = []
        self.keyword = ''

    def fill(self, yushu_book, keyword):
        self.total = yushu_book.total
        self.books = [BookViewModel(book) for book in yushu_book.books]
        self.keyword = keyword







class _BookViewModel:
    @classmethod
    def package_single(cls, data, keyword):
        returned = {
            'book': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = 1
            returned['book'] = [cls.__cut_book_data(data)]
        return returned

    @classmethod
    def package_collection(cls, data, keyword):
        returned = {
            'book': [],
            'total': 0,
            'keyword': keyword
        }
        if data:
            returned['total'] = data['total']
            returned['book'] = [cls.__cut_book_data(book) for book in data['book']]
        return returned

    @classmethod
    def __cut_book_data(cls, data):
        book = {
            'title': data['title'],
            'publisher': data['publisher'],
            'pages': data['pages'] or '',
            'author': '，'.join(data['author']),
            'price': data['price'],
            'summary': data['summary'] or '',
            'image': data['image']
        }
        return book

    @classmethod
    def __cut_books_data(cls, data):
        books = []
        for book in books:
            r = {
                'title': data['title'],
                'publisher': data['publisher'],
                'pages': data['pages'],
                'author': '，'.join(data['author']),
                'price': data['price'],
                'summary': data['summary'],
                'image': data['image']
            }
            books.append(r)
        return books
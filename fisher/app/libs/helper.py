def is_isbn_or_key(word):

    #判断搜索是关键字还是isbn
    # isbn 13 13个数字组成
    # isbn 10 10个数字和一些 '-'组成
    isbn_or_key = 'key'
    if len(word) == 13 and word.isdigit():
        isbn_or_key = 'isbn'
    short_word = word.replace('-', '')
    if '-' in word and len(short_word) == 10 and short_word.isdigit():
        isbn_or_key = 'isbn'
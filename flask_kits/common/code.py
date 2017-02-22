# -*- coding: utf-8 -*-

ENCODINGS = ['utf8', 'gbk']


def decode_statement(statement, encodings):
    if isinstance(statement, unicode):
        return statement
    for encoding in encodings:
        try:
            return statement.decode(encoding)
        except UnicodeDecodeError:
            pass


def get_initial_letters(statement):
    statement = decode_statement(statement, ENCODINGS)
    if statement is None:
        return ''
    return ''.join(get_initial_letter(word) for word in statement)


def get_initial_letter(character):
    character = character.encode('gbk')
    try:
        ord(character)
        return character.lower()
    except Exception:
        # ignore exception
        asc = ord(character[0]) * 256 + ord(character[1]) - 65536
        if -20319 <= asc <= -20284:
            return 'a'
        if -20283 <= asc <= -19776:
            return 'b'
        if -19775 <= asc <= -19219:
            return 'c'
        if -19218 <= asc <= -18711:
            return 'd'
        if -18710 <= asc <= -18527:
            return 'e'
        if -18526 <= asc <= -18240:
            return 'f'
        if -18239 <= asc <= -17923:
            return 'g'
        if -17922 <= asc <= -17418:
            return 'h'
        if -17417 <= asc <= -16475:
            return 'j'
        if -16474 <= asc <= -16213:
            return 'k'
        if -16212 <= asc <= -15641:
            return 'l'
        if -15640 <= asc <= -15166:
            return 'm'
        if -15165 <= asc <= -14923:
            return 'n'
        if -14922 <= asc <= -14915:
            return 'o'
        if -14914 <= asc <= -14631:
            return 'p'
        if -14630 <= asc <= -14150:
            return 'q'
        if -14149 <= asc <= -14091:
            return 'r'
        if -14090 <= asc <= -13119:
            return 's'
        if -13118 <= asc <= -12839:
            return 't'
        if -12838 <= asc <= -12557:
            return 'w'
        if -12556 <= asc <= -11848:
            return 'x'
        if -11847 <= asc <= -11056:
            return 'y'
        if -11055 <= asc <= -10247:
            return 'z'
        return ''


if __name__ == "__main__":
    x = u'迦舒布鲁姆Ⅰ峰'
    print(get_initial_letters(x))

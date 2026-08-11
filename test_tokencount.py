import tokencount


def test_empty_text_is_zero():
    assert tokencount.estimate("") == 0

def test_short_words_are_one_token_each():
    assert tokencount.estimate("the cat sat") == 3

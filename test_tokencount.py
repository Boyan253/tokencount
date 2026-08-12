import tokencount


def test_empty_text_is_zero():
    assert tokencount.estimate("") == 0

def test_short_words_are_one_token_each():
    assert tokencount.estimate("the cat sat") == 3


def test_punctuation_counts():
    assert tokencount.estimate("hi!") == 2

def test_long_words_split_into_subwords():
    assert tokencount.estimate("internationalization") > 1

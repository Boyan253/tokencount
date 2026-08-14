import tokencount


def test_empty_text_is_zero():
    assert tokencount.estimate("") == 0

def test_short_words_are_one_token_each():
    assert tokencount.estimate("the cat sat") == 3


def test_punctuation_counts():
    assert tokencount.estimate("hi!") == 2

def test_long_words_split_into_subwords():
    assert tokencount.estimate("internationalization") > 1


def test_newlines_count_but_plain_spaces_do_not():
    assert tokencount.estimate("a b") == 2
    assert tokencount.estimate("a\nb") == tokencount.estimate("a b") + 1

def test_estimate_is_roughly_chars_over_four():
    text = "The quick brown fox jumps over the lazy dog. " * 20
    ratio = len(text) / tokencount.estimate(text)
    assert 3.0 < ratio < 6.0


def test_cost_maths():
    assert round(tokencount.cost(1_000_000, 3.0), 4) == 3.0
    assert round(tokencount.cost(500_000, 3.0), 4) == 1.5

def test_human_abbreviates():
    assert tokencount.human(1500) == "1.5k"
    assert tokencount.human(2_000_000) == "2.0M"
    assert tokencount.human(42) == "42"

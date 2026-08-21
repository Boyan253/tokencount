# tokencount

> Estimate LLM token counts and cost for files or stdin, offline, with no tokenizer download.

## Why

Before you paste a directory into a model you want to know: is this 8k tokens
or 800k, and what will it cost? Real tokenizers mean installing a package and
downloading vocabulary files. This is one stdlib file that gets you within a
few percent.

## Usage

```
python tokencount.py README.md
python tokencount.py src/*.py --price 3.00
cat prompt.txt | python tokencount.py
python tokencount.py docs/*.md --limit 100000     # exit 1 if over budget
```

## Output

```
    4.1k tokens      16.8k chars  src/app.py
    2.3k tokens       9.2k chars  src/utils.py
----------------------------------------
    6.4k tokens total
   0.0192 USD at $3.00 per million
```

## How the estimate works

Text is split into word, punctuation and whitespace pieces. Each punctuation
mark is one token, each newline is one, and a word costs roughly one token per
four characters — which is how byte-pair encoding behaves on ordinary prose and
code.

It is an **estimate**. Expect a few percent of error on English and code, more
on dense JSON, base64, or non-Latin scripts. Use it for budgeting and limits,
not billing reconciliation.

## Cost

`--price` is dollars per million input tokens; put your provider's number in.
`--limit` makes the tool exit 1 when a directory is bigger than the context you
were planning to use, which is handy in a script that assembles prompts.

## Tests

```
pip install pytest
pytest
```

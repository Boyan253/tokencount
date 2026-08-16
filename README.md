# tokencount

> Estimate LLM token counts and cost for files or stdin, offline, with no tokenizer download.

## Why

Before you paste a directory into a model you want to know: is this 8k tokens
or 800k, and what will it cost? Real tokenizers mean installing a package and
downloading vocabulary files. This is one stdlib file that gets you within a
few percent.

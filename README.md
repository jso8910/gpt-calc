A calculator generated with Chat GPT (`gpt.py`) and modified to the version in `calc.py`. The original version works but operates right-to-left and with no order of operations, functions, or irrational constants.

I added functional order of operations (other than the fact that power towers don't work because 2^2^2 is treated as (2^2)^2 rather than 2^(2^2) and I really can't be bothered to fix that because this doesn't matter. Just work out your power towers by hands)

I think GPT-3 did a very good job. Here is the prompt I gave it. GPT-3's responses are summaries of the response:

```
Me: Create a calculator in Python which supports Polish notation that is inputted using the input() function

GPT-3: Spits out code that only works with things like 2 3 + (so Reverse Polish notation and it might not even work for more complex examples)

Me: This doesn't work when the operator is between the two numbers. Make it work in that scenario

GPT-3: The code currently in `gpt.py`
```

`calc.py` is still based on the same fundamental theory as `gpt.py` but with modifications which allow order of operations to work.

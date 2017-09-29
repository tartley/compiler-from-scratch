Compile a toy language (see input.src) to Javascript.

```bash
USAGE: cat input.src | ./tokenize.py | ./parse.py | ./generate.py | node
```

Following along with Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
(paywalled) but translated into Python.

I also couldn't resist splitting up the three phases into stand-alone
scripts. This adds the slight complication of having to encode/decode
to JSON between each stage, which regrettably meant I couldn't see a neat
way to continue using namedtuples throughout, and had to substitute dicts.
But it has the payoff of being able to use the above pipeline, which is pretty
rad.


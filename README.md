Compile a toy language (see input.src) to Javascript.

```bash
USAGE: cat input.src | ./tokenize.py | ./parse.py | ./generate.py | node
```

Following along with Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
but translated into Python.

I also couldn't resist splitting up the separate phases into stand-alone
processes, just so I could create the above pipeline.


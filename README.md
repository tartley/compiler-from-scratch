Compile a toy language (see input.src) to Javascript.

```bash
USAGE: cat input.src | ./tokenize.py | ./parse.py | ./generate.py | node
```

Following along with Destroy All Software, s07 0101 A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch
(paywalled.) Being a bear of little brain, I can't just skim over material
like this, or else I'll forget it in three days. So I followed along, but
couldn't resist making a few changes along the way:

* Translated from Ruby to Python.
* I split the three phases into stand-alone scripts. This adds the slight
  complication of having to encode/decode to JSON between each stage, which
  regrettably meant I couldn't see a neat way to continue using namedtuples
  throughout, and had to substitute dicts in places. But it has the payoff of
  being able to use the above pipeline, which is pretty rad.
* The input source code can now contain more than one top-level parse node,
  allowing the input source to contain a sequence of function definitions
  and/or function calls. This means we no longer need the 'TEST' code injected
  at code generation time.

# Toy language

Let's start with the toy language with intend to compile:

```bash
$ cat input.src
def f(a, b)
    add(100, add(20, add(a, b)))
end

print(f(1, 2))
```

It includes:
* function definitions
* function calls
* integer literals,
* variable references.

It also makes use of two undefined functions 'add' and 'print'. We'll define
those later, built-in to the compilation process, as part of our toy language
runtime.

# Tokenize

This splits the source code above into a sequence of tokens. Each token
has a type and a value.

```bash
$ cat input.src | ./tokenize.py
[["def", "def"], ["identifier", "f"], ["oparen", "("], etc...
```

We can make this a bit easier to read with a '-h' (human readable) flag:

```bash
$ cat input.src | ./tokenize.py -h
[
    ["def", "def"],
    ["identifier", "f"],
    ["oparen", "("],
    ["identifier", "a"],
    ["comma", ","],
    ["identifier", "b"],
    ["cparen", ")"],
    ["identifier", "add"],
    ["oparen", "("],
    ["integer", "100"],
    etc...
```

In Gary's original, the output of the tokenizing step was a sequence of
objects that were passed, in-process, to the next step. I've tweaked this
so that the parsing runs as a parallel process, and so the tokenizer needs to
output a serialized version of those objects on stdout. Since the objects
in Python are namedtuples, and I serialized using JSON, these come out
as a series of lists. So each item in the above sequence has two fields,
representing a token's type and value.

Comparing this output to input.src, we can see the transformation that has been
done is straightforward.

# Parse

```bash
cat input.src | ./tokenize.py | ./parse.py 
[{"node_type": "def", "name": "f", "arg_names": ["a", "b"],
"body": {"node_type": "call", "name": "add", "arg_exprs": etc...
```

Once again, we can make this more human-readable with '-h':

```bash
$ cat input.src | ./tokenize.py | ./parse.py -h
[
    {
        "node_type": "def",
        "name": "f",
        "arg_names": [
            "a",
            "b"
        ],
        "body": {
            "node_type": "call",
            "name": "add",
            "arg_exprs": [
                {
                    "node_type": "int",
                    "value": 100
                },
                {
                    "node_type": "call",
                    "name": "add",
                    "arg_exprs": [
                        {
                            "node_type": "int",
                            "value": 20
                        },
etc..
```

The parsing has transformed the linear sequence of tokens into a tree of
*parse nodes*.


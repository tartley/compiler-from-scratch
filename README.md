Compile a toy language (See [input.src](./input.src) to Javascript.

```bash
USAGE: cat input.src | ./tokenize.py | ./parse.py | ./generate.py | node
```

Written using Python3.6, no other dependencis.

Following along with Destroy All Software, s07-e0101, A compiler from scratch.
https://www.destroyallsoftware.com/screencasts/catalog/a-compiler-from-scratch

The DAS content is paywalled, but excellent, I highly recommend it. This video,
for example goes way beyond what I'm about to describe here. The videos are
very short (usually closer to ten minutes) so are easily digestible, but are
dense, like pair programming with an expert, you learn a lot of incidentals
along the way, and they dive deep on well-chosen topics.

Being a bear of little brain, I can't just skim over material like this, or
else I'll forget it in three days. So I followed along, coding along with
Gary, but couldn't resist making a few changes along the way:

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

This repo was first presented to the [Python meetup in Rochester, MN](https://www.meetup.com/PyRochesterMN/).

# Toy language

Let's start with the toy language we intend to compile (See [input.src](./input.src)):

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

This splits the source code above into a sequence of tokens.
See [tokenize.py](./tokenize.py).

Each token has a type and a value.

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

The output of tokenizing is fed into the parser.
See [parse.py](./parse.py).

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
*parse nodes*. Each node has a 'node_type' (in Gary's original, this was
the class of the node object. To serialize these to JSON, I've added it
as an explicit field.). Each node type has its own set of additional fields.
For example, a function definition has:

    node_type: def
    name: <function name>
    arg_names: <list of arg names>
    body: some other node

Whereas an integer literal node has only:

    node_type: int
    value: <value of integer>

These nodes reference each other (eg. the body of a function definition), to
form a tree, representing the origininal input.src.

# Generation

The output of parsing is fed into the generator.
See [generate.py](./generate.py).

```bash
$ cat input.src | ./tokenize.py | ./parse.py | ./generate.py 
function add(x, y) { return x + y };
function print(x) { console.log(x) };
function f(a, b) { return add(100, add(20, add(a, b))) };
print(f(1, 2))
```

This generator produces Javascript, because that's easy to do and easy
to understand. But it's not a substantially different in principle for it to
output executable binaries instead.

Only the final two lines in the above output represent our input.src. The
first two lines are some 'runtime' support that our generator injects into the
output, to provide an implementation for functions 'add' and 'print'.
We do this because providing an 'add' function is easy, whereas implementing
an actual '+' operator in our toy language would be quite verbose, without
demonstrating anything new.

# Demonstration

Looking back at input.src:

```bash
$ cat input.src
def f(a, b)
    add(100, add(20, add(a, b)))
end

print(f(1, 2))
```

We can see the expected output is 123. We can test this, execute the Javascript
output by piping it to node:

```bash
$ cat input.src | ./tokenize.py | ./parse.py | ./generate.py | node
123
```


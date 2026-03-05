# Rules

All rules are prefixed `VIB`. Codes are assigned sequentially and never reused.

---

## `VIB001` — thursday-energy

**Severity:** warning

Thursdays occupy a liminal position in the work week — close enough to Friday to generate excitement, far enough from Monday to have accumulated significant technical debt in the developer's psyche. Functions written on Thursdays tend toward overengineering, premature abstraction, and a particular kind of ambition that the coming weekend will absolutely not resolve. This rule flags functions exceeding 20 lines authored on a Thursday, as identified by `git blame` or, when unavailable, the system clock at lint time.

```python
# Bad - authored on a Thursday, 27 lines long
def parse_user_preferences(input_data):
    # ... 27 lines of thursday ambition
    pass

# Good - same function, written on a Wednesday
def parse_user_preferences(input_data):
    # ... 27 lines, wednesday energy is stable and does not overreach
    pass
```

```
VIB001 thursday energy detected: 'parse_user_preferences' is 27 lines of pure thursday hubris. we felt it. the diff felt it.
```

---

## `VIB002` — todo-shame

**Severity:** warning

A `TODO` is a dream with a comment attached and no follow-through. A `FIXME` is a bug that developed self-awareness and still didn't get fixed. This rule flags both, because acknowledging a problem and solving it are not the same thing, and the diff doesn't care which one you did.

```python
# Bad
x = compute()  # TODO: handle edge case
y = broken()   # FIXME: this crashes on empty input

# Good
x = compute_with_edge_case_handled()
y = fixed()
```

```
VIB002 todo shame: this TODO has survived more sprints than some of your teammates
VIB002 todo shame: FIXME: acknowledged, unaddressed, unforgiven, and now publicly humiliated
```

---

## `VIB013` — god-variable

**Severity:** warning

Variables named `data`, `result`, `info`, `stuff`, `thing`, or `obj` describe their type, not their purpose. They are the naming equivalent of labeling a box "box". Every codebase has one. Every developer regrets it.

```python
# Bad
data = fetch_user_records()
result = transform(data)

# Good
user_records = fetch_user_records()
transformed_records = transform(user_records)
```

```
VIB013 naming crime: `data` holds everything and describes absolutely nothing. a true void.
```

---

## `VIB014` — single-letter

**Severity:** warning

Single-letter variable names outside of loops and comprehensions carry no semantic information. `i` in a `for` loop is idiomatic. `i` as a module-level assignment is a mystery that only you can solve and you are not here to solve it.

```python
# Bad
n = len(users)
x = get_config()

# Good — loop variables are fine
for i, user in enumerate(users):
    ...
```

```
VIB014 naming crime: `n` is one character, zero context, and infinite future confusion.
```

---

## `VIB015` — temp-variable

**Severity:** warning

Variables named `temp`, `tmp`, `temp2`, etc. were supposed to be temporary. They never are. They outlive the sprint they were born in, the developer who wrote them, and sometimes the company. This rule flags assignments where `temp` or `tmp` appears in the variable name.

```python
# Bad
temp = process(data)
tmp_result = calculate()

# Good
intermediate_value = process(data)
```

```
VIB015 naming crime: `temp` was supposed to be temporary. it has now outlived the sprint it was born in.
```

---

## `VIB016` — new-prefix

**Severity:** warning

`new_x` implies there is an `old_x` nearby. If there isn't, you have a poorly named variable. If there is, you have a refactor that didn't finish. Either way, `new_` is a timestamp masquerading as a name, and timestamps are not names.

```python
# Bad
new_user = create_user(form)
new_config = load_config()

# Good
created_user = create_user(form)
loaded_config = load_config()
```

```
VIB016 naming crime: `new_user` implies there's an `old_` version lurking nearby. there is, isn't there.
```

---

## `VIB017` — copy-suffix

**Severity:** warning

Suffixing `_copy`, `_2`, `_3`, etc. onto a variable name is version control implemented in identifiers. That is what git is for. This is not a naming strategy. It is a surrender.

```python
# Bad
user_copy = copy(user)
config_2 = updated_config()

# Good
archived_user = copy(user)
updated_config = load_updated_config()
```

```
VIB017 naming crime: `config_2` tells you its history, not its purpose. those are not the same thing.
```

---

## `VIB018` — final-variable

**Severity:** warning

Nothing in code is actually final. Variables named `final_x` become `final_v2_x` in the next PR, `final_actual_x` in the one after that, and a cautionary tale in the one after that. `final` is not a description. It is a wish.

```python
# Bad
final_report = generate_report()
final_result = compute()

# Good
report = generate_report()
```

```
VIB018 naming crime: `final_report` — the audacity of `final` in a variable name. the hubris. the nerve.
```

---

## `VIB019` — flag-variable

**Severity:** warning

A variable called `flag` is a boolean that looked at meaning and said "not my department". `is_active`, `should_retry`, `has_errors` are booleans with opinions. `flag` is a boolean with nothing to say for itself.

```python
# Bad
flag = check_status()
if flag:
    ...

# Good
is_ready = check_status()
if is_ready:
    ...
```

```
VIB019 naming crime: `flag` is the least informative boolean name in the entire english language.
```

---

## `VIB020` — vague-class

**Severity:** warning

Classes with `Manager` in the name are classes with identity issues. They manage something. Nobody knows what. Not even `Manager`. `Manager` is a title given to a class when no one could agree on what the class actually does, so they gave up and called it a manager.

```python
# Bad
class UserManager:
    ...

# Good
class UserRegistration:
    ...
```

```
VIB020 naming crime: `UserManager` manages something. nobody knows what. not even `UserManager`.
```

---

## `VIB030` — too-many-args

**Severity:** warning

A function that takes more than 5 arguments has stopped being a function and started being a form. The caller must remember six things, in the right order, with the right names. That information wants to live in a dataclass. It is begging you. Listen to it.

```python
# Bad
def create_user(name, email, age, role, is_active, plan, referral_code):
    ...

# Good
def create_user(user_data: UserData):
    ...
```

```
VIB030 structure: 'create_user' takes 7 arguments. this is not a function, this is a hostage situation.
```

---

## `VIB031` — deep-nesting

**Severity:** warning

Code nested more than 4 levels deep is code that has run out of ideas. Every additional level of indentation is a decision that could have been a function, a guard clause, or a different data structure. The indentation is screaming what the variable names won't say. Listen to the indentation.

```python
# Bad
def process(items):
    if items:
        for item in items:
            if item.active:
                for sub in item.children:
                    if sub.valid:  # 5 levels deep
                        handle(sub)

# Good
def process(items):
    active = [i for i in items if i.active]
    for item in active:
        _process_children(item)
```

```
VIB031 structure: depth 5. extract a function. any function. i am begging you.
```

---

## `VIB032` — too-many-returns

**Severity:** warning

A function with more than 3 return statements has not decided what it is yet. Return statements are exits, and a function with four exits has four different opinions about its own purpose. The only thing this function is committed to is leaving.

```python
# Bad
def classify(x):
    if x < 0: return "negative"
    if x == 0: return "zero"
    if x < 10: return "small"
    return "large"

# Good
_BUCKETS = [(-float("inf"), 0, "negative"), (0, 1, "zero"), (1, 10, "small")]
def classify(x):
    for lo, hi, label in _BUCKETS:
        if lo <= x < hi:
            return label
    return "large"
```

```
VIB032 structure: 'classify' — 4 ways out. no clear way in. iconic, but not in a good way.
```

---

## `VIB033` — bare-except

**Severity:** warning

`except:` with no exception type catches everything: `ValueError`, `KeyboardInterrupt`, `SystemExit`, and the thing that broke production last Tuesday. A bare `except` is not error handling. It is a cope mechanism with a colon. Name the exception you expect, or accept that you are hiding bugs you haven't met yet.

```python
# Bad
try:
    connect()
except:
    retry()

# Good
try:
    connect()
except ConnectionError:
    retry()
```

```
VIB033 structure: a bare `except` catches `KeyboardInterrupt`. sit with that. really sit with it.
```

---

## `VIB034` — empty-except

**Severity:** warning

An `except` block containing only `pass` is not error handling. It is a signed confession that you know something can go wrong and have chosen to do nothing about it. You caught the exception. You looked it in the eyes. You said `pass`. The exception deserved better. Your users deserved better.

```python
# Bad
try:
    load_config()
except FileNotFoundError:
    pass

# Good
try:
    load_config()
except FileNotFoundError:
    load_defaults()
```

```
VIB034 structure: `except: pass` — the code equivalent of unplugging the smoke alarm.
```

---

## `VIB081` — equals-true

**Severity:** warning

`if x == True` is a tautology wearing a trench coat. You already have a boolean. `if x` was right there. The question is why you walked past it.

```python
# Bad
if is_active == True:
    ...

# Good
if is_active:
    ...
```

```
VIB081 boolean chaos: `== True`. the boolean was right there. you walked past it. why.
```

---

## `VIB082` — equals-false

**Severity:** warning

`if x == False` is `not x` with extra steps, less confidence, and worse vibes. The `not` keyword has been here since 1991. It has been waiting for you this entire time.

```python
# Bad
if is_active == False:
    ...

# Good
if not is_active:
    ...
```

```
VIB082 boolean chaos: Python has a `not` keyword. it's been here since 1991. i'm begging you to use it.
```

---

## `VIB083` — equals-none

**Severity:** warning

`None` is a singleton. You identity-check singletons. This is not a debate. `is None` has been here the whole time — waiting, patient, judging. PEP 8 asked nicely. We are not asking.

```python
# Bad
if result == None:
    ...

# Good
if result is None:
    ...
```

```
VIB083 boolean chaos: `is None` has been here the whole time. waiting. patient. judging.
```

---

## `VIB084` — not-equals

**Severity:** warning

`not x == y` is `x != y` with passive-aggressive energy and worse readability. The `!=` operator is one character. It is on your keyboard right now. There is no excuse.

```python
# Bad
if not user == admin:
    ...

# Good
if user != admin:
    ...
```

```
VIB084 boolean chaos: `not x == y` is `x != y` with passive-aggressive energy and worse readability.
```

---

## `VIB003` — except-exception-cowardice

**Severity:** warning

`except Exception` is a typed version of a bare `except` that still catches everything worth catching. You typed a word. You get no credit for it. The exception you actually expect has a name. Use it.

```python
# Bad
try:
    connect()
except Exception:
    retry()

# Good
try:
    connect()
except ConnectionError:
    retry()
```

```
VIB003 exception: `except Exception` is a coward's `except:` wearing a tie.
```

---

## `VIB006` — generic-raise

**Severity:** warning

`raise Exception("something went wrong")` is the error message equivalent of naming a file `file.txt`. Your callers can't catch it specifically. Your logs can't filter it. A specific exception type costs one word and earns infinite goodwill.

```python
# Bad
raise Exception("something went wrong")

# Good
raise ValueError("expected a positive integer, got -1")
```

```
VIB006 exception: `raise Exception(...)` — so you know something went wrong but not what. bold.
```

---

## `VIB008` — print-left-behind

**Severity:** warning

A `print()` in committed code is a debugging session that survived the review. It is not logging. It is not telemetry. It is the ghost of a panic that never got cleaned up.

```python
# Bad
def process(data):
    print("got here")
    return transform(data)

# Good
def process(data):
    return transform(data)
```

```
VIB008 debug: `print()` in production code is a confession you didn't write tests.
```

---

## `VIB009` — breakpoint-left-behind

**Severity:** warning

`breakpoint()` committed to the codebase is a debugging session that made it to production. It will pause the process and wait for a human who is not coming.

```python
# Bad
def tricky_function():
    breakpoint()
    return result

# Good
def tricky_function():
    return result
```

```
VIB009 debug: `breakpoint()` committed to the codebase. you had one job.
```

---

## `VIB010` — pdb-set-trace

**Severity:** warning

`pdb.set_trace()` is the pre-`breakpoint()` way to halt production. Both are equally inexcusable. This one just has more nostalgia attached to it.

```python
# Bad
import pdb
pdb.set_trace()

# Good
# nothing. the debugger should not be in the code.
```

```
VIB010 debug: `pdb.set_trace()` committed. the 90s called and they want their debugger back.
```

---

## `VIB011` — import-pdb

**Severity:** warning

Importing `pdb` is evidence that a debugging session happened and nobody cleaned up. The import serves no purpose in production code. Delete it.

```python
# Bad
import pdb
from pdb import set_trace

# Good
# no pdb in sight
```

```
VIB011 debug: you imported `pdb`. you forgot to remove it. these two facts are related.
```

---

## `VIB021` — commented-code-graveyard

**Severity:** warning

Three or more consecutive lines that look like commented-out code are a code graveyard. Git exists for this. Branches exist for this. A comment block is not version control.

```python
# Bad
# x = old_value
# y = compute_old(x)
# z = transform(x, y)

# Good
# (just delete the old code; git has it)
```

```
VIB021 comment: git exists. use it. delete the corpse.
```

---

## `VIB022` — type-ignore-no-explanation

**Severity:** warning

A `# type: ignore` without a following comment is a suppression without an explanation. You told mypy to look away. At least say why.

```python
# Bad
x = bad_function()  # type: ignore

# Good
x = bad_function()  # type: ignore[assignment]  # returns Any due to dynamic dispatch
```

```
VIB022 comment: silent type-ignore with no explanation is a lie you're asking mypy to sign off on.
```

---

## `VIB023` — noqa-no-code

**Severity:** warning

`# noqa` with no error code suppresses every linter check on the line. Name what you're suppressing or explain why the violation is acceptable.

```python
# Bad
very_long_function_call(with_many_arguments, that_exceed_line_length)  # noqa

# Good
very_long_function_call(with_many_arguments, that_exceed_line_length)  # noqa: E501
```

```
VIB023 comment: bare noqa suppresses everything. specify what you're ignoring or fix it.
```

---

## `VIB024` — todo-named

**Severity:** warning

A `TODO(name)` assigns work to a person in a comment. That person has not done it. The comment remains. The work remains. This is not a ticket system.

```python
# Bad
# TODO(alice): fix edge case handling

# Good
# TODO: fix edge case handling — tracked in GH-1234
```

```
VIB024 comment: TODO assigned to alice. has alice seen this? has alice done anything about it? no.
```

---

## `VIB026` — hack-comment

**Severity:** warning

A `# hack` comment is a bug with a disclaimer attached. You knew it was wrong when you wrote it. You know it now. The comment has not made it better.

```python
# Bad
# hack: multiply by 2 to compensate for the off-by-one somewhere upstream
result = value * 2

# Good
# compensate for upstream doubling in legacy_processor (see GH-42)
result = value * 2
```

```
VIB026 comment: a hack-tagged comment is a bug with a disclaimer attached.
```

---

## `VIB027` — do-not-touch

**Severity:** warning

`# do not touch` is a request made by someone who understood the code and has since left. Anything that cannot be touched cannot be maintained. If you're afraid of it, rewrite it.

```python
# Bad
# DO NOT TOUCH - things break if you change this
_magic_constant = 42

# Good
# this value is derived from the legacy batch size (see docs/batch_sizing.md)
_magic_constant = 42
```

```
VIB027 comment: the 'do not touch' comment means code you're afraid of — code you need to delete or rewrite.
```

---

## `VIB028` — this-is-fine

**Severity:** warning

`# this is fine` is the comment of someone watching their code on fire and choosing not to act. It is not documentation. It is a coping mechanism.

```python
# Bad
except Exception:
    pass  # this is fine

# Good
except SpecificError:
    logger.warning("handled expected error", exc_info=True)
```

```
VIB028 comment: the 'this is fine' comment — the universal sign of someone watching things burn.
```

---

## `VIB029` — lol-wtf-comment

**Severity:** warning

`# lol` means you found something funny. `# wtf` means you found something alarming. Neither is an explanation. Write what you actually mean.

```python
# Bad
# lol
# wtf is this

# Good
# this returns a string in dev and an int in prod — see GH-99 for the fix
```

```
VIB029 comment: a lol-comment in your code means even you don't take it seriously.
```

---

## `VIB048` — star-import

**Severity:** warning

`from x import *` brings every name from `x` into your namespace and documents none of them. Six months from now nobody will know where `parse_config` came from. Import what you need by name.

```python
# Bad
from utils import *

# Good
from utils import parse_config, validate_schema
```

```
VIB048 import: `import *` pollutes the namespace with everything and documents nothing.
```

---

## `VIB051` — import-in-function

**Severity:** warning

An import inside a function is a top-level import that couldn't commit. It hides dependencies, adds overhead on every call, and confuses readers expecting to find imports at the top.

```python
# Bad
def get_config():
    import json
    return json.loads(raw)

# Good
import json

def get_config():
    return json.loads(raw)
```

```
VIB051 import: importing inside a function delays the problem, it doesn't solve it.
```

---

## `VIB053` — explicit-return-none

**Severity:** warning

`return None` at the end of a function is redundant. Python already returns `None` when a function ends without a value. A bare `return` is cleaner. Silence is also fine.

```python
# Bad
def send_email(address):
    deliver(address)
    return None

# Good
def send_email(address):
    deliver(address)
```

```
VIB053 return: `return None` is the statement of a function that doesn't know how to end gracefully.
```

---

## `VIB054` — assign-then-return

**Severity:** warning

Assigning a variable only to return it on the next line adds nothing. The variable had a zero-line lifespan. Return the expression directly.

```python
# Bad
def get_total(items):
    result = sum(items)
    return result

# Good
def get_total(items):
    return sum(items)
```

```
VIB054 return: assign then immediately return — just return the expression. the variable adds nothing.
```

---

## `VIB055` — mutable-default-argument

**Severity:** warning

A mutable default argument (`[]`, `{}`, `set()`) is shared across every call to the function. Mutations in one call persist into the next. This is never what you wanted and always what you got.

```python
# Bad
def append_to(item, target=[]):
    target.append(item)
    return target

# Good
def append_to(item, target=None):
    if target is None:
        target = []
    target.append(item)
    return target
```

```
VIB055 return: mutable default argument — this list is shared across every call. that is never what you wanted.
```

---

## `VIB056` — shadow-builtin

**Severity:** warning

Naming a variable `list`, `dict`, `str`, `len`, or any other builtin replaces it in the local scope. Every subsequent call to `list()` now calls your variable. This is not clever. This is a trap.

```python
# Bad
list = [1, 2, 3]
len = 42

# Good
items = [1, 2, 3]
item_count = 42
```

```
VIB056 return: `list` is a builtin. you just overwrote it. your future `list()` calls thank you for the confusion.
```

---

## `VIB063` — multiple-inheritance

**Severity:** warning

Inheriting from 3 or more classes creates a method resolution order that even the developers of MRO would struggle to reason about. Each additional base class is another set of assumptions you now have to honor forever.

```python
# Bad
class Handler(BaseHandler, LogMixin, ValidationMixin, CacheMixin):
    ...

# Good
class Handler(BaseHandler):
    def __init__(self):
        self._log = Logger()
        self._validator = Validator()
```

```
VIB063 class: inheriting from 4 classes means 4 sets of assumptions you now have to honor. good luck.
```

---

## `VIB069` — test-no-assertion

**Severity:** warning

A test function with no assertions is a test that cannot fail. A test that cannot fail proves nothing. Green means nothing if the bar is on the floor.

```python
# Bad
def test_process():
    result = process(data)
    # forgot to assert

# Good
def test_process():
    result = process(data)
    assert result == expected
```

```
VIB069 test: `test_process` runs but never asserts anything. a test that can't fail can't prove anything.
```

---

## `VIB070` — test-named-test-it

**Severity:** warning

`test_it` is a test name that tests nothing but the reader's patience. What does it test? What is "it"? A test name should describe what it's testing and under what conditions.

```python
# Bad
def test_it():
    assert process(1) == 1

# Good
def test_process_returns_input_unchanged():
    assert process(1) == 1
```

```
VIB070 test: `test_it` — it. it what? what does it do? what did you test?
```

---

## `VIB071` — assert-true

**Severity:** warning

`assert True` is a test that proves `True` is `True`. It always passes. It means nothing. If you need to document that you've reached a code path, use a comment. This is not that.

```python
# Bad
def test_something():
    assert True

# Good
def test_something():
    assert compute() == expected_value
```

```
VIB071 test: `assert True` always passes. it proves nothing. it tests nothing. why is it here.
```

---

## `VIB072` — time-sleep-in-test

**Severity:** warning

`time.sleep()` in a test is a guess wearing a timer. You're hoping the thing you're waiting for will be done by then. It won't be. On CI. On the slowest day. Mock the time or mock the dependency.

```python
# Bad
def test_retry_logic():
    trigger_retry()
    time.sleep(2)
    assert result_received()

# Good
def test_retry_logic(mock_time):
    trigger_retry()
    mock_time.advance(2)
    assert result_received()
```

```
VIB072 test: found `time.sleep()` in a test. flaky tests have a sleep in them. this is a flaky test.
```

---

## `VIB074` — async-no-await

**Severity:** warning

An `async def` function that never uses `await` is a synchronous function with extra overhead and false advertising. Either add an `await` or remove the `async`.

```python
# Bad
async def get_name():
    return "alice"

# Good
def get_name():
    return "alice"
```

```
VIB074 async: async function with no `await` — this is a synchronous function wearing a costume.
```

---

## `VIB076` — asyncio-sleep-zero

**Severity:** warning

`asyncio.sleep(0)` yields control to the event loop. This is sometimes necessary but almost always undocumented. The next reader will not know why this sleep is here. Document the intent.

```python
# Bad
await asyncio.sleep(0)

# Good
await asyncio.sleep(0)  # yield to event loop to allow pending callbacks to run
```

```
VIB076 async: `asyncio.sleep(0)` is a yield to the event loop disguised as a nap.
```

---

## `VIB077` — string-concat-in-loop

**Severity:** warning

String `+=` inside a loop creates a new string on every iteration. For `n` iterations, you allocate `n` strings. `''.join(parts)` allocates one. Use `join`.

```python
# Bad
result = ""
for item in items:
    result += str(item)

# Good
result = "".join(str(item) for item in items)
```

```
VIB077 string: string `+=` in a loop is O(n²) performance and a betrayal of `str.join`.
```

---

## `VIB078` — percent-format

**Severity:** warning

`%` string formatting is Python 2 syntax that never quite went away. f-strings exist. They're faster, more readable, and don't require you to count `%s` placeholders.

```python
# Bad
msg = "hello %s, you have %d messages" % (name, count)

# Good
msg = f"hello {name}, you have {count} messages"
```

```
VIB078 string: `%` string formatting hasn't been recommended since Python 2. let go.
```

---

## `VIB079` — format-positional

**Severity:** warning

`.format()` with positional arguments requires you to count curly braces and match them to arguments by index. f-strings do the same thing with less ceremony and more readability.

```python
# Bad
msg = "hello {}, you have {} messages".format(name, count)

# Good
msg = f"hello {name}, you have {count} messages"
```

```
VIB079 string: `.format()` with positional args — an f-string would have been shorter and readable.
```

---

## `VIB089` — lambda-assigned

**Severity:** warning

A lambda assigned to a variable is an anonymous function that immediately got a name. At that point it's just a function. Use `def`. The lambda was not saving you anything.

```python
# Bad
double = lambda x: x * 2

# Good
def double(x):
    return x * 2
```

```
VIB089 misc: lambda assigned to a variable is a function that's embarrassed to be one. use `def`.
```

---

## `VIB090` — global-statement

**Severity:** warning

`global` is what you write when a function needs to modify state it shouldn't own. Functions take arguments and return values. That's the deal. Pass the state in, pass the result out.

```python
# Bad
count = 0

def increment():
    global count
    count += 1

# Good
def increment(count):
    return count + 1
```

```
VIB090 misc: `global` is a way of saying 'i couldn't figure out how to pass this as an argument'.
```

---

## `VIB091` — eval-used

**Severity:** warning

`eval()` executes arbitrary Python code from a string. If the string comes from user input, you have a code injection vulnerability. If it comes from your own code, you have an architecture problem.

```python
# Bad
result = eval(user_expression)

# Good
result = safe_eval(user_expression)  # use ast.literal_eval or a proper parser
```

```
VIB091 misc: `eval()` executes arbitrary code. if you know what you're doing, you don't need it.
```

---

## `VIB092` — exec-used

**Severity:** warning

`exec()` runs strings as Python code. Whatever you're doing with it, there is a safer, more explicit way to do it. Find that way.

```python
# Bad
exec(f"result_{name} = compute()")

# Good
results[name] = compute()
```

```
VIB092 misc: `exec()` runs strings as code. strings are not code. or they are, and that's the problem.
```

---

## `VIB094` — file-too-long

**Severity:** warning

A file with more than 500 lines has stopped being a module and started being a monolith. Cohesion has left the building. Split it.

```python
# Bad
# my_module.py — 800 lines of loosely related functions

# Good
# my_module/
#   core.py
#   utils.py
#   models.py
```

```
VIB094 misc: 623 lines in one file. that's not a module, that's a monolith with an extension.
```

---

## `VIB095` — nested-comprehension

**Severity:** warning

A comprehension nested 3 or more levels deep is something you can write and nobody else can read. Extract intermediate results into variables or loops. Be kind to the next person.

```python
# Bad
result = [x for xs in [y for y in [z for z in data]] for x in xs]

# Good
layers = [z for z in data]
flattened = [y for y in layers]
result = [x for x in flattened]
```

```
VIB095 misc: comprehension nested 3+ levels deep. you've made something unreadable and called it clever.
```

---

## `VIB096` — dict-constructor

**Severity:** warning

`dict(key=value)` is slower than `{"key": value}` and harder to read. The literal syntax was designed for exactly this. Use it.

```python
# Bad
config = dict(host="localhost", port=8080, debug=True)

# Good
config = {"host": "localhost", "port": 8080, "debug": True}
```

```
VIB096 misc: `dict(key=value)` — `{'key': value}` is shorter, faster, and obvious.
```

---

## `VIB097` — list-around-literal

**Severity:** warning

`list([1, 2, 3])` is `[1, 2, 3]` with extra steps. You already had a list. You made another list of the list. The brackets were doing fine on their own.

```python
# Bad
items = list([1, 2, 3])

# Good
items = [1, 2, 3]
```

```
VIB097 misc: `list([...])` — you already had a list. you made another list of the list.
```

---

## `VIB098` — assert-in-non-test

**Severity:** warning

`assert` statements are removed when Python is run with the `-O` flag. Your invariant just stopped existing in optimized production builds. Use an `if` with a proper exception.

```python
# Bad
assert user_id > 0, "user_id must be positive"

# Good
if user_id <= 0:
    raise ValueError(f"user_id must be positive, got {user_id}")
```

```
VIB098 misc: `assert` in production code is removed by `-O`. your invariant just stopped existing.
```

---

## `VIB099` — sys-exit

**Severity:** warning

`sys.exit()` in library code terminates the entire process. That's the caller's decision to make, not yours. Raise an exception and let the top-level handler decide how to die.

```python
# Bad
def validate(config):
    if not config:
        sys.exit(1)

# Good
def validate(config):
    if not config:
        raise ConfigError("config is empty")
```

```
VIB099 misc: `sys.exit()` in library code exits the entire process. that's the caller's call to make.
```


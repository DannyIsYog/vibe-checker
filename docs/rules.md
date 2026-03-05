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

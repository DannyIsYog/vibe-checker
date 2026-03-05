# Rules

All rules are prefixed `VIB`. Codes are assigned sequentially and never reused.

---

## `VIB001` — thursday-energy

**Severity:** warning

Thursdays occupy a liminal position in the work week — close enough to Friday to generate excitement, far enough from Monday to have accumulated significant technical debt in the developer's psyche. Functions written on Thursdays tend toward overengineering, premature abstraction, and a particular kind of ambition that the coming weekend will not resolve. This rule flags functions exceeding 20 lines authored on a Thursday, as identified by `git blame` or, when unavailable, the system clock at lint time.

```python
# Bad - authored on a Thursday, 27 lines long
def parse_user_preferences(input_data):
    # ... 27 lines of ambition
    pass

# Good - same function, written on a Wednesday
def parse_user_preferences(input_data):
    # ... 27 lines, but Wednesday energy is stable
    pass
```

```
VIB001 thursday energy detected: function 'parse_user_preferences' is 27 lines long and it's Thursday
```

---

## `VIB002` — todo-shame

**Severity:** warning

A `TODO` is a dream with a comment attached. A `FIXME` is a bug with good self-awareness. This rule flags both, because acknowledging a problem and solving it are not the same thing, and the diff doesn't care which one you did.

```python
# Bad
x = compute()  # TODO: handle edge case
y = broken()   # FIXME: this crashes on empty input

# Good
x = compute_with_edge_case_handled()
y = fixed()
```

```
VIB002 todo shame: this TODO has seen three sprints and counting
VIB002 todo shame: FIXME: acknowledged, unaddressed, unforgiven
```

---

## `VIB013` — god-variable

**Severity:** warning

Variables named `data`, `result`, `info`, `stuff`, `thing`, or `obj` describe their type, not their purpose. They are the naming equivalent of labeling a box "box". This rule flags assignments to those names.

```python
# Bad
data = fetch_user_records()
result = transform(data)

# Good
user_records = fetch_user_records()
transformed_records = transform(user_records)
```

```
VIB013 naming crime: `data` holds everything and describes nothing.
```

---

## `VIB014` — single-letter

**Severity:** warning

Single-letter variable names outside of loops and comprehensions carry no semantic information. `i` in a `for` loop is idiomatic. `i` as a module-level assignment is a mystery.

```python
# Bad
n = len(users)
x = get_config()

# Good — loop variables are fine
for i, user in enumerate(users):
    ...
```

```
VIB014 naming crime: `n` is one character and zero context.
```

---

## `VIB015` — temp-variable

**Severity:** warning

Variables named `temp`, `tmp`, `temp2`, etc. were supposed to be temporary. They never are. This rule flags assignments where `temp` or `tmp` appears in the variable name, as a reminder that nothing temporary ever gets cleaned up.

```python
# Bad
temp = process(data)
tmp_result = calculate()

# Good
intermediate_value = process(data)
```

```
VIB015 naming crime: `temp` was supposed to be temporary. it wasn't.
```

---

## `VIB016` — new-prefix

**Severity:** warning

`new_x` implies there is an `old_x` nearby. If there isn't, you just have a poorly named variable. If there is, you have a refactor that didn't finish. Either way, `new_` is a timestamp masquerading as a name.

```python
# Bad
new_user = create_user(form)
new_config = load_config()

# Good
created_user = create_user(form)
loaded_config = load_config()
```

```
VIB016 naming crime: `new_user` implies there's an `old_` version nearby. there isn't.
```

---

## `VIB017` — copy-suffix

**Severity:** warning

Suffixing `_copy`, `_2`, `_3`, etc. onto a variable name is version control implemented in identifiers. That is what git is for. This rule flags assignments where the name ends in `_copy` or a trailing number.

```python
# Bad
user_copy = copy(user)
config_2 = updated_config()

# Good
archived_user = copy(user)
updated_config = load_updated_config()
```

```
VIB017 naming crime: `config_2` is a variable name that tells you its history, not its purpose.
```

---

## `VIB018` — final-variable

**Severity:** warning

Nothing in code is actually final. Variables named `final_x` become `final_v2_x` in the next PR. `final` is not a descriptor, it is a wish. This rule flags assignments where `final` appears as a word in the variable name.

```python
# Bad
final_report = generate_report()
final_result = compute()

# Good
report = generate_report()
```

```
VIB018 naming crime: `final_report` — the hubris of `final` in a variable name.
```

---

## `VIB019` — flag-variable

**Severity:** warning

A variable called `flag` is a boolean that refused to describe itself. `is_active`, `should_retry`, `has_errors` — these are booleans with opinions. `flag` is a boolean with nothing to say.

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
VIB019 naming crime: `flag` is a boolean that refused to describe itself.
```

---

## `VIB020` — vague-class

**Severity:** warning

Classes with `Manager` in the name are classes with identity issues. They manage something. The question is what. `Manager` is a title given to a class when no one could agree on what the class actually does.

```python
# Bad
class UserManager:
    ...

# Good
class UserRegistration:
    ...
```

```
VIB020 naming crime: `UserManager` manages something. the question is what.
```

---

## `VIB081` — equals-true

**Severity:** warning

`if x == True` is a tautology wrapped in anxiety. You already have a boolean. `if x` was right there.

```python
# Bad
if is_active == True:
    ...

# Good
if is_active:
    ...
```

```
VIB081 boolean chaos: `== True` — you already have a boolean, what more do you need.
```

---

## `VIB082` — equals-false

**Severity:** warning

`if x == False` is `not x` with extra steps and less confidence. The `not` keyword exists. It has been here the whole time.

```python
# Bad
if is_active == False:
    ...

# Good
if not is_active:
    ...
```

```
VIB082 boolean chaos: `if not x` was right there and you walked right past it.
```

---

## `VIB083` — equals-none

**Severity:** warning

`None` is a singleton. You compare singletons with `is`, not `==`. PEP 8 asked nicely. This rule asks less nicely.

```python
# Bad
if result == None:
    ...

# Good
if result is None:
    ...
```

```
VIB083 boolean chaos: None is a singleton. you don't compare singletons with `==`.
```

---

## `VIB084` — not-equals

**Severity:** warning

`not x == y` is `x != y` with passive-aggressive energy. The `!=` operator exists. It is one character. It is right there on your keyboard.

```python
# Bad
if not user == admin:
    ...

# Good
if user != admin:
    ...
```

```
VIB084 boolean chaos: `not x == y` is `x != y` with passive-aggressive energy.
```

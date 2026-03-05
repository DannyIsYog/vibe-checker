"""Demo file showcasing every flake8-vibes rule.

This file is intentionally full of violations. Run it through vibe-check
to see every rule fire. Do not ship this to production. Please.

    vibe-check demo.py
"""

# VIB050 — dead __future__ import: Python 2 relics with no effect in Python 3
from __future__ import print_function

# VIB011 — import pdb: the debugging session that escaped into version control
import pdb

# VIB052 — import os just for os.path: expensive taste, narrow purpose
import os

import sys
import time
import asyncio

# VIB048 — star import: you imported everything and named nothing
from os.path import *  # noqa: F401,F403

# VIB049 — unused import: stood in the corner all night, never called upon
import json  # noqa: F401


# ── VIB002 — todo shame ──────────────────────────────────────────────────────

# TODO: refactor this before it becomes someone else's problem
# FIXME: this is broken and has been since the last sprint


# ── VIB021 — commented-out code graveyard ───────────────────────────────────

# result = compute_value()
# if result > threshold:
#     return process(result)


# ── VIB024 — named TODO ──────────────────────────────────────────────────────

# TODO(alice): this was assigned in 2019 and alice has not seen it since


# ── VIB026 — hack comment ────────────────────────────────────────────────────

# HACK: added this to make tests pass, not because it's correct


# ── VIB027 — do not touch ────────────────────────────────────────────────────

# DO NOT TOUCH — if you change this, everything breaks and nobody knows why


# ── VIB028 — this is fine ────────────────────────────────────────────────────

# this is fine


# ── VIB029 — lol / wtf comment ───────────────────────────────────────────────

# wtf is this doing here
# lol this actually works somehow


# ── VIB035 — magic comment ───────────────────────────────────────────────────

# uses magic to bypass the rate limiter  # noqa: VIB035


# ── VIB022 — type: ignore without explanation ────────────────────────────────

broken_annotation: int = "this is not an int"  # type: ignore


# ── VIB023 — bare noqa ───────────────────────────────────────────────────────

noqa_cowardice = True  # noqa


# ── VIB025 — obvious comment ─────────────────────────────────────────────────

counter = 0
# increment counter
counter = counter + 1


# ── VIB013 — god variables ───────────────────────────────────────────────────

def process_request(payload):
    data = payload.get("body")
    result = data["items"]
    info = result[0]
    return info


# ── VIB014 — single-letter variables outside loops ──────────────────────────

def calculate(n):
    x = n * 2
    y = x + 10
    return y


# ── VIB015 — temp variables ──────────────────────────────────────────────────

def build_response():
    temp = {"status": "ok"}
    tmp_headers = {"Content-Type": "application/json"}
    return temp, tmp_headers


# ── VIB016 — new_ prefix ─────────────────────────────────────────────────────

def update_user(user):
    new_user = {**user, "updated": True}
    new_email = user["email"].lower()
    return new_user, new_email


# ── VIB017 — _copy / _2 suffix ───────────────────────────────────────────────

def retry_handler(request):
    handler_copy = request.handler
    result_2 = handler_copy()
    return result_2


# ── VIB018 — final in variable name ──────────────────────────────────────────

def resolve_config(base, overrides):
    final_config = {**base, **overrides}
    final_result = final_config.get("value")
    return final_result


# ── VIB019 — flag variable ───────────────────────────────────────────────────

def validate(value):
    flag = value is not None
    error_flag = len(str(value)) > 100
    return flag, error_flag


# ── VIB020 — vague Manager class ─────────────────────────────────────────────

class DataManager:
    def handle(self, payload):
        return payload


class UserManager:
    def get(self, user_id):
        return user_id


# ── VIB030 — too many arguments ──────────────────────────────────────────────

def create_user(name, email, age, role, team, department, timezone):
    return {"name": name, "email": email, "role": role}


# ── VIB031 — deep nesting ────────────────────────────────────────────────────

def find_admin_active_item(users):
    for user in users:
        if user["active"]:
            if user["role"] == "admin":
                for item in user["items"]:
                    if item["enabled"]:
                        return item
    return None


# ── VIB032 — too many returns ────────────────────────────────────────────────

def classify(value):
    if value < 0:
        return "negative"
    if value == 0:
        return "zero"
    if value < 10:
        return "small"
    if value < 100:
        return "medium"
    return "large"


# ── VIB033 — bare except ─────────────────────────────────────────────────────

def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except:  # noqa: E722
        return None


# ── VIB034 — empty except ────────────────────────────────────────────────────

def parse_int(value):
    try:
        return int(value)
    except ValueError:
        pass


# ── VIB003 — except Exception ────────────────────────────────────────────────

def fetch_data(url):
    try:
        return requests.get(url)
    except Exception:
        return None


# ── VIB006 — raise Exception ─────────────────────────────────────────────────

def validate_age(age):
    if age < 0:
        raise Exception("age cannot be negative")


# ── VIB007 — re-raise without logging ────────────────────────────────────────

def connect(host):
    try:
        return socket.connect(host)
    except OSError:
        raise


# ── VIB008 — print() left behind ─────────────────────────────────────────────

def process(event):
    print("processing event:", event)
    return event


# ── VIB009 — breakpoint() left behind ────────────────────────────────────────

def debug_me(value):
    breakpoint()
    return value * 2


# ── VIB010 — pdb.set_trace() ─────────────────────────────────────────────────

def old_debug(value):
    pdb.set_trace()
    return value


# ── VIB012 — console.log in Python ───────────────────────────────────────────
# (valid Python syntax; undefined at runtime, but parses cleanly for linting)

def log_something(user_id):
    console.log(user_id)


# ── VIB041 — magic number ────────────────────────────────────────────────────

def check_threshold(value):
    if value > 42:
        return "too high"
    return value * 7


# ── VIB042 — hardcoded URL ───────────────────────────────────────────────────

API_BASE = "https://api.example.com/v1/data"


# ── VIB043 — hardcoded port ──────────────────────────────────────────────────

def get_server():
    return ("0.0.0.0", 8080)


# ── VIB044 — hardcoded path ───────────────────────────────────────────────────

CONFIG_PATH = "/Users/deploy/app/config.json"


# ── VIB045 — hardcoded timeout ───────────────────────────────────────────────

def wait_for_service():
    time.sleep(30)


def call_api(session, url):
    return session.get(url, timeout=10)


# ── VIB046 — hardcoded credentials ───────────────────────────────────────────

password = "supersecret123"
api_key = "sk-1234567890abcdef"


# ── VIB047 — hardcoded localhost ─────────────────────────────────────────────

DB_HOST = "localhost"
REDIS_URL = "redis://127.0.0.1:6379"


# ── VIB051 — import inside function ──────────────────────────────────────────

def load_yaml(path):
    import yaml
    return yaml.safe_load(open(path))


# ── VIB052 — import os just for os.path ──────────────────────────────────────

def get_config_path(name):
    return os.path.join("/etc", name)


# ── VIB053 — explicit return None ────────────────────────────────────────────

def do_nothing():
    return None


# ── VIB054 — assign then immediately return ──────────────────────────────────

def get_name(user):
    name = user["name"].strip()
    return name


# ── VIB055 — mutable default argument ────────────────────────────────────────

def append_to(item, container=[]):
    container.append(item)
    return container


# ── VIB056 — shadow builtin ──────────────────────────────────────────────────

def normalize(items):
    list = items[:]
    return list


# ── VIB057 — assign to _ then use it ─────────────────────────────────────────

def skip_it(value):
    _ = expensive_call(value)
    return _ + 1


# ── VIB058 — __str__ returns self.__dict__ ────────────────────────────────────

class Order:
    def __str__(self):
        return str(self.__dict__)


# ── VIB059 — empty except in __del__ ─────────────────────────────────────────

class Connection:
    def __del__(self):
        try:
            self.socket.close()
        except Exception:
            pass


# ── VIB060 — class with no docstring (>100 lines) ────────────────────────────
# Fires on any class longer than 100 lines with no docstring.
# Not demonstrated inline here since padding 100 lines is theatrical cruelty.


# ── VIB061 — super().__init__() not called ───────────────────────────────────

class Animal:
    def __init__(self, name):
        self.name = name


class Dog(Animal):
    def __init__(self, name, breed):
        self.breed = breed  # forgot super().__init__()


# ── VIB062 — no-op override ───────────────────────────────────────────────────

class Base:
    def process(self, data):
        return data.strip()


class Child(Base):
    def process(self, data):
        return super().process(data)


# ── VIB063 — multiple inheritance (3+ bases) ─────────────────────────────────

class Logger:
    pass


class Serializable:
    pass


class Cacheable:
    pass


class GodObject(Logger, Serializable, Cacheable):
    pass


# ── VIB064 / VIB065 / VIB067 — calendar crimes ───────────────────────────────
# These fire based on the file's last git commit date:
#   VIB001 — function >20 lines committed on a Thursday
#   VIB064 — tiny function committed on a Monday
#   VIB065 — any commit on a Friday
#   VIB067 — any commit in December


# ── VIB069 — test with no assertions ─────────────────────────────────────────
# Fires only in test files (filename contains "test").
# Pattern: a test_ function with no assert statements.

def test_nothing_asserted():
    result = process({"key": "value"})
    return result


# ── VIB070 — test named test_it ──────────────────────────────────────────────

def test_it():
    x = 1
    return x


# ── VIB071 — assert True ─────────────────────────────────────────────────────

assert True


# ── VIB072 — time.sleep() in tests ───────────────────────────────────────────
# Fires only in test files (filename contains "test").
# Pattern: time.sleep() called inside a test function.

def test_with_sleep():
    time.sleep(2)
    assert True


# ── VIB073 — copy-pasted test ────────────────────────────────────────────────
# Fires only in test files (filename contains "test").
# Pattern: two test_ functions with identical bodies.

def test_first():
    assert 1 + 1 == 2


def test_second():
    assert 1 + 1 == 2


# ── VIB074 — async without await ─────────────────────────────────────────────

async def fetch_user(user_id):
    return {"id": user_id}


# ── VIB076 — asyncio.sleep(0) ────────────────────────────────────────────────

async def yield_to_loop():
    await asyncio.sleep(0)


# ── VIB077 — string concat in loop ───────────────────────────────────────────

def join_names(names):
    result = ""
    for name in names:
        result += f"{name}, "
    return result


# ── VIB078 — % string formatting ─────────────────────────────────────────────

def greet_old_style(name):
    return "Hello, %s!" % name


# ── VIB079 — .format() with positional args ──────────────────────────────────

def greet_format(first, last):
    return "Hello, {} {}!".format(first, last)


# ── VIB080 — multiline string pretending to be a comment ─────────────────────

"""
This block of text is floating unattached at module level.
It is not a docstring. It is not assigned. It is just here.
This is a comment that refuses to use the # character.
"""


# ── VIB081 — == True ─────────────────────────────────────────────────────────

def check_active(status):
    if status == True:
        return "active"
    return "inactive"


# ── VIB082 — == False ────────────────────────────────────────────────────────

def check_inactive(status):
    if status == False:
        return "inactive"
    return "active"


# ── VIB083 — == None ─────────────────────────────────────────────────────────

def has_value(item):
    if item == None:
        return False
    return True


# ── VIB084 — not x == y instead of x != y ───────────────────────────────────

def not_equal(a, b):
    if not a == b:
        return True
    return False


# ── VIB085 — docstring repeats function name ─────────────────────────────────

def load_user(user_id):
    """Load user."""
    return db.get(user_id)


# ── VIB086 — docstring summary missing period ────────────────────────────────

def parse_config(path):
    """Parse the configuration file"""
    return {}


# ── VIB087 — docstring Args section doesn't match signature ──────────────────

def create_item(name, value):
    """Create a new item.

    Args:
        name: the item name.
        value: the item value.
        owner: a parameter that was deleted but lives on in the docstring.
    """
    return {"name": name, "value": value}


# ── VIB088 — docstring longer than the function body ─────────────────────────

def add(a, b):
    """Add two numbers together and return their sum.

    This operation is fundamental to mathematics and to this application.
    Without it, numerical computation would simply not be possible in this
    module. The two inputs are summed using the built-in addition operator,
    which has been available in Python since the beginning of time.

    Args:
        a: the first number.
        b: the second number.

    Returns:
        The sum of a and b.
    """
    return a + b


# ── VIB089 — lambda assigned to variable ─────────────────────────────────────

double = lambda x: x * 2
square = lambda x: x ** 2


# ── VIB090 — global statement ────────────────────────────────────────────────

_request_count = 0


def increment_request_count():
    global _request_count
    _request_count += 1


# ── VIB091 — eval() ──────────────────────────────────────────────────────────

def run_expression(expr):
    return eval(expr)


# ── VIB092 — exec() ──────────────────────────────────────────────────────────

def run_code(code):
    exec(code)


# ── VIB093 — private names in __all__ ────────────────────────────────────────

__all__ = ["DataManager", "_internal_helper", "UserManager"]


# ── VIB094 — file too long (>500 lines) ──────────────────────────────────────
# This file exceeds 500 lines, so VIB094 fires automatically.


# ── VIB095 — nested comprehension (3+ levels deep) ───────────────────────────

deep = [x for x in [y for y in [z for z in range(5)]]]


# ── VIB096 — dict() constructor instead of literal ───────────────────────────

db_config = dict(host="localhost", port=5432, name="mydb")


# ── VIB097 — list() wrapping a list literal ──────────────────────────────────

items = list([1, 2, 3, 4, 5])


# ── VIB098 — assert in non-test code ─────────────────────────────────────────

def verify_positive(n):
    assert n > 0, "n must be positive"
    return n


# ── VIB099 — sys.exit() ──────────────────────────────────────────────────────

def abort(message):
    print(message)
    sys.exit(1)


# ── VIB100 — zero-star repo ───────────────────────────────────────────────────
# Fires in files that contain 5+ print() calls and nothing else — no functions,
# no classes, just bare prints. Can't demonstrate here because this file has
# plenty of structure. A script with only print statements would trigger it.

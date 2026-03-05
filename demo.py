"""Demo file for flake8-vibes."""


def clean_function():
    """Short and clean."""
    return 42


def very_long_function():
    """This function is suspiciously long."""
    step_1 = 1
    step_2 = 2
    step_3 = 3
    step_4 = 4
    step_5 = 5
    step_6 = 6
    step_7 = 7
    step_8 = 8
    step_9 = 9
    step_10 = 10
    step_11 = 11
    step_12 = 12
    step_13 = 13
    step_14 = 14
    step_15 = 15
    step_16 = 16
    step_17 = 17
    step_18 = 18
    step_19 = 19
    step_20 = 20
    step_21 = 21
    return step_1 + step_21


async def another_long_function():
    """An async function that is also very long."""
    a = 1
    b = 2
    c = 3
    d = 4
    e = 5
    f = 6
    g = 7
    h = 8
    i = 9
    j = 10
    k = 11
    l = 12  # noqa: E741
    m = 13
    n = 14
    o = 15
    p = 16
    q = 17
    r = 18
    s = 19
    t = 20
    u = 21
    return a + u

# TODO: refactor this someday
# FIXME: this is broken but it's Wednesday so whatever
x = 42


# --- boolean chaos showcase ---

def check_status(is_active, value, result, user):
    # VIB081: comparing to True explicitly
    if is_active == True:
        print("active")

    # VIB082: comparing to False instead of using not
    if is_active == False:
        print("not active")

    # VIB083: using == None instead of is None
    if user == None:
        print("no user")

    if None == value:
        print("also no value")

    # VIB084: not x == y instead of x != y
    if not result == 42:
        print("wrong answer")


# --- naming crimes showcase ---

# VIB013: god variables — names that hold everything and mean nothing
def process_request(payload):
    data = payload.get("body")
    result = data["items"]
    info = result[0]
    return info


# VIB014: single-letter variables outside loops
def calculate(n):
    x = n * 2
    y = x + 10
    return y


# VIB015: temp/tmp anything — names that were never meant to last
def build_response():
    temp = {"status": "ok"}
    tmp_headers = {"Content-Type": "application/json"}
    return temp, tmp_headers


# VIB016: new_ prefix — implies an old_ that doesn't exist
def update_user(user):
    new_user = {**user, "updated": True}
    new_email = user["email"].lower()
    return new_user, new_email


# VIB017: _2 or _copy suffix — version control in a variable name
def retry_handler(request):
    handler_copy = request.handler
    result_2 = handler_copy()
    return result_2


# VIB018: final in the variable name — the hubris
def resolve_config(base, overrides):
    final_config = {**base, **overrides}
    final_result = final_config.get("value")
    return final_result


# VIB019: flag variable — a boolean that refused to explain itself
def validate(value):
    flag = value is not None
    error_flag = len(str(value)) > 100
    return flag, error_flag


# VIB020: Manager class with no clear purpose
class DataManager:
    def handle(self, payload):
        return payload


class UserManager:
    def get(self, user_id):
        return user_id

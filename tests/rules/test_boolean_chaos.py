from __future__ import annotations

import ast

from flake8_vibes.rules.boolean_chaos import (
    EqualsFalseRule,
    EqualsNoneRule,
    EqualsTrueRule,
    NotEqualsRule,
    _EQUALS_FALSE_MESSAGES,
    _EQUALS_NONE_MESSAGES,
    _EQUALS_TRUE_MESSAGES,
    _NOT_EQUALS_MESSAGES,
    _is_const,
)


def parse(source: str) -> ast.AST:
    return ast.parse(source)


def check_true(source: str) -> list:
    return EqualsTrueRule().check(parse(source))


def check_false(source: str) -> list:
    return EqualsFalseRule().check(parse(source))


def check_none(source: str) -> list:
    return EqualsNoneRule().check(parse(source))


def check_not_eq(source: str) -> list:
    return NotEqualsRule().check(parse(source))


# --- VIB081: == True ---

def test_flags_equals_true():
    errors = check_true("if x == True: pass")
    assert len(errors) == 1
    assert "VIB081" in errors[0][2]


def test_flags_true_equals_x():
    errors = check_true("if True == x: pass")
    assert len(errors) == 1
    assert "VIB081" in errors[0][2]


def test_no_flag_plain_truthy_check():
    assert check_true("if x: pass") == []


def test_no_flag_equals_false_for_081():
    assert check_true("if x == False: pass") == []


def test_no_flag_equals_none_for_081():
    assert check_true("if x == None: pass") == []


def test_081_error_tuple_format():
    row, col, msg, typ = check_true("if x == True: pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_081_messages_list():
    assert len(_EQUALS_TRUE_MESSAGES) >= 2


# --- VIB082: == False ---

def test_flags_equals_false():
    errors = check_false("if x == False: pass")
    assert len(errors) == 1
    assert "VIB082" in errors[0][2]


def test_flags_false_equals_x():
    errors = check_false("if False == x: pass")
    assert len(errors) == 1
    assert "VIB082" in errors[0][2]


def test_no_flag_not_x():
    assert check_false("if not x: pass") == []


def test_no_flag_equals_true_for_082():
    assert check_false("if x == True: pass") == []


def test_082_error_tuple_format():
    row, col, msg, typ = check_false("if x == False: pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_082_messages_list():
    assert len(_EQUALS_FALSE_MESSAGES) >= 2


# --- VIB083: == None ---

def test_flags_equals_none():
    errors = check_none("if x == None: pass")
    assert len(errors) == 1
    assert "VIB083" in errors[0][2]


def test_flags_none_equals_x():
    errors = check_none("if None == x: pass")
    assert len(errors) == 1
    assert "VIB083" in errors[0][2]


def test_no_flag_is_none():
    assert check_none("if x is None: pass") == []


def test_no_flag_is_not_none():
    assert check_none("if x is not None: pass") == []


def test_083_flags_multiple():
    source = "x == None\ny == None\n"
    errors = check_none(source)
    assert len(errors) == 2


def test_083_error_tuple_format():
    row, col, msg, typ = check_none("if x == None: pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_083_messages_list():
    assert len(_EQUALS_NONE_MESSAGES) >= 2


# --- VIB084: not x == y ---

def test_flags_not_x_eq_y():
    errors = check_not_eq("if not x == y: pass")
    assert len(errors) == 1
    assert "VIB084" in errors[0][2]


def test_no_flag_not_eq_operator():
    assert check_not_eq("if x != y: pass") == []


def test_no_flag_plain_not():
    assert check_not_eq("if not x: pass") == []


def test_no_flag_unary_minus():
    assert check_not_eq("y = -x") == []


def test_no_flag_not_with_lt():
    assert check_not_eq("if not x < y: pass") == []


def test_084_error_tuple_format():
    row, col, msg, typ = check_not_eq("if not x == y: pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_084_messages_list():
    assert len(_NOT_EQUALS_MESSAGES) >= 2


# --- _is_const helper ---

def test_is_const_true():
    node = ast.Constant(value=True)
    assert _is_const(node, True) is True


def test_is_const_false():
    node = ast.Constant(value=False)
    assert _is_const(node, False) is True


def test_is_const_none():
    node = ast.Constant(value=None)
    assert _is_const(node, None) is True


def test_is_const_wrong_value():
    node = ast.Constant(value=True)
    assert _is_const(node, False) is False


def test_is_const_non_constant():
    node = ast.Name(id="x", ctx=ast.Load())
    assert _is_const(node, True) is False

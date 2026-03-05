from __future__ import annotations

import ast

from flake8_vibes.rules.naming_crimes import (
    CopySuffixRule,
    FinalVariableRule,
    FlagVariableRule,
    GodVariableRule,
    NewPrefixRule,
    SingleLetterRule,
    TempVariableRule,
    VagueClassRule,
    _COPY_SUFFIX_MESSAGES,
    _OPAQUE_BOOL_MESSAGES,
    _OVERCONFIDENT_NAME_MESSAGES,
    _GOD_VARIABLE_MESSAGES,
    _NEW_PREFIX_MESSAGES,
    _SINGLE_LETTER_MESSAGES,
    _PLACEHOLDER_NAME_MESSAGES,
    _VAGUE_CLASS_MESSAGES,
    _loop_and_comp_positions,
    _name_words,
)


def parse(source: str) -> ast.AST:
    return ast.parse(source)


def check_013(source: str) -> list:
    return GodVariableRule().check(parse(source))


def check_014(source: str) -> list:
    return SingleLetterRule().check(parse(source))


def check_015(source: str) -> list:
    return TempVariableRule().check(parse(source))


def check_016(source: str) -> list:
    return NewPrefixRule().check(parse(source))


def check_017(source: str) -> list:
    return CopySuffixRule().check(parse(source))


def check_018(source: str) -> list:
    return FinalVariableRule().check(parse(source))


def check_019(source: str) -> list:
    return FlagVariableRule().check(parse(source))


def check_020(source: str) -> list:
    return VagueClassRule().check(parse(source))


# --- VIB013: God variable ---

def test_013_flags_data():
    errors = check_013("data = {}")
    assert len(errors) == 1
    assert "VIB013" in errors[0][2]


def test_013_flags_result():
    errors = check_013("result = compute()")
    assert len(errors) == 1
    assert "VIB013" in errors[0][2]


def test_013_flags_all_god_names():
    for name in ("data", "result", "info", "stuff", "thing", "obj"):
        errors = check_013(f"{name} = 1")
        assert len(errors) == 1, f"expected flag for {name!r}"
        assert "VIB013" in errors[0][2]


def test_013_no_flag_descriptive_name():
    assert check_013("user_data = {}") == []
    assert check_013("parsed_result = compute()") == []
    assert check_013("total = 0") == []


def test_013_error_tuple_format():
    row, col, msg, typ = check_013("data = {}")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_013_message_contains_name():
    _, _, msg, _ = check_013("result = compute()")[0]
    assert "result" in msg


def test_013_messages_list():
    assert len(_GOD_VARIABLE_MESSAGES) >= 2


# --- VIB014: Single-letter variables outside loops ---

def test_014_flags_single_letter_assignment():
    errors = check_014("x = 1")
    assert len(errors) == 1
    assert "VIB014" in errors[0][2]


def test_014_flags_multiple_single_letters():
    errors = check_014("x = 1\ny = 2\nz = 3")
    assert len(errors) == 3


def test_014_no_flag_loop_var():
    assert check_014("for i in range(10): pass") == []


def test_014_no_flag_loop_var_tuple():
    assert check_014("for i, j in items: pass") == []


def test_014_no_flag_listcomp_var():
    assert check_014("[x for x in range(10)]") == []


def test_014_no_flag_genexp_var():
    assert check_014("list(x for x in items)") == []


def test_014_no_flag_underscore():
    assert check_014("_ = unused()") == []


def test_014_no_flag_long_name():
    assert check_014("xy = 1") == []


def test_014_error_tuple_format():
    row, col, msg, typ = check_014("x = 1")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_014_messages_list():
    assert len(_SINGLE_LETTER_MESSAGES) >= 2


# --- VIB015: temp anything ---

def test_015_flags_temp():
    errors = check_015("temp = 1")
    assert len(errors) == 1
    assert "VIB015" in errors[0][2]


def test_015_flags_tmp():
    errors = check_015("tmp = 1")
    assert len(errors) == 1
    assert "VIB015" in errors[0][2]


def test_015_flags_temp2():
    errors = check_015("temp2 = 1")
    assert len(errors) == 1
    assert "VIB015" in errors[0][2]


def test_015_flags_temp_prefix():
    errors = check_015("temp_value = 1")
    assert len(errors) == 1
    assert "VIB015" in errors[0][2]


def test_015_flags_temp_suffix():
    errors = check_015("my_temp = 1")
    assert len(errors) == 1
    assert "VIB015" in errors[0][2]


def test_015_no_flag_temporary():
    assert check_015("temporary = 1") == []


def test_015_no_flag_template():
    assert check_015("template = 1") == []


def test_015_no_flag_normal_name():
    assert check_015("value = 1") == []


def test_015_error_tuple_format():
    row, col, msg, typ = check_015("temp = 1")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_015_messages_list():
    assert len(_PLACEHOLDER_NAME_MESSAGES) >= 2


# --- VIB016: new_ prefix ---

def test_016_flags_new_prefix():
    errors = check_016("new_value = 1")
    assert len(errors) == 1
    assert "VIB016" in errors[0][2]


def test_016_flags_bare_new():
    errors = check_016("new = get_thing()")
    assert len(errors) == 1
    assert "VIB016" in errors[0][2]


def test_016_no_flag_no_new():
    assert check_016("value = 1") == []
    assert check_016("renewed = 1") == []
    assert check_016("newer = 1") == []


def test_016_error_tuple_format():
    row, col, msg, typ = check_016("new_data = {}")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_016_message_contains_name():
    _, _, msg, _ = check_016("new_data = {}")[0]
    assert "new_data" in msg


def test_016_messages_list():
    assert len(_NEW_PREFIX_MESSAGES) >= 2


# --- VIB017: _2 or _copy suffix ---

def test_017_flags_number_suffix():
    errors = check_017("handler_2 = fn()")
    assert len(errors) == 1
    assert "VIB017" in errors[0][2]


def test_017_flags_copy_suffix():
    errors = check_017("handler_copy = fn()")
    assert len(errors) == 1
    assert "VIB017" in errors[0][2]


def test_017_flags_higher_number():
    errors = check_017("func_3 = fn()")
    assert len(errors) == 1
    assert "VIB017" in errors[0][2]


def test_017_no_flag_copy_not_suffix():
    assert check_017("copy_of_handler = fn()") == []


def test_017_no_flag_normal_name():
    assert check_017("handler = fn()") == []
    assert check_017("value2 = 1") == []  # no underscore before digit


def test_017_error_tuple_format():
    row, col, msg, typ = check_017("result_2 = 1")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_017_messages_list():
    assert len(_COPY_SUFFIX_MESSAGES) >= 2


# --- VIB018: final in variable name ---

def test_018_flags_bare_final():
    errors = check_018("final = compute()")
    assert len(errors) == 1
    assert "VIB018" in errors[0][2]


def test_018_flags_final_prefix():
    errors = check_018("final_result = compute()")
    assert len(errors) == 1
    assert "VIB018" in errors[0][2]


def test_018_flags_final_suffix():
    errors = check_018("answer_final = compute()")
    assert len(errors) == 1
    assert "VIB018" in errors[0][2]


def test_018_no_flag_finalize():
    assert check_018("finalize = True") == []


def test_018_no_flag_finalist():
    assert check_018("finalist = True") == []


def test_018_no_flag_normal_name():
    assert check_018("answer = compute()") == []


def test_018_error_tuple_format():
    row, col, msg, typ = check_018("final_value = 1")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_018_messages_list():
    assert len(_OVERCONFIDENT_NAME_MESSAGES) >= 2


# --- VIB019: flag variable name ---

def test_019_flags_bare_flag():
    errors = check_019("flag = True")
    assert len(errors) == 1
    assert "VIB019" in errors[0][2]


def test_019_flags_error_flag():
    errors = check_019("error_flag = False")
    assert len(errors) == 1
    assert "VIB019" in errors[0][2]


def test_019_flags_flag_value():
    errors = check_019("flag_value = 0")
    assert len(errors) == 1
    assert "VIB019" in errors[0][2]


def test_019_no_flag_flagged():
    assert check_019("flagged = True") == []


def test_019_no_flag_normal_bool():
    assert check_019("is_valid = True") == []
    assert check_019("has_errors = False") == []


def test_019_error_tuple_format():
    row, col, msg, typ = check_019("flag = True")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_019_messages_list():
    assert len(_OPAQUE_BOOL_MESSAGES) >= 2


# --- VIB020: Manager class ---

def test_020_flags_manager_class():
    errors = check_020("class UserManager: pass")
    assert len(errors) == 1
    assert "VIB020" in errors[0][2]


def test_020_flags_bare_manager():
    errors = check_020("class Manager: pass")
    assert len(errors) == 1
    assert "VIB020" in errors[0][2]


def test_020_flags_snake_case_manager():
    errors = check_020("class user_manager: pass")
    assert len(errors) == 1
    assert "VIB020" in errors[0][2]


def test_020_flags_manager_mixin():
    errors = check_020("class DataManagerMixin: pass")
    assert len(errors) == 1
    assert "VIB020" in errors[0][2]


def test_020_no_flag_management():
    assert check_020("class DataManagement: pass") == []


def test_020_no_flag_normal_class():
    assert check_020("class UserService: pass") == []
    assert check_020("class Repository: pass") == []


def test_020_error_tuple_format():
    row, col, msg, typ = check_020("class UserManager: pass")[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert isinstance(typ, type)


def test_020_message_contains_name():
    _, _, msg, _ = check_020("class UserManager: pass")[0]
    assert "UserManager" in msg


def test_020_messages_list():
    assert len(_VAGUE_CLASS_MESSAGES) >= 2


# --- helper tests ---

def test_loop_and_comp_positions_for_loop():
    tree = ast.parse("for i in range(10): pass")
    pos = _loop_and_comp_positions(tree)
    assert len(pos) == 1


def test_loop_and_comp_positions_listcomp():
    tree = ast.parse("[x for x in items]")
    pos = _loop_and_comp_positions(tree)
    assert len(pos) >= 1


def test_name_words_pascal_case():
    assert _name_words("UserManager") == ["user", "manager"]


def test_name_words_snake_case():
    assert _name_words("user_manager") == ["user", "manager"]


def test_name_words_single():
    assert _name_words("Manager") == ["manager"]


def test_name_words_management_not_manager():
    assert "manager" not in _name_words("DataManagement")

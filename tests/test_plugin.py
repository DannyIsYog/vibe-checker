from __future__ import annotations

import ast

import pytest

from flake8_vibes.plugin import VibesPlugin
from flake8_vibes.rules.base import VibRule


def test_plugin_instantiation():
    tree = ast.parse("x = 1")
    plugin = VibesPlugin(tree, filename="test.py")
    assert plugin.name == "flake8-vibes"
    assert plugin.version == "0.1.0"


def test_plugin_run_returns_iterable():
    tree = ast.parse("x = 1")
    plugin = VibesPlugin(tree, filename="test.py")
    results = list(plugin.run())
    assert isinstance(results, list)


def test_plugin_run_output_format(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: True
    )
    source = "\n".join(["def big_fn():"] + [f"    x_{i} = {i}" for i in range(25)])
    tree = ast.parse(source)
    plugin = VibesPlugin(tree, filename="test.py")
    results = list(plugin.run())
    assert len(results) >= 1
    row, col, msg, typ = results[0]
    assert isinstance(row, int)
    assert isinstance(col, int)
    assert isinstance(msg, str)
    assert "VIB001" in msg
    assert isinstance(typ, type)


def test_vib_rule_base_raises():
    rule = VibRule()
    tree = ast.parse("x = 1")
    with pytest.raises(NotImplementedError):
        rule.check(tree)


def test_plugin_no_violations_on_clean_code(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setattr(
        "flake8_vibes.rules.thursday_energy._is_thursday", lambda _: True
    )
    tree = ast.parse("def small(): pass")
    plugin = VibesPlugin(tree, filename="test.py")
    results = list(plugin.run())
    assert results == []

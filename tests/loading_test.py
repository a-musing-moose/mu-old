import pytest
from mu.loading import load_from_path


def test_can_load_abitrary_attribute_from_module():
    a = load_from_path("mu.loading.load_from_path")
    assert a == load_from_path


def test_raises_exception_for_missing_path():
    with pytest.raises(ImportError):
        load_from_path("does.not.exist")


def test_raises_exception_for_invalid_path():
    with pytest.raises(ImportError):
        load_from_path("to_short")

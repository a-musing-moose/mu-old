import pytest
import json
import os


os.environ['MU_SETTINGS'] = "{}"  # loading conf module will load settings


from mu.conf import Settings


def test_str_loading():
    settings = {'key': 'value'}
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    assert c.json == settings
    del os.environ['MU_SETTINGS']


def test_dynamic_key_setting():
    settings = {'key': 'value'}
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    assert c.key == settings['key']
    del os.environ['MU_SETTINGS']


def test_does_not_pull_setting_twice():
    settings = {'key': 'value'}
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    assert c.key == settings['key']
    c.json = {}
    assert c.key == settings['key']
    del os.environ['MU_SETTINGS']


def test_exception_raise_for_invalid_key():
    settings = {'key': 'value'}
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    with pytest.raises(AttributeError):
        c.nope
    del os.environ['MU_SETTINGS']


def test_pulls_setting_from_environment():
    try:
        del os.environ['TEST_ENV']  # Ensure it is not present
    except:
        pass
    settings = {'key': {'env': 'TEST_ENV'}}
    os.environ['TEST_ENV'] = 'yep'
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    assert c.key == 'yep'
    del os.environ['TEST_ENV']
    del os.environ['MU_SETTINGS']


def test_uses_default_is_env_not_set():
    try:
        del os.environ['TEST_ENV']  # Ensure it is not present
    except:
        pass
    settings = {'key': {'env': 'TEST_ENV', 'default': 'ummm'}}
    os.environ['MU_SETTINGS'] = json.dumps(settings)
    c = Settings()
    assert c.key == 'ummm'
    del os.environ['MU_SETTINGS']


def test_load_from_file(tmpdir):
    settings = {'key': 'value'}
    f = tmpdir.join("settings.json")
    f.write(json.dumps(settings))
    os.environ['MU_SETTINGS'] = f.strpath
    c = Settings()
    assert c.json == settings
    del os.environ['MU_SETTINGS']

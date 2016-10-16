"""test for brain module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest


def test_simple_import():
    """test simple error import.

    the first error raised because IO is disable when testing.
    IO error is on profile_populator module.
    """
    with pytest.raises(IOError):
        from melissa import brain  # NOQA


def test_import_and_mock_populator():
    """test mock profile_populator module when import this module.

    this still raise error because profile.json is missing.
    IO error is raised on profile module
    """
    with pytest.raises(IOError):
        with mock.patch('melissa.profile_populator.profile_populator'):
            from melissa import brain  # NOQA

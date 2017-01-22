"""test module."""
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

from pushbullet import Pushbullet


def test_push(info):
    with mock.patch('melissa.profile_loader.load_profile'):
        from melissa.actions import notification
        notification.push(info)

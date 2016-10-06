import os


def test_file_path():
    assert(os.path.isfile('profile.json')) == False # noqa

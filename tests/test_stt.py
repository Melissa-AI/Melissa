"""test tts module."""
import unittest
try:  # py3
    from unittest import mock
except ImportError:  # py2
    import mock

import pytest

from melissa.tts import tts


def test_empty_string():
    """test empty string."""
    assert tts('') == 0


def test_mock_input():
    """test using different type of variable such as Mock object."""
    # NOTE: tts only receive string or equivalent as input.
    with pytest.raises(TypeError):
        tts(mock.Mock())


@mock.patch('melissa.tts.subprocess')
@mock.patch('melissa.tts.sys')
class TestDifferentPlatform(unittest.TestCase):
    """test different platform."""

    def setUp(self):
        """set up func."""
        self.message = ''

    def test_default_mock(self, mock_sys, mock_subprocess):
        """test using default mock obj."""
        tts(self.message)
        # NOTE: the default for linux/win32 with gender female. ( see '-ven+f3' input)
        mock_call = mock.call.call(['espeak', '-ven+f3', '-s170', self.message])
        assert mock_call in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_darwin_platform(self, mock_sys, mock_subprocess):
        """test darwin platform."""
        mock_sys.platform = 'darwin'
        tts(self.message)
        # NOTE: the default for macos with gender female. (it don't have 'valex' flag)
        assert mock.call.call(['say', self.message]) in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    @mock.patch('melissa.tts.profile')
    def test_darwin_platform_male_gender(self, mock_profile, mock_sys, mock_subprocess, ):
        """test darwin platform and male gender."""
        mock_sys.platform = 'darwin'
        mock_profile.data = {'va_gender': 'male'}
        tts(self.message)
        assert mock.call.call(['say', '-valex', self.message]) in mock_subprocess.mock_calls
        assert len(mock_subprocess.mock_calls) == 1

    def test_random_platform(self, mock_sys, mock_subprocess):
        """test random platform."""
        mock_sys.platform = 'random'
        tts(self.message)
        # empty list/mock_subprocess not called
        assert not mock_subprocess.mock_calls

    def test_linux_win32_platform(self, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        for platform in ['linux', 'win32']:
            mock_sys.platform = platform
            tts(self.message)
            # NOTE: the default for linux/win32 with gender female. ( see '-ven+f3' input)
            mock_call = mock.call.call(['espeak', '-ven+f3', '-s170', self.message])
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

    @mock.patch('melissa.tts.profile')
    def test_linux_win32_platform_male_gender(self, mock_profile, mock_sys, mock_subprocess):
        """test linux and win32 platform."""
        mock_profile.data['va_gender'] = 'male'
        for platform in ('linux', 'win32'):
            mock_sys.platform = platform
            tts(self.message)
            mock_call = mock.call.call(['espeak', '-s170', self.message])
            assert mock_call in mock_subprocess.mock_calls
            assert len(mock_subprocess.mock_calls) == 1

            # reset mock_subprocess
            mock_subprocess.reset_mock()

from unittest import TestCase
from unittest.mock import MagicMock, patch

from nak import utils


class TestUtils(TestCase):
    ####
    # hide_variable
    ####
    def test_hide_variable_should_return_string_we_expect(self):
        actual = utils.hide_variable('12212112345666')
        expected = '********12345666'
        assert actual == expected

    def test_hide_variable_with_all_true_should_return_string_we_expect(self):
        actual = utils.hide_variable('12212112345666', all=True)
        expected = '********'
        assert actual == expected

    ####
    # get_error_from_response
    ####
    def test_get_error_from_response_should_return_correctly_error_msg(self):
        response = MagicMock()
        response.json.return_value = dict(
            file=['required', ]
        )

        actual = utils.get_error_from_response(response)
        assert actual == '"file" : required'

        response.json.return_value = dict(
            error='file is required'
        )

        actual = utils.get_error_from_response(response)
        assert actual == 'file is required'

    ####
    # get_all_file
    ####
    @patch('os.listdir')
    def test_get_all_file_with_allow_file_should_return_correctly_file_list(self, mock_listdir):
        mock_listdir.return_value = [
            'test1.html', 'test2.html', 'test.json'
        ]

        actual = utils.get_all_file('.')

        assert actual == ['./test1.html', './test2.html', './test.json']

    @patch('os.listdir')
    def test_get_all_file_with_not_allow_file_should_return_correctly_file_list(self, mock_listdir):
        mock_listdir.return_value = [
            '.env', 'config.yml', '.tmp', 'test1.a', 'test2.b', 'test.c'
        ]

        actual = utils.get_all_file('.')
        assert actual == []

    @patch('os.listdir')
    def test_get_all_file_with_required_extension_file_should_return_correctly_file_list(self, mock_listdir):
        mock_listdir.return_value = [
            'test1.a', 'test2.b', 'test.c', 'test_zip1.zip', 'test_zip2.zip'
        ]

        actual = utils.get_all_file('.', required_extension='.zip')
        assert actual == ['./test_zip1.zip', './test_zip2.zip']

    ####
    # get_lastest_build_file
    ###
    @patch("nak.utils.Path")
    def test_get_lastest_build_file_with_no_zip_file_should_return_none(self, mock_path):
        mock_dir = MagicMock()
        mock_path.return_value = mock_dir

        mock_dir.iterdir.return_value = [
            MagicMock(
                is_file=MagicMock(return_value=True), suffix='.txt', as_posix=MagicMock(return_value='file1.txt')),
            MagicMock(
                is_file=MagicMock(return_value=True), suffix='.txt', as_posix=MagicMock(return_value='file2.txt'))
        ]

        result = utils.get_lastest_build_file()
        assert result is None

    @patch("nak.utils.Path")
    def test_get_lastest_build_file_with_have_zip_fiile_should_return_latest_file(self, mock_path):
        mock_dir = MagicMock()
        mock_path.return_value = mock_dir

        mock_file1 = MagicMock(
            is_file=MagicMock(return_value=True), suffix='.zip', as_posix=MagicMock(return_value='file1.txt'))
        mock_file1.stat.return_value.st_ctime = 1000
        mock_file1.as_posix.return_value = 'file1.zip'

        mock_file2 = MagicMock(
            is_file=MagicMock(return_value=True), suffix='.zip', as_posix=MagicMock(return_value='file2.txt'))
        mock_file2.stat.return_value.st_ctime = 2000
        mock_file2.as_posix.return_value = 'file2.zip'

        mock_dir.iterdir.return_value = [mock_file1, mock_file2]

        result = utils.get_lastest_build_file()
        assert result == 'file2.zip'

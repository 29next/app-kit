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
